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
"""Likee VSR

  MODE: single image -> network -> single image

"""
import os
import cv2
import tqdm

import torch
from torch import nn

import tw
from tw import logger
from tw import transform as T

import vsr_base


class LikeeVsr(vsr_base.VsrBase):

  def __init__(self, config):
    super().__init__(config)

  def _train(self, **kwargs):
    """train routine
    """
    cfg = self.Config
    device = self.Config.device
    init_step = self.Step
    stat = tw.stat.AverSet()
    start_time = tw.timer.tic()

    # build train dataset
    train_loader = self._build_dataloader(tw.phase.train, self._build_dataset(tw.phase.train))
    total_step = len(train_loader) * cfg.train_epoch

    # build val dataset
    if self.Master:
      val_loader = self._build_dataloader(tw.phase.val, self._build_dataset(tw.phase.val))

    # print trainable parameters
    tw.checkpoint.print_trainable_variables(self.Model)

    # losses
    self.loss_l1 = nn.L1Loss().to(device)

    # training
    while self.Epoch < cfg.train_epoch:

      self.Epoch += 1
      self.Model.train()

      for samples in train_loader:

        # prepare data
        self.Step += 1

        # convert data into tensor
        lr, hr = [], []
        for sample in samples:
          if cfg.input_colorspace in ['RGB', 'YUV']:
            lr.append(sample[0].bin.float().to(device))
            hr.append(sample[1].bin.float().to(device))
          elif cfg.input_colorspace in ['Y']:
            lr.append(sample[0].bin[0][None].float().to(device))
            hr.append(sample[1].bin[0][None].float().to(device))
          else:
            raise NotImplementedError(cfg.input_colorspace)
        lr = torch.stack(lr, dim=0).float().to(device)
        hr = torch.stack(hr, dim=0).float().to(device)

        # forward
        hr_pred = self.Model.netG(lr)
        hr_pred = hr_pred + self.resize(lr, scale=2.0)

        # compute loss
        losses = {
            'loss_pixel': self.loss_l1(hr_pred, hr).mean(),
        }

        # accumulate
        loss = sum(loss for loss in losses.values())
        self.Optim['G'].zero_grad()
        loss.backward()
        self.Optim['G'].step()

        # iter
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
                        values=[eta] + stat.values() + [self.Optim['G'].param_groups[0]['lr']],
                        step=self.Step,
                        epoch=self.Epoch,
                        tag='train',
                        iters_per_epoch=len(train_loader),
                        writer=self.Writer)
          stat.reset()

      if tw.runner.reach(self.Epoch, cfg.log_save) and self.Master:
        self._dump()

      if tw.runner.reach(self.Epoch, cfg.log_val) and self.Master:
        self._val(loader=val_loader)
      
      if tw.runner.reach(self.Epoch, cfg.log_test) and self.Master:
        self._test()

  def _inference(self, img_lr, **kwargs):
    img_hr = self.Model.netG(img_lr)
    img_hr = img_hr + self.resize(img_lr, scale=2.0)
    return img_hr
