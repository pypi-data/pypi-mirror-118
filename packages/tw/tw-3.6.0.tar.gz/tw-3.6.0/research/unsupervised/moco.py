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
r"""MoCo-v2:
"""
import warnings  # nopep8
warnings.filterwarnings("ignore")  # nopep8

import argparse
import os
import tqdm

import cv2
import kornia

import torch
from torch import nn

from torch.utils import tensorboard

import tw
from tw import logger
from tw import transform as T
from tw.transform import functional as F

#!<----------------------------------------------------------------------------
#!< Models
#!<----------------------------------------------------------------------------


class SimpleEncoder(nn.Module):

  def __init__(self, in_channels=1, out_channels=32):
    super(SimpleEncoder, self).__init__()

    self.E = nn.Sequential(
        nn.Conv2d(in_channels, 8, kernel_size=3, padding=1),
        nn.BatchNorm2d(8),
        nn.LeakyReLU(0.1, True),
        nn.Conv2d(8, 8, kernel_size=3, padding=1),
        nn.BatchNorm2d(8),
        nn.LeakyReLU(0.1, True),
        nn.Conv2d(8, 16, kernel_size=3, stride=2, padding=1),
        nn.BatchNorm2d(16),
        nn.LeakyReLU(0.1, True),
        nn.Conv2d(16, 16, kernel_size=3, padding=1),
        nn.BatchNorm2d(16),
        nn.LeakyReLU(0.1, True),
        nn.Conv2d(16, 32, kernel_size=3, stride=2, padding=1),
        nn.BatchNorm2d(32),
        nn.LeakyReLU(0.1, True),
        nn.Conv2d(32, out_channels, kernel_size=3, padding=1),
        nn.BatchNorm2d(out_channels),
        nn.LeakyReLU(0.1, True),
        nn.AdaptiveAvgPool2d(1))

    self.mlp = nn.Sequential(
        nn.Linear(out_channels, out_channels),
        nn.LeakyReLU(0.1, True),
        nn.Linear(out_channels, out_channels))

  def forward(self, x):
    fea = self.E(x).squeeze(-1).squeeze(-1)
    out = self.mlp(fea)
    return fea, out


class MoCoWrapper(nn.Module):

  def __init__(self, Encoder, channels=32, queue_size=32):
    super(MoCoWrapper, self).__init__()
    self.E = tw.models.moco.MoCo(Encoder,
                                 dim=channels,
                                 K=queue_size * channels,
                                 m=0.999,
                                 T=0.07)

  def forward(self, x_query, x_key):
    if self.training:
      return self.E(x_query, x_key)  # fea, logits, labels
    else:
      return self.E(x_query, None)

#!<----------------------------------------------------------------------------
#!< Pipeline
#!<----------------------------------------------------------------------------


