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


def transform_train(metas):
  T.random_crop(metas, 224, 224)
  T.random_hflip(metas, 0.5)
  T.truncated_standardize(metas)
  T.to_tensor(metas)
  return metas


def transform_test(metas):
  T.center_crop(metas, 224, 224)
  T.truncated_standardize(metas)
  T.to_tensor(metas)
  return metas


class Depress2D():

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

  def _build_dataset(self, phase: tw.phase):
    """build train/val datasets
    """
    cfg = self.Config

    # build target datasets
    if phase == tw.phase.train:
      dataset = tw.datasets.Avec2014(path=cfg.train_dataset, transform=transform_train)
    else:
      dataset = tw.datasets.Avec2014(path=cfg.test_dataset, transform=transform_test)

    # build data loader
    if phase == tw.phase.train:
      return torch.utils.data.DataLoader(
          dataset=dataset,
          batch_size=cfg.train_batchsize,
          shuffle=True,
          num_workers=8,
          collate_fn=tw.datasets.SampleCollator(),
          pin_memory=True,
          drop_last=True)

    else:
      return torch.utils.data.DataLoader(
          dataset=dataset,
          batch_size=cfg.test_batchsize,
          shuffle=False,
          num_workers=8,
          collate_fn=tw.datasets.SampleCollator(),
          pin_memory=False,
          drop_last=False)

    raise NotImplementedError

  def _build_optim(self, model: nn.Module):
    """build optimizer
    """
    cfg = self.Config

    if cfg.train_optimizer == 'adam':
      return torch.optim.Adam([{'params': model.parameters(), 'lr': cfg.train_lr}])

    elif cfg.train_optimizer == 'sgd':
      return torch.optim.SGD([{'params': model.parameters(), 'lr': cfg.train_lr, 'momentum': 0.9}])

    else:
      raise NotImplementedError(cfg.train_optimizer)

  def _build_model(self):
    """build model
    """
    cfg = self.Config

    if cfg.model_name == 'resnet50':
      model = tw.models.resnet_tf.resnet50(num_classes=1)
    elif cfg.model_name == 'mobilenet_v2':
      model = tw.models.mobilenet_v2.mobilenet_v2(num_classes=1)
    else:
      raise NotImplementedError(cfg.model_name)

    # to device
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
    criteria = torch.nn.MSELoss(reduction='mean')

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
        images, targets = [], []
        for sample in samples:
          images.append(sample[0].bin.to(device))
          targets.append(sample[0].label)
        images = torch.stack(images, dim=0).float().to(device)
        targets = torch.tensor(targets).long().to(device)

        # -------------------------------------------------------------------------
        # FORWARD
        # -------------------------------------------------------------------------
        outputs = self.Model(images)

        # losses
        losses = {'loss_mse': criteria(outputs.flatten(), targets.float())}

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
        images, targets, paths = [], [], []
        for sample in samples:
          paths.append(sample[0].path)
          images.append(sample[0].bin.to(device))
          targets.append(sample[0].label)
        images = torch.stack(images, dim=0).float().to(device)
        targets = torch.tensor(targets).long().to(device)

        # -------------------------------------------------------------------
        # FORWARD
        # -------------------------------------------------------------------
        outputs = self.Model(images)

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
  parser.add_argument('--train-lr', type=float, default=0.001, help="total learning rate across devices.")
  parser.add_argument('--train-batchsize', type=int, default=32, help="total batch size across devices.")
  parser.add_argument('--train-epoch', type=int, default=240, help="total training epochs.")
  parser.add_argument('--train-optimizer', type=str, default='adam', choices=['sgd', 'adam'], help="optimizer.")
  parser.add_argument('--train-dataset', type=str, default='_datasets/AVEC2014/pp_trn.txt')

  # ---------------------------------------------
  #  USED BY TEST-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--test-dataset', type=str, default='_datasets/AVEC2014/pp_tst.txt')
  parser.add_argument('--test-batchsize', type=int, default=8, help="total batch size across devices.")

  tw.runner.launch(parser, Depress2D)
