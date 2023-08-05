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
"""Blind VSR

  MODE: single image -> encoder -> estimation
              |                          |----> generator -> hr -> discriminator
              ----------------------------           

"""

import os
import random
from collections import OrderedDict
import tqdm
import functools

import cv2

import torch
from torch import nn

import kornia

import tw
from tw import logger
from tw import transform as T

import vsr_base


class ClassFolderEnhance(torch.utils.data.Dataset):

  def __init__(self, path, transform, **kwargs):
    # check
    tw.fs.raise_path_not_exist(path)
    res, _ = tw.parser.parse_from_text(path, [str, str], [True, True])  # nopep8

    self.targets = {}
    for _, (image_folder, enhance_folder) in enumerate(zip(*res)):
      tag = image_folder[:-5]

      if tag not in self.targets:
        self.targets[tag] = {}

      self.targets[tag][image_folder[-4:]] = (
          [os.path.join(image_folder, f) for f in sorted(os.listdir(image_folder))],
          [os.path.join(enhance_folder, f) for f in sorted(os.listdir(enhance_folder))],
      )

    self.transform = transform
    self.keys = list(self.targets.keys())
    tw.logger.info(f'number of whole images: {len(self)}')

  def __len__(self):
    return len(self.targets)

  def __getitem__(self, idx):

    # select image sequence group
    group = self.targets[self.keys[idx]]
    p0, p1 = random.sample([i for i in range(len(group))], 2)
    v0_lr, v0_hr = group[list(group.keys())[p0]]
    v1_lr, v1_hr = group[list(group.keys())[p1]]

    # select time t in [0, 120]
    t = random.randint(0, len(v0_lr) - 1)

    img0_lr = v0_lr[t]
    img0_hr = v0_hr[t]
    img1_lr = v1_lr[t]
    img1_hr = v1_hr[t]

    img_meta = T.VideoMeta(path=[img0_lr, img1_lr])
    img_meta.load().numpy()
    enh_meta = T.VideoMeta(path=[img0_hr, img1_hr])
    enh_meta.load().numpy()
    return self.transform([img_meta, enh_meta])