class MoCo():

  def __init__(self, config):
    """config
    """
    self.Config = config

    # overwrite when dist
    if self.Config.dist_size > 1:
      self.Config.device = 'cuda:{}'.format(self.Config.dist_rank)
    self.Master = True if self.Config.dist_rank == 0 else False

    # evaluation and tensorboard
    # self.Evaluator = tw.evaluator.ImageSimilarityEvaluator(use_psnr=True, use_ssim=True, use_lpips=True)
    # self.Evaluator.to(self.Config.device)
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
      model = torch.nn.SyncBatchNorm.convert_sync_batchnorm(model)
      model = torch.nn.parallel.DistributedDataParallel(model, device_ids=[self.Config.dist_rank])

  def _load(self):
    """Loading mode"""
    cfg = self.Config

    logger.net('Loading model source: {}'.format(cfg.model_source))
    ckpt = tw.checkpoint.load(cfg.model_path)

    if cfg.model_source is None:
      tw.checkpoint.load_matched_state_dict(self.Model, ckpt)

    elif cfg.model_source == 'tw':
      content = tw.checkpoint.replace_prefix(ckpt['state_dict'], 'module.', '')
      tw.checkpoint.load_matched_state_dict(self.Model, content)

      if cfg.task == 'train':
        self.Optim.load_state_dict(ckpt['optimizer'][k])

      if 'global_step' in ckpt:
        self.Step = ckpt['global_step']

      if 'global_epoch' in ckpt:
        self.Epoch = ckpt['global_epoch']

    elif cfg.model_source == 'vanilla':
      tw.checkpoint.load_matched_state_dict(self.Model, ckpt['state_dict'])

    else:
      raise NotImplementedError(cfg.model_source)

  def _dump(self):
    """dump current checkpoint"""
    cfg = self.Config

    path = f'{cfg.root}/model.epoch-{self.Epoch}.step-{self.Step}.pth'
    torch.save({
        'state_dict': self.Model.state_dict(),
        'global_step': self.Step,
        'global_epoch': self.Epoch,
        'optimizer': self.Optim.state_dict(),
    }, path)

    logger.info(f'Model has saved in {path}')

  def _build_model(self):
    """build models"""
    cfg = self.Config

    if cfg.model_encoder == 'simple':
      model = MoCoWrapper(SimpleEncoder, channels=32, queue_size=32)

    else:
      raise NotImplementedError(cfg.model_encoder)

    model.to(cfg.device)
    return model

  def _build_dataset(self, phase: tw.phase):
    """self-supervised using a image as input to learn low-level image info
    """
    cfg = self.Config

    def transform_yuv_train(metas):
      F.change_colorspace(metas, T.COLORSPACE.BGR, T.COLORSPACE.BT709_FULLRANGE)
      F.to_tensor(metas, scale=255.0)

      return metas

    def transform_yuv_val(metas):
      F.change_colorspace(metas, T.COLORSPACE.BGR, T.COLORSPACE.BT709_FULLRANGE)
      F.to_tensor(metas, scale=255.0)

    # build target dataset
    if phase == tw.phase.train:
      dataset = tw.datasets.ImagesDataset(path=cfg.dataset_train, transform=transform_yuv_train)

    elif phase == tw.phase.val and self.Master:
      dataset = tw.datasets.ImageEnhance(path=cfg.dataset_val, transform=transform_yuv_val)

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

    elif phase == tw.phase.val:
      return torch.utils.data.DataLoader(
          dataset=dataset,
          batch_size=cfg.val_batchsize,
          shuffle=False,
          num_workers=4,
          collate_fn=tw.datasets.SampleCollator(),
          pin_memory=False,
          drop_last=False)

    raise NotImplementedError

  def _build_optim(self, model: nn.Module):
    """build optimizer"""
    cfg = self.Config
    optim = {}

    if cfg.train_optimizer == 'adam':
      optim = torch.optim.Adam([{'params': model.parameters(), 'lr': cfg.train_lr}])

    elif cfg.train_optimizer == 'sgd':
      optim = torch.optim.SGD([{'params': model.parameters(), 'lr': cfg.train_lr, 'momentum': 0.9}])

    else:
      raise NotImplementedError(cfg.train_optimizer)

    return optim

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

    # build val dataset
    if self.Master:
      val_loader = self._build_dataset(tw.phase.val)

    # print trainable parameters
    tw.checkpoint.print_trainable_variables(self.Model)

    # losses
    self.loss_contrast = torch.nn.CrossEntropyLoss()

    # training
    while self.Epoch < cfg.train_epoch:

      self.Epoch += 1
      self.Model.train()

      for samples in train_loader:

        # --------------------------------------------------------------------
        # prepare data
        # --------------------------------------------------------------------
        self.Step += 1

        # convert data into tensor
        inputs = []
        for sample in samples:
          inputs.append(sample[0].bin[0][None].float().to(device))

        # [bs, c, h, w] for image
        inputs = torch.stack(inputs, dim=0).float().to(device)

        # augmentation
        inputs_k = kornia.random_hflip(inputs, p=0.5)
        inputs_k = kornia.random_affine(inputs_k, degrees=(-1, 1), translate=(0.01, 0.01))

        # --------------------------------------------------------------------
        # FORWARD
        # --------------------------------------------------------------------

        feat, logits, labels = self.Model(inputs, inputs_k)

        losses = {'loss_cl': self.loss_contrast(logits, labels)}

        # accumulate
        loss = sum(loss for loss in losses.values())
        self.Optim.zero_grad()
        loss.backward()
        self.Optim.step()

        # --------------------------------------------------------------------
        # ITER
        # --------------------------------------------------------------------
        losses.update({
            'loss': sum(loss for loss in losses.values()),
            'time': logger.toc(),
        })
        stat.update(losses)
        logger.tic()

        # --------------------------------------------------------------------
        # PRINT
        # --------------------------------------------------------------------
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

      if tw.runner.reach(self.Epoch, cfg.log_save) and self.Master:
        self._dump()

  def _viz(self, **kwargs):
    """ visualize """
    cfg = self.Config
    device = cfg.device
    images, _ = tw.media.collect(cfg.viz_input)

    # visualize during training
    if 'root' in kwargs:
      viz_output = kwargs['root']
    else:
      viz_output = cfg.viz_output

    # mkdir
    if not os.path.exists(viz_output):
      os.makedirs(viz_output)

    # set state
    self.Model.eval()

    results = {}

    # process images
    for filepath in tqdm.tqdm(sorted(images)):

      # convert image to tensor
      raw = cv2.imread(filepath)  # .astype('float')

      # inference super resolution
      img = F._rgb_to_yuv_bt709_videorange(raw, True)  # [h, w, c]
      img = torch.from_numpy(img).float().to(device) / 255.0
      img = img.permute(2, 0, 1)  # [0, 1]
      img_y = img[0].unsqueeze(0).unsqueeze(0)  # select Y channel

      # inference
      feat = self.Model(img_y, img_y)
      results[filepath] = feat

    if os.path.isdir(viz_output):
      torch.save(results, os.path.join(viz_output, os.path.basename(cfg.viz_input) + '.pth'))
    else:
      torch.save(results, viz_output)

  def __call__(self):
    """prepare basic
    """
    cfg = self.Config

    if cfg.task == 'train':
      self._train()

    elif cfg.task == 'val':
      with torch.no_grad():
        self._val()

    elif cfg.task == 'viz':
      with torch.no_grad():
        self._viz()

    elif cfg.task == 'onnx':
      with torch.no_grad():
        self._onnx()

    elif cfg.task == 'trt':
      with torch.no_grad():
        self._tensorrt()

    else:
      raise NotImplementedError(cfg.task)


