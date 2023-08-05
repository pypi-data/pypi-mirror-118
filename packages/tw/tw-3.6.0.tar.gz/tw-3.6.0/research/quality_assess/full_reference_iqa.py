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
"""IQA SYSTEM for evaluation a variety of quality assessment index.

  Referenced by: https://github.com/dingkeyan93/IQA-optimization

  - SSIM, MS-SSIM, CW-SSIM,
  - FSIM, VSI, GMSD,
  - NLPD, MAD,
  - VIF,
  - LPIPS, DISTS.

"""
import os
import functools
import argparse
import tqdm

import cv2
import kornia
import numpy as np

import torch
from torch import nn
from torch.utils import tensorboard

import tw
from tw import logger
from tw import transform as T

import image_assess
import models
import common


class FullReferenceIQA():

  def __init__(self, config):
    self.Config = config

    # overwrite when dist
    if self.Config.dist_size > 1:
      self.Config.device = 'cuda:{}'.format(self.Config.dist_rank)
    self.Master = True if self.Config.dist_rank == 0 else False

    # evaluation and tensorboard
    self.Writer = tensorboard.SummaryWriter(log_dir=self.Config.root)
    self.Evaluator = tw.evaluator.QualityAssessEvaluator()

    # scalar
    self.Epoch = 0
    self.Step = 0

    # models
    self.Model = self._build_model()

    # build optim
    if self.Config.task == 'train':
      self.Optim = torch.optim.Adam([{'params': self.Model.parameters(), 'lr': self.Config.train_lr}])
    else:
      self.Optim = None

    # load model and possible optimizer
    if self.Config.model_path is not None:
      self._load()

    # extend to distributed
    if self.Config.dist_size > 1:
      self.Model = torch.nn.SyncBatchNorm.convert_sync_batchnorm(self.Model)
      self.Model = torch.nn.parallel.DistributedDataParallel(self.Model, device_ids=[self.Config.dist_rank])

  def _build_model(self):
    """build iqa models
    """
    cfg = self.Config
    device = self.Config.device

    if cfg.model == 'ssim':
      model = image_assess.SSIM()
    elif cfg.model == 'ms_ssim':
      model = image_assess.MS_SSIM()
    elif cfg.model == 'cw_ssim':
      model = image_assess.CW_SSIM()
    elif cfg.model == 'gmsd':
      model = image_assess.GMSD()
    elif cfg.model == 'nlpd':
      model = image_assess.NLPD()
    elif cfg.model == 'fsim':
      model = image_assess.FSIM()
    elif cfg.model == 'vsi':
      model = image_assess.VSI()
    elif cfg.model == 'vif':
      model = image_assess.VIF()
    elif cfg.model == 'vifs':
      model = image_assess.VIFs()
    elif cfg.model == 'mad':
      model = image_assess.MAD()
    elif cfg.model == 'lpips':
      model = image_assess.LPIPSvgg()
    elif cfg.model == 'dists':
      model = image_assess.DISTS()
    elif cfg.model == 'psnr':
      model = image_assess.PSNR()
    else:
      raise NotImplementedError(cfg.model)

    model.to(device)
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
      content = tw.checkpoint.replace_prefix(ckpt['state_dict'], 'module.', '')
      tw.checkpoint.load_matched_state_dict(self.Model, content)

      if cfg.task == 'train' and self.Optim is not None:
        self.Optim.load_state_dict(ckpt['optimizer'])

      if 'global_step' in ckpt:
        self.Step = ckpt['global_step']

      if 'global_epoch' in ckpt:
        self.Epoch = ckpt['global_epoch']

    elif cfg.model_source == 'vanilla':
      tw.checkpoint.load_matched_state_dict(self.Model, ckpt['state_dict'])

    else:
      raise NotImplementedError(cfg.model_source)

  def _val(self, **kwargs):
    """val (ref, distort)"""
    cfg = self.Config
    device = self.Config.device
    start_time = tw.timer.tic()
    total = 0

    # reset
    self.Model.eval()
    self.Evaluator.reset()

    # build dataloader
    if 'loader' in kwargs and kwargs['loader'] is not None:
      loader = kwargs['loader']
    else:
      loader = common.build_dataset(cfg, tw.phase.val, blind_mode=False)

    # create folder for every epoch
    root = tw.fs.mkdirs(f'{cfg.root}/val/epoch_{self.Epoch}_step_{self.Step}/')
    result_path = os.path.join(root, 'prediction.txt')
    result = open(result_path, 'w')

    # start
    with torch.no_grad():

      for refs, distorts, labels, distort_paths, ref_paths in tqdm.tqdm(loader):

        total += refs.size(0)

        refs = refs.float().to(device, non_blocking=True)
        distorts = distorts.float().to(device, non_blocking=True)
        labels = labels.float()

        # inference
        if refs.ndim == 5:
          preds = []
          for ref, distort in zip(refs, distorts):
            pred = self.Model(ref, distort, as_loss=False)
            preds.append(pred.mean())
          preds = torch.tensor(preds)
        else:
          preds = self.Model(ref, distort, as_loss=False)
          if preds.ndim == 0:
            preds = preds.reshape([-1])

        # write to file
        for rp, dp, label, pred in zip(ref_paths, distort_paths, labels, preds):
          result.write('{} {} {} {}\n'.format(rp, dp, label.item(), pred.item()))

        # append
        self.Evaluator.append(preds, labels)

    # stat
    result.close()
    reports = self.Evaluator.accumulate()
    elapsed = tw.timer.duration(start_time, tw.timer.tic())
    throughput = tw.timer.throughput(elapsed, total)
    keys = list(reports.keys()) + ['time', 'throughtput']
    vals = list(reports.values()) + [elapsed, throughput]
    tw.runner.log(keys=keys, values=vals, step=self.Step, epoch=self.Epoch, tag='val', writer=self.Writer)
    tw.logger.val('Result has been saved in {}'.format(result_path))

  def _test(self, **kwargs):
    """test (ref, distort)"""
    cfg = self.Config
    device = self.Config.device
    start_time = tw.timer.tic()
    total = 0

    # reset
    self.Model.eval()

    # build dataloader
    if 'loader' in kwargs and kwargs['loader'] is not None:
      loader = kwargs['loader']
    else:
      loader = common.build_dataset(cfg, tw.phase.test, blind_mode=False)

    # create folder for every epoch
    root = tw.fs.mkdirs(f'{cfg.root}/test/epoch_{self.Epoch}_step_{self.Step}/')
    result = open(os.path.join(root, 'prediction.txt'), 'w')

    # start
    with torch.no_grad():

      for ref, distort, labels, paths in tqdm.tqdm(loader):

        total += ref.size(0)

        ref = ref.float().to(device, non_blocking=True)
        distort = distort.float().to(device, non_blocking=True)

        # inference
        preds = self.Model(ref, distort, as_loss=False)

        # write to file
        for path, pred in zip(paths, preds):
          result.write('{} {} {}\n'.format(path, pred.item()))

    # stat
    result.close()
    elapsed = tw.timer.duration(start_time, tw.timer.tic())
    throughput = tw.timer.throughput(elapsed, total)
    tw.runner.log(keys=['time', 'throughtput'],
                  values=[elapsed, throughput],
                  step=self.Step,
                  epoch=self.Epoch,
                  tag='test',
                  writer=self.Writer)

  def __call__(self):
    """prepare basic
    """
    cfg = self.Config

    if cfg.task == 'train':
      self._train()

    elif cfg.task == 'val':
      with torch.no_grad():
        self._val()

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
  common.build_argparse(parser)
  args, _ = parser.parse_known_args()
  tw.runner.launch(parser, FullReferenceIQA)
