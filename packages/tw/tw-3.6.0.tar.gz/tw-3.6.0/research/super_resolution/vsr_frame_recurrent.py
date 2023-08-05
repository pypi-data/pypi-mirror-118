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
"""Frame-Recurrent Vsr
"""
import os
from collections import OrderedDict
import tqdm

import cv2

import torch
from torch import nn

import tw
from tw import logger
from tw import transform as T

import vsr_base


class FrVsr(vsr_base.VsrBase):

  def __init__(self, config):
    super().__init__(config)
    self.segment = 8
    self.last_hr = None

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
    self.loss_l2 = nn.MSELoss().to(device)
    # self.loss_lpips = tw.nn.LPIPSLoss(net='vgg').to(device)
    self.loss_gan_type = 'ragan'
    self.loss_gan = tw.nn.GeneralGanLoss(gan_type=self.loss_gan_type).to(device)

    perceptual_opt = OrderedDict(
        [('layer_weights', OrderedDict([('conv5_4', 1)])),
         ('vgg_type', 'vgg19'),
         ('use_input_norm', True),
         ('range_norm', False),
         ('perceptual_weight', 1.0),
         ('style_weight', 0),
         ('criterion', 'l1')])
    self.loss_lpips = tw.nn.PerceptualLoss(**perceptual_opt).to(device)

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
          lr.append(sample[0].bin[0][None].float().to(device))
          hr.append(sample[1].bin[0][None].float().to(device))
        lr = torch.stack(lr, dim=0).float().to(device)  # n, c, d, h, w
        hr = torch.stack(hr, dim=0).float().to(device)  # n, c, d, h, w

        n, c, d, h, w = lr.shape
        last_hr = torch.zeros(n, c, 2 * h, 2 * w).to(device)

        # ---------------------------------------------------------------
        # training generator
        # ---------------------------------------------------------------

        # freeze discriminator and clear generator gradients
        for p in self.Model.netD.parameters():
          p.requires_grad = False
        self.Optim['G'].zero_grad()

        loss_g_pix, l_g_percep, loss_g_gan, hr_preds = 0, 0, 0, []

        for i in range(d):
          # select lr and hr
          lr_i = lr[:, :, i].contiguous()
          hr_i = hr[:, :, i].contiguous()

          # training hr
          hr_pred = self.Model.netG(lr_i.detach(), last_hr)
          last_hr = hr_pred.clone()

          hr_pred = hr_pred + self.resize(lr_i, scale=2.0)
          hr_pred = hr_pred.contiguous()
          hr_preds.append(hr_pred)

          # gan-pred
          hr_logit = self.Model.netD(hr_pred)

          # pixelwise loss
          loss_g_pix += self.loss_l1(hr_pred, hr_i).mean()

          # feature loss
          percep, style = self.loss_lpips(hr_pred, hr_i)
          if percep is not None:
            l_g_percep += percep
          if style is not None:
            l_g_percep += style

          # gan loss
          if self.loss_gan_type == 'gan':
            loss_g_gan += self.loss_gan(hr_logit, True)
          elif self.loss_gan_type == 'ragan':
            hr_real = self.Model.netD(hr_i).detach()
            loss_g_real = self.loss_gan(hr_real - hr_logit.mean(), False)
            loss_g_fake = self.loss_gan(hr_logit - hr_real.mean(), True)
            loss_g_gan += (loss_g_real + loss_g_fake) / 2.0
          else:
            raise NotImplementedError

        loss_g = (0.01 * loss_g_pix + l_g_percep + 0.005 * loss_g_gan) / self.segment
        loss_g.backward()
        self.Optim['G'].step()

        # ---------------------------------------------------------------
        # training discriminator
        # ---------------------------------------------------------------
        for p in self.Model.netD.parameters():
          p.requires_grad = True
        self.Optim['D'].zero_grad()

        loss_d = 0
        for i in range(d):
          # select lr and hr
          lr_i = lr[:, :, i].contiguous()
          hr_i = hr[:, :, i].contiguous()
          hr_pred = hr_preds[i]

          # discriminator
          hr_real = self.Model.netD(hr_i)
          hr_logit = self.Model.netD(hr_pred.detach())

          # gan loss
          if self.loss_gan_type == 'gan':
            loss_d_real = self.loss_gan(hr_real, True)
            loss_d_fake = self.loss_gan(hr_logit, False)
            loss_d += (loss_d_real + loss_d_fake)
          elif self.loss_gan_type == 'ragan':
            loss_d_real = self.loss_gan(hr_real - hr_logit.mean(), True)
            loss_d_fake = self.loss_gan(hr_logit - hr_real.mean(), False)
            loss_d += (loss_d_real + loss_d_fake) / 2.0
          else:
            raise NotImplementedError

        loss_d = (0.005 * loss_d) / self.segment
        loss_d.backward()
        self.Optim['D'].step()

        # iter
        losses = {
            'loss_g_pix': loss_g_pix,
            'loss_g_percep': l_g_percep,
            'loss_g_gan': loss_g_gan,
            'loss_d_real': loss_d_real,
            'loss_d_fake': loss_d_fake,
            'loss_d': loss_d,
            'loss': loss_g + loss_d,
            'time': logger.toc(),
        }
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
        self.last_hr = None
        self._test()

  def _inference(self, img_lr, **kwargs):

    n, c, h, w = img_lr.shape

    if self.last_hr is None or img_lr.shape[-2:] != self.last_hr[-2:]:
      self.last_hr = torch.zeros(n, c, 2 * h, 2 * w).to(img_lr.device)

    img_hr = self.Model.netG(img_lr, self.last_hr)
    self.last_hr = img_hr.clone()

    img_hr = img_hr + self.resize(img_lr, scale=2.0)

    return img_hr