class BlindVsr(vsr_base.VsrBase):

  def __init__(self, config):
    super().__init__(config)

  def _build_dataset(self, phase: tw.phase):
    """build train/val datasets
    """
    cfg = self.Config

    # build target dataset
    if phase == tw.phase.train:
      return ClassFolderEnhance(path=cfg.dataset_train, transform=self.transform_yuv_train)

    elif phase == tw.phase.val and self.Master:
      return tw.datasets.ImageEnhance(path=cfg.dataset_val, transform=self.transform_yuv_val)

    raise NotImplementedError

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

    # korina
    from kornia import augmentation as Augment
    self.random_crop = Augment.RandomCrop([64, 64], same_on_batch=True)
    self.random_flip = functools.partial(kornia.random_hflip, p=0.5)
    self.random_affine = functools.partial(kornia.random_affine, degrees=(-1, 1), translate=(0.01, 0.01))
    self.loss_contrast = torch.nn.CrossEntropyLoss()

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

        # n, c, 2, h, w
        lr_pair = torch.stack(lr, dim=0).float().to(device)
        lr = lr_pair[:, :, 0]
        hr_pair = torch.stack(hr, dim=0).float().to(device)
        hr = hr_pair[:, :, 0]

        # ---------------------------------------------------------------
        # training encoder
        # ---------------------------------------------------------------

        # positive-1
        lr_query = lr_pair[:, :, 0]
        lr_key = lr_pair[:, :, 1]

        # aug second sample
        lr_key = self.random_flip(lr_key)
        lr_key = self.random_affine(lr_key)

        # moco encoder
        _, logits, labels, feat = self.Model.netE(lr_query, lr_key)
        # print(feat.shape, lr_query.shape)

        # compute loss
        loss_cl = self.loss_contrast(logits, labels)

        if self.Epoch < 50:
          self.Optim['E'].zero_grad()
          loss_cl.backward()
          self.Optim['E'].step()

          # iter
          losses = {'loss_cl': loss_cl, 'time': logger.toc()}

        else:

          # ---------------------------------------------------------------
          # sobel gradient loss
          # ---------------------------------------------------------------

          if cfg.input_colorspace in ['RGB', 'Y']:
            weight = kornia.sobel(hr)
          elif cfg.input_colorspace in ['YUV']:
            weight = kornia.sobel(hr[:, 0].unsqueeze(dim=1))
            weight = (weight - weight.min()) / (weight.max() - weight.min())
            # print(weight.max(), weight.min(), weight.mean())
          else:
            raise NotImplementedError

          # ---------------------------------------------------------------
          # training generator
          # ---------------------------------------------------------------

          # freeze discriminator and clear generator gradients
          for p in self.Model.netD.parameters():
            p.requires_grad = False
          self.Optim['G'].zero_grad()
          self.Optim['E'].zero_grad()

          # training hr
          hr_pred = self.Model.netG(lr.detach(), feat)
          hr_pred = hr_pred + self.resize(lr, scale=2.0)

          # gan-pred
          hr_logit = self.Model.netD(hr_pred)

          # pixelwise loss
          loss_g_pix = self.loss_l1(hr_pred, hr).mean()

          # low-frequency loss
          loss_g_pix_low = (2 * self.loss_l1(hr_pred, hr) * (1 - weight)).mean()

          # feature loss
          # NOTE: perceptual loss requires inputs to be RGB in [0, 1]
          if cfg.input_colorspace == 'Y':
            l_g_percep, l_g_style = self.loss_lpips(hr_pred, hr)
          elif cfg.input_colorspace == 'YUV':
            hr_pred_rgb = T.change_colorspace(hr_pred * 255.0, src=T.COLORSPACE.BT709_FULLRANGE, dst=T.COLORSPACE.RGB) / 255.0  # nopep8
            hr_rgb = T.change_colorspace(hr * 255.0, src=T.COLORSPACE.BT709_FULLRANGE, dst=T.COLORSPACE.RGB) / 255.0  # nopep8
            l_g_percep, l_g_style = self.loss_lpips(hr_pred_rgb, hr_rgb)
          elif cfg.input_colorspace == 'RGB':
            l_g_percep, l_g_style = self.loss_lpips(hr_pred, hr)
          else:
            raise NotImplementedError(cfg.input_colorspace)

          if l_g_percep is not None:
            l_g_percep += l_g_percep
          if l_g_style is not None:
            l_g_percep += l_g_style

          # gan loss
          if self.loss_gan_type == 'gan':
            loss_g_gan = self.loss_gan(hr_logit, True)
          elif self.loss_gan_type == 'ragan':
            hr_real = self.Model.netD(hr).detach()
            loss_g_real = self.loss_gan(hr_real - hr_logit.mean(), False)
            loss_g_fake = self.loss_gan(hr_logit - hr_real.mean(), True)
            loss_g_gan = (loss_g_real + loss_g_fake) / 2.0
          else:
            raise NotImplementedError

          loss_g = 0.01 * (loss_g_pix + loss_g_pix_low) + l_g_percep + 0.005 * loss_g_gan + loss_cl
          loss_g.backward()
          self.Optim['G'].step()
          self.Optim['E'].step()

          # ---------------------------------------------------------------
          # training discriminator
          # ---------------------------------------------------------------

          for p in self.Model.netD.parameters():
            p.requires_grad = True
          self.Optim['D'].zero_grad()

          # discriminator
          hr_real = self.Model.netD(hr)
          hr_logit = self.Model.netD(hr_pred.detach())

          # gan loss
          if self.loss_gan_type == 'gan':
            loss_d_real = self.loss_gan(hr_real, True)
            loss_d_fake = self.loss_gan(hr_logit, False)
            loss_d = (loss_d_real + loss_d_fake)
          elif self.loss_gan_type == 'ragan':
            loss_d_real = self.loss_gan(hr_real - hr_logit.mean(), True)
            loss_d_fake = self.loss_gan(hr_logit - hr_real.mean(), False)
            loss_d = (loss_d_real + loss_d_fake) / 2.0
          else:
            raise NotImplementedError

          loss_d = 0.005 * loss_d
          loss_d.backward()
          self.Optim['D'].step()

          # iter
          losses = {
              'loss_g_pix_low': loss_g_pix_low,
              'loss_g_pix': loss_g_pix,
              'loss_g_percep': l_g_percep,
              'loss_g_gan': loss_g_gan,
              'loss_d_real': loss_d_real,
              'loss_d_fake': loss_d_fake,
              'loss_d': loss_d,
              'loss_cl': loss_cl,
              'loss': loss_g + loss_d,
              'time': logger.toc(),
          }

        # accumulate
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
    _, feat = self.Model.netE(img_lr, img_lr)
    img_hr = self.Model.netG(img_lr, feat)
    img_hr = img_hr + self.resize(img_lr, scale=2.0)
    return img_hr