if __name__ == "__main__":

  parser = argparse.ArgumentParser()

  # ---------------------------------------------
  #  USED BY COMMON
  # ---------------------------------------------
  parser.add_argument('--task', type=str, default=None, choices=['train', 'val', 'viz', 'onnx', 'trt'])
  parser.add_argument('--dataset-train', type=str, default='_datasets/BigoliveGameSR/PAPER.protocal.txt')
  parser.add_argument('--dataset-val', type=str, default='_datasets/BigoliveGameSR/PAPER.protocal.txt')

  # ---------------------------------------------
  #  USED BY LOGGER
  # ---------------------------------------------
  parser.add_argument('--log', type=int, default=10, help="display interval step.")
  parser.add_argument('--log-val', type=int, default=-1, help="running validation in terms of step.")
  parser.add_argument('--log-test', type=int, default=-1, help="running test in terms of step.")
  parser.add_argument('--log-save', type=int, default=1, help="saveing checkpoint with interval.")

  # ---------------------------------------------
  #  USED BY MODEL-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--model-encoder', type=str, default=None)
  parser.add_argument('--model-path', type=str, default=None, help="loadding pretrain/last-checkpoint model.")
  parser.add_argument('--model-source', type=str, default=None)

  # ---------------------------------------------
  #  USED BY TRAIN-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--train-lr', type=float, default=0.0001, help="total learning rate across devices.")
  parser.add_argument('--train-batchsize', type=int, default=4, help="total batch size across devices.")
  parser.add_argument('--train-epoch', type=int, default=240, help="total training epochs.")
  parser.add_argument('--train-optimizer', type=str, default='sgd', choices=['sgd', 'adam'], help="training optimizer.")

  # ---------------------------------------------
  #  USED BY VAL-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--val-batchsize', type=int, default=1, help="total batch size across devices.")

  # ---------------------------------------------
  #  USED BY VIZ-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--viz-input', type=str, help='input path could be a folder/filepath.')
  parser.add_argument('--viz-output', type=str, help='output path should be a folder path.')

  tw.runner.launch(parser, MoCo)
