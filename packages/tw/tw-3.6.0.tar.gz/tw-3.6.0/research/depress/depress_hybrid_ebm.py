# Copyright 2021 The KaiJIN Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Hybrid Training: generative-discriminative training for depression recognition
"""
import os
import random
import argparse
import tqdm
import functools
import cv2
import numpy as np

import torch
from torch import nn

from torch.utils import tensorboard

import tw
from tw import logger
from tw import transform as T


class PredictorNet(nn.Module):
  def __init__(self, input_dim, feature_dim, hidden_dim):
    super(PredictorNet, self).__init__()
    self.map = nn.Linear(input_dim, 64)
    self.linear1 = nn.Sequential(
        nn.Linear(feature_dim + 64, hidden_dim),
        nn.ReLU6())
    self.linear2 = nn.Sequential(
        nn.Linear(hidden_dim, hidden_dim),
        nn.ReLU6())
    self.linear3 = nn.Sequential(
        nn.Linear(hidden_dim, hidden_dim),
        nn.ReLU6())
    self.predict = nn.Linear(hidden_dim, 1)

  def forward(self, x, y):
    """Combine input and target to predict prob.

    Args:
        x: (batchsize, hidden dim)
        y: (batchsize, num_samples * 1)

    Returns:
        score: (batchsize, num_samples)
    """
    if x.dim() == 3:
      x = x.mean(dim=2)

    assert x.dim() == 2, x.shape
    assert y.dim() == 2, y.shape

    bs, num_sample = y.shape  # [n, k]
    x = x.unsqueeze(dim=1).expand(-1, num_sample, -1)  # [n, k, c]
    x = x.reshape(bs * num_sample, -1)  # [bs * num_sample, hidden_dim]
    y = y.reshape(bs * num_sample, -1)  # [bs * num_sample, 1]
    y = self.map(y)  # [nk, c]
    xy = self.linear1(torch.cat([x, y], dim=1))  # [nk, 2c] -> [nk, h]
    xy = self.linear2(xy) + xy
    xy = self.linear3(xy) + xy
    score = self.predict(xy)

    return score.view(bs, num_sample)


class ModelWrapper(nn.Module):

  def __init__(self, backbone: nn.Module, classifier: nn.Module, predictor: nn.Module):
    super(ModelWrapper, self).__init__()
    self.backbone = backbone
    self.classifier = classifier
    self.predictor = predictor


class DepressHybridEBM():

  def __init__(self, config):
    """classification for 2d image.
    """
    self.Config = config

    # overwrite when dist
    if self.Config.dist_size > 1:
      self.Config.device = 'cuda:{}'.format(self.Config.dist_rank)
    self.Master = True if self.Config.dist_rank == 0 else False

    # evaluation and tensorboard
    self.Evaluator = tw.evaluator.Avec2014Evaluator()
    self.Writer = tensorboard.SummaryWriter(log_dir=self.Config.root)

    # scalar
    self.Epoch = 0
    self.Step = 0

    # models
    self.Model = self._build_model()

    # build optim
    if self.Config.task == 'train':
      self.Optim = self._build_optim(self.Model)
    else:
      self.Optim = None

    # load model and possible optimizer
    if self.Config.model_path is not None:
      self._load()

    # extend to distributed
    if self.Config.dist_size > 1:
      self.Model = torch.nn.SyncBatchNorm.convert_sync_batchnorm(self.Model)
      self.Model = torch.nn.parallel.DistributedDataParallel(self.Model, device_ids=[self.Config.dist_rank])

  def _transform_train(self, metas):
    T.random_crop(metas, 192, 192)
    T.resize(metas, 112, 112, cv2.INTER_CUBIC)
    T.random_hflip(metas, 0.5)
    T.truncated_standardize(metas)
    T.to_tensor(metas)
    return metas

  def _transform_test(self, metas):
    T.center_crop(metas, 192, 192)
    T.resize(metas, 112, 112, cv2.INTER_CUBIC)
    T.truncated_standardize(metas)
    T.to_tensor(metas)
    return metas

  def _build_dataset(self, phase: tw.phase):
    """build train/val datasets
    """
    cfg = self.Config

    # build target datasets
    if phase == tw.phase.train:
      dataset = tw.datasets.Avec2014Video(
          path=cfg.train_dataset, transform=self._transform_train,
          num_frame=16, num_interval=1, overlap=0.5)
    else:
      dataset = tw.datasets.Avec2014Video(
          path=cfg.test_dataset, transform=self._transform_test,
          num_frame=16, num_interval=1, overlap=0.5)

    # build data loader
    if phase == tw.phase.train:
      return torch.utils.data.DataLoader(
          dataset=dataset,
          batch_size=cfg.train_batchsize,
          shuffle=True,
          num_workers=8,
          collate_fn=tw.datasets.SampleCollator(),
          pin_memory=False,
          drop_last=True)

    else:
      return torch.utils.data.DataLoader(
          dataset=dataset,
          batch_size=cfg.test_batchsize,
          shuffle=False,
          num_workers=4,
          collate_fn=tw.datasets.SampleCollator(),
          pin_memory=False,
          drop_last=False)

    raise NotImplementedError

  def _build_optim(self, model: nn.Module):
    """build optimizer
    """
    cfg = self.Config
    return torch.optim.Adam([{'params': model.parameters(), 'lr': cfg.train_lr}])

  def _build_model(self):
    """build model
    """
    cfg = self.Config

    if cfg.model_name == 'c3d':
      backbone = tw.models.c3d.C3D(num_classes=1)
      classifier = nn.Sequential(
          nn.Dropout(0.5),
          nn.Linear(512, 1))
      feature_dim = 512

    elif cfg.model_name == 'i3d':
      from tw.models.backbone3d.i3d import Unit3Dpy
      backbone = tw.models.i3d.I3D(num_classes=1, dropout_keep_prob=0.5)
      classifier = nn.Sequential(
          nn.Dropout(0.5),
          Unit3Dpy(in_channels=1024, out_channels=1, kernel_size=(1, 1, 1),
                   activation=None, use_bias=True, use_bn=False))
      feature_dim = 1024

    elif cfg.model_name == 'r3d18':
      backbone = tw.models.r3d.R3D18(num_classes=1)
    elif cfg.model_name == 'r3d34':
      backbone = tw.models.r3d.R3D34(num_classes=1)
    elif cfg.model_name == 'r2plus1d18':
      backbone = tw.models.r2plus1d.R2Plus1D18(num_classes=1)
    elif cfg.model_name == 'r2plus1d34':
      backbone = tw.models.r2plus1d.R2Plus1D34(num_classes=1)
    elif cfg.model_name == 'p3d63':
      backbone = tw.models.p3d.P3D63(num_classes=1)
    elif cfg.model_name == 'p3d131':
      backbone = tw.models.p3d.P3D131(num_classes=1)
    elif cfg.model_name == 'p3d199':
      backbone = tw.models.p3d.P3D199(num_classes=1)
    else:
      raise NotImplementedError(cfg.model_name)

    # predictor
    predictor = PredictorNet(1, feature_dim, 128)

    # to device
    model = ModelWrapper(backbone, classifier, predictor)
    model.to(cfg.device)

    return model

  def _dump(self):
    """dump current checkpoint
    """
    cfg = self.Config
    path = f'{cfg.root}/model.epoch-{self.Epoch}.step-{self.Step}.pth'

    torch.save({
        'state_dict': self.Model.state_dict(),
        'global_step': self.Step,
        'global_epoch': self.Epoch,
        'optimizer': self.Optim.state_dict(),
    }, path)

    logger.info(f'Model has saved in {path}')

  def _load(self):
    """Loading mode
    """
    cfg = self.Config

    logger.net('Loading model source: {}'.format(cfg.model_source))
    ckpt = tw.checkpoint.load(cfg.model_path)

    if cfg.model_source is None:
      tw.checkpoint.load_matched_state_dict(self.Model, ckpt)

    elif cfg.model_source == 'tw':
      tw.checkpoint.load_matched_state_dict(self.Model, ckpt['state_dict'])
      if self.Optim is not None:
        self.Optim.load_state_dict(ckpt['optimizer'])
        self.Step = ckpt['global_step']
        self.Epoch = ckpt['global_epoch']

    elif cfg.model_source == 'vanilla':
      tw.checkpoint.load_matched_state_dict(self.Model, ckpt['state_dict'])

    elif cfg.model_source == 'torchvision':
      tw.checkpoint.load_matched_state_dict(self.Model, ckpt)

    else:
      raise NotImplementedError

  def _inference(self, inputs):
    """inference phase we only use stem pipeline.

    Args:
        inputs ([type]): [N, C, D, H, W]

    Raises:
        NotImplementedError: [description]
    """
    cfg = self.Config
    device = self.Config.device

    if cfg.model_name == 'c3d':
      logits = self.Model.backbone(inputs).flatten()
      features = self.Model.backbone.endpoints['fc7']  # [8, 512]
      logits = self.Model.classifier(features).squeeze()

    elif cfg.model_name == 'i3d':
      self.Model.backbone(inputs)
      features = self.Model.backbone.endpoints['gap']  # [8, 1024, 2, 1, 1]
      logits = self.Model.classifier(features).squeeze().mean(1)

    else:
      raise NotImplementedError(cfg.model_name)

    return features, logits

  def _optimize(self, inputs, labels):
    """[summary]

    Args:
        inputs ([type]): [description]
        labels ([type]): [description]

    Raises:
        NotImplementedError: [description]
    """

    cfg = self.Config
    device = self.Config.device

    # inference result
    features, logits = self._inference(inputs)

    # losses
    losses = {
        'loss_mse': self.loss_mse(logits, labels.float()),
        'loss_ebm': self.loss_ebm(self.Model.predictor, features, labels.float())
    }

    return losses

  def _train(self, **kwargs):
    """train routine
    """

    # build stat
    cfg = self.Config
    device = self.Config.device
    init_step = self.Step
    stat = tw.stat.AverSet()
    start_time = tw.timer.tic()

    # build train dataset
    train_loader = self._build_dataset(tw.phase.train)
    total_step = len(train_loader) * cfg.train_epoch

    # build test dataset
    if self.Master:
      test_loader = self._build_dataset(tw.phase.test)

    # print trainable parameters
    tw.checkpoint.print_trainable_variables(self.Model)

    # criteria
    self.loss_mse = torch.nn.MSELoss(reduction='mean')
    self.loss_ebm = tw.nn.EBMLoss(num_samples=1024, gmm_stds=[[4.0, 2.0, 1.0]], method='mcis_hybrid')

    # training
    while self.Epoch < cfg.train_epoch:

      self.Epoch += 1
      self.Model.train()

      for samples in train_loader:

        # -------------------------------------------------------------------------
        # prepare data
        # -------------------------------------------------------------------------
        self.Step += 1

        # convert data into tensor
        videos, targets = [], []
        for sample in samples:
          videos.append(sample[0].bin.to(device))
          targets.append(sample[0].label)
        videos = torch.stack(videos, dim=0).float().to(device)
        targets = torch.tensor(targets).long().to(device)

        # -------------------------------------------------------------------------
        # FORWARD
        # -------------------------------------------------------------------------
        losses = self._optimize(videos, targets)

        # update
        loss = sum(loss for loss in losses.values())
        self.Optim.zero_grad()
        loss.backward()
        self.Optim.step()

        # iteration stat
        losses.update({
            'loss': sum(loss for loss in losses.values()),
            'time': logger.toc(),
        })
        stat.update(losses)
        logger.tic()

        # print
        if tw.runner.reach(self.Step, cfg.log):
          eta = tw.timer.remain_eta(self.Step, total_step, start_time, init_step)
          tw.runner.log(keys=['eta'] + stat.keys() + ['lr'],
                        values=[eta] + stat.values() + [self.Optim.param_groups[0]['lr']],
                        step=self.Step,
                        epoch=self.Epoch,
                        tag='train',
                        iters_per_epoch=len(train_loader),
                        writer=self.Writer)
          stat.reset()

        if tw.runner.reach(self.Step, cfg.log_save) and self.Master:
          self._dump()

        if tw.runner.reach(self.Step, cfg.log_test) and self.Master:
          self._test(loader=test_loader)

  def _test(self, **kwargs):
    """validate after epoch
    """
    cfg = self.Config
    device = self.Config.device
    start_time = tw.timer.tic()
    total = 0

    # reset
    self.Model.eval()
    self.Evaluator.reset()

    # build dataloader
    if 'loader' in kwargs and kwargs['loader'] is not None:
      test_loader = kwargs['loader']
    else:
      test_loader = self._build_dataset(tw.phase.test)

    # create folder for every epoch
    root = tw.fs.mkdirs(f'{cfg.root}/test/epoch_{self.Epoch}_step_{self.Step}/')
    self.Evaluator.root = root

    # start
    with torch.no_grad():
      for samples in tqdm.tqdm(test_loader):
        total += len(samples)

        # -------------------------------------------------------------------
        # prepare data
        # -------------------------------------------------------------------
        videos, targets, paths = [], [], []
        for sample in samples:
          paths.append(sample[0].path[0])
          videos.append(sample[0].bin.to(device))
          targets.append(sample[0].label)
        videos = torch.stack(videos, dim=0).float().to(device)
        targets = torch.tensor(targets).long().to(device)

        # -------------------------------------------------------------------
        # FORWARD
        # -------------------------------------------------------------------
        _, outputs = self._inference(videos)

        # eval
        self.Evaluator.append([paths, targets.cpu().numpy(), outputs.cpu().numpy()])

    # stat
    reports = self.Evaluator.accumulate()
    elapsed = tw.timer.duration(start_time, tw.timer.tic())
    throughput = tw.timer.throughput(elapsed, total)
    keys = list(reports.keys()) + ['time', 'throughtput']
    vals = list(reports.values()) + [elapsed, throughput]
    tw.runner.log(keys=keys, values=vals, step=self.Step, epoch=self.Epoch, tag='val', writer=self.Writer)

  def _viz(self, **kwargs):
    raise NotImplementedError()

  def __call__(self):
    """prepare basic
    """
    cfg = self.Config

    if cfg.task == 'train':
      self._train()

    elif cfg.task == 'test':
      with torch.no_grad():
        self._test()

    elif cfg.task == 'viz':
      with torch.no_grad():
        self._viz()

    else:
      raise NotImplementedError(cfg.task)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()

  # ---------------------------------------------
  #  USED BY CONTEXT
  # ---------------------------------------------
  parser.add_argument('--task', type=str, default=None, choices=['train', 'test', 'viz'])

  # ---------------------------------------------
  #  USED BY LOGGER
  # ---------------------------------------------
  parser.add_argument('--log', type=int, default=10, help="display interval step.")
  parser.add_argument('--log-test', type=int, default=500, help="running test in terms of step.")
  parser.add_argument('--log-save', type=int, default=500, help="saveing checkpoint with interval.")

  # ---------------------------------------------
  #  USED BY MODEL-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--model-name', type=str, required=True)
  parser.add_argument('--model-path', type=str, default=None, help="loadding pretrain/last-checkpoint model.")
  parser.add_argument('--model-source', type=str, default=None)

  # ---------------------------------------------
  #  USED BY TRAIN-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--train-lr', type=float, default=0.0001, help="total learning rate across devices.")
  parser.add_argument('--train-batchsize', type=int, default=8, help="total batch size across devices.")
  parser.add_argument('--train-epoch', type=int, default=240, help="total training epochs.")
  parser.add_argument('--train-dataset', type=str, default='_datasets/depression/AVEC2014/pp_trn.txt')

  # ---------------------------------------------
  #  USED BY TEST-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--test-dataset', type=str, default='_datasets/depression/AVEC2014/pp_tst.txt')
  parser.add_argument('--test-batchsize', type=int, default=8, help="total batch size across devices.")

  tw.runner.launch(parser, DepressHybridEBM)
