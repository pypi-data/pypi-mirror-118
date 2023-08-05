# Copyright 2017 The KaiJIN Authors. All Rights Reserved.
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
r"""Background Matting: Based on https://github.com/PeterL1n/BackgroundMattingV2
"""

import os
import argparse
import tqdm
import random

# torch 1.4 = 0.2.2
# torch 1.6 = latest
import kornia

from PIL import Image

import torch
from torch import nn
from torch.utils import tensorboard
from torchvision import transforms as tvt
from torchvision.transforms import functional as tvf

import tw
from tw import logger
from tw import transform as T


class BackgroundMattingV2():

  def __init__(self, config):
    """init
    """
    self.Config = config

    # overwrite when dist
    if self.Config.dist_size > 1:
      self.Config.device = 'cuda:{}'.format(self.Config.dist_rank)
    self.Master = True if self.Config.dist_rank == 0 else False

    # evaluation and tensorboard
    self.Writer = tensorboard.SummaryWriter(log_dir=self.Config.root)

    # scalar
    self.Epoch = 0
    self.Step = 0

    # models
    self.Model = self._build_model()
    self.Model.to(self.Config.device)

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

  def _split_compression(self, tensor):
    """Assume tensor[n,c(RGB/RGBA),h,w]
    """
    diff = (tensor[0][0] + tensor[0][2]) / 2
    tensor[0][1] = torch.where(diff <= tensor[0][1], diff, tensor[0][1])
    return tensor

  def _random_crop(self, *imgs):
    """ random crop image with 2048 x 2048 to random[h, w] in [1024, 2048] 
    """
    H_src, W_src = imgs[0].shape[2:]
    W_tgt = random.choice(range(512, 1024)) // 4 * 4
    H_tgt = random.choice(range(512, 1024)) // 4 * 4
    scale = max(W_tgt / W_src, H_tgt / H_src)
    results = []
    for img in imgs:
      img = kornia.resize(img, (int(H_src * scale), int(W_src * scale)))
      img = kornia.center_crop(img, (H_tgt, W_tgt))
      results.append(img)
    return results

  def _transform_train(self):
    """transform for image and background
    """
    cfg = self.Config

    if cfg.model_name == 'mattingrefine':

      img = T.pil.PairCompose([
          T.pil.PairRandomAffineAndResize((1024, 1024), degrees=(-5, 5), translate=(0.1, 0.1), scale=(0.3, 1), shear=(-5, 5)),  # nopep8
          T.pil.PairRandomHorizontalFlip(),
          T.pil.PairRandomBoxBlur(0.1, 5),
          T.pil.PairRandomSharpen(0.1),
          T.pil.PairApplyOnlyAtIndices([1], T.pil.ColorJitter(0.15, 0.15, 0.15, 0.05)),
          T.pil.PairApply(T.pil.ToTensor())
      ])

      bgr = T.pil.Compose([
          T.pil.RandomAffineAndResize((1024, 1024), degrees=(-5, 5), translate=(0.1, 0.1), scale=(1, 2), shear=(-5, 5)),  # nopep8
          T.pil.RandomHorizontalFlip(),
          T.pil.RandomVerticalFlip(),  # extra
          T.pil.RandomBoxBlur(0.1, 5),
          T.pil.RandomSharpen(0.1),
          T.pil.ColorJitter(0.15, 0.15, 0.15, 0.05),
          T.pil.ToTensor()
      ])

    elif cfg.model_name == 'mattingbase':
      pass

    else:
      raise NotImplementedError(f'Unknown input {cfg.model_name}')

    return img, bgr

  def _transform_val(self):
    """transform_val
    """
    cfg = self.Config

    if cfg.model_name == 'mattingrefine':

      img = T.pil.PairCompose([
          T.pil.PairRandomAffineAndResize((1024, 1024), degrees=(-5, 5), translate=(0.1, 0.1), scale=(0.3, 1), shear=(-5, 5)),  # nopep8
          T.pil.PairApply(T.pil.ToTensor())
      ])

      bgr = T.pil.Compose([
          T.pil.RandomAffineAndResize((1024, 1024), degrees=(-5, 5), translate=(0.1, 0.1), scale=(1, 1.2), shear=(-5, 5)),  # nopep8
          T.pil.ToTensor()
      ])

    elif cfg.model_name == 'mattingbase':
      pass

    else:
      raise NotImplementedError(f'Unknown input {cfg.model_name}')

    return img, bgr

  def _dump(self):
    """dump
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
    """load
    """
    cfg = self.Config

    logger.net('Loading model source: {}'.format(cfg.model_source))
    ckpt = tw.checkpoint.load(cfg.model_path)

    if cfg.model_source == 'tw':
      # consider dist training will add a extra `module.` header.
      state_dict = tw.checkpoint.replace_prefix(ckpt['state_dict'], 'module.', '')
      tw.checkpoint.load_matched_state_dict(self.Model, state_dict)
      if self.Optim is not None:
        self.Optim.load_state_dict(ckpt['optimizer'])
        self.Step = ckpt['global_step']
        self.Epoch = ckpt['global_epoch']

    elif cfg.model_source == 'bgm':
      tw.checkpoint.load_matched_state_dict(self.Model, ckpt)

    else:
      raise NotImplementedError(cfg.model_source)

  def _build_dataset(self, phase: tw.phase):
    """build_dataset
    """
    cfg = self.Config

    # bgm-v2 format dataset
    paths = {
        'bigo80k': {
            'train': {
                'fgr': '_datasets/matting/bigo_80k_sep/fgr',
                'pha': '_datasets/matting/bigo_80k_sep/pha'
            },
            'valid': {
                'fgr': '_datasets/matting/PhotoMatte85/PhotoMatte85_vanilla',
                'pha': '_datasets/matting/PhotoMatte85/PhotoMatte85_alpha'
            }
        },
        'photomatte13k': {
            'train': {
                'fgr': '_datasets/matting/PhotoMatte85/PhotoMatte85_vanilla',
                'pha': '_datasets/matting/PhotoMatte85/PhotoMatte85_alpha'
            },
            'valid': {
                'fgr': '_datasets/matting/PhotoMatte85/PhotoMatte85_vanilla',
                'pha': '_datasets/matting/PhotoMatte85/PhotoMatte85_alpha'
            }
        },
        'distinction': {
            'train': {
                'fgr': 'PATH_TO_IMAGES_DIR',
                'pha': 'PATH_TO_IMAGES_DIR',
            },
            'valid': {
                'fgr': 'PATH_TO_IMAGES_DIR',
                'pha': 'PATH_TO_IMAGES_DIR'
            },
        },
        'adobe': {
            'train': {
                'fgr': '_datasets/matting/Combined_Dataset/Training_set/alpha',
                'pha': '_datasets/matting/Combined_Dataset/Training_set/fg',
            },
            'valid': {
                'fgr': '_datasets/matting/PhotoMatte85/PhotoMatte85_vanilla',
                'pha': '_datasets/matting/PhotoMatte85/PhotoMatte85_alpha'
            },
        },
        'backgrounds': {
            'train': '_datasets/matting/bigo_green_bg',
            'valid': '_datasets/matting/bigo_green_bg_val'
        },
        'coco': {
            'train': '_datasets/detection/coco2017/train2017',
            'valid': '_datasets/detection/coco2017/train2017'
        },
    }

    if phase == tw.phase.train:
      # get transform of image and bgr in terms of network model
      trans_img, trans_bgr = self._transform_train()
      # (pha, fgr, bgr)
      dataset = tw.datasets.pil.ZipDataset([
          tw.datasets.pil.ZipDataset(
              datasets=[
                  tw.datasets.pil.ImagesDataset(paths[cfg.dataset]['train']['pha'], mode='L'),
                  tw.datasets.pil.ImagesDataset(paths[cfg.dataset]['train']['fgr'], mode='RGB')
              ],
              transform=trans_img,
              assert_equal_length=True),
          tw.datasets.pil.ImagesDataset(
              path=paths['backgrounds']['train'],
              mode='RGB',
              transform=trans_bgr)
      ])
      # slice dataset into non-overlapping subset for each node
      per_gpu = int(len(dataset) / cfg.dist_size)
      dataset = tw.datasets.Subset(dataset, range(cfg.dist_rank * per_gpu, (cfg.dist_rank + 1) * per_gpu))
      loader = tw.datasets.DataLoader(dataset,
                                      shuffle=True,
                                      batch_size=cfg.train_batchsize,
                                      drop_last=True,
                                      pin_memory=True,
                                      num_workers=4)

    elif phase == tw.phase.val:
      # get transform of image and bgr in terms of network model
      trans_img, trans_bgr = self._transform_val()
      # (pha, fgr, bgr)
      dataset = tw.datasets.pil.ZipDataset([
          tw.datasets.pil.ZipDataset(
              datasets=[
                  tw.datasets.pil.ImagesDataset(paths[cfg.dataset]['valid']['pha'], mode='L'),
                  tw.datasets.pil.ImagesDataset(paths[cfg.dataset]['valid']['fgr'], mode='RGB')
              ],
              transform=trans_img,
              assert_equal_length=True),
          tw.datasets.pil.ImagesDataset(
              path=paths['backgrounds']['valid'],
              mode='RGB',
              transform=trans_bgr)
      ])
      # dataset = tw.datasets.pil.SampleDataset(dataset, 50)
      loader = tw.datasets.DataLoader(dataset,
                                      pin_memory=True,
                                      drop_last=False,
                                      batch_size=1,
                                      num_workers=1)

    else:
      raise NotImplementedError(f"{phase}")

    return loader

  def _build_optim(self, model: nn.Module):
    """build_optim
    """
    cfg = self.Config

    if cfg.model_name == 'mattingrefine':
      optim = torch.optim.Adam([
          {'params': model.backbone.parameters(), 'lr': 5e-5},
          {'params': model.aspp.parameters(), 'lr': 5e-5},
          {'params': model.decoder.parameters(), 'lr': 1e-4},
          {'params': model.refiner.parameters(), 'lr': 3e-4},
      ])

    elif cfg.model_name == 'mattingbase':
      pass

    else:
      raise NotImplementedError(cfg.model_name)

    return optim

  def _build_model(self):
    """build_model
    """
    cfg = self.Config
    without_background = True if cfg.model_sgsm else False

    if cfg.model_name == 'mattingrefine':
      # origin: 32, 24, 16, 12, 4
      # slim1: 16, 16, 8, 8, 4
      model = tw.models.bgmv2.MattingRefine(
          backbone=cfg.model_backbone,
          backbone_scale=cfg.model_backbone_scale,
          refine_mode=cfg.model_refine_mode,
          refine_sample_pixels=cfg.model_refine_sample_pixels,
          refine_threshold=cfg.model_refine_threshold,
          refine_kernel_size=cfg.model_refine_kernel_size,
          refine_prevent_oversampling=True,
          refine_patch_crop_method=cfg.model_refine_patch_crop_method,
          refine_patch_replace_method=cfg.model_refine_patch_replace_method,
          refine_channels=[8, 8, 4, 4, 4],
          without_background=without_background)

    elif cfg.model_name == 'mattingbase':
      model = tw.models.bgmv2.MattingBase(backbone=cfg.model_backbone,
                                          without_background=without_background)

    else:
      raise NotImplementedError(cfg.model_name)

    # to device
    model.to(cfg.device)

    return model

  def _train_refine(self, **kwargs):
    """train refine
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

    #!< using `Automatic Mixed Precision` tech.
    if int(torch.__version__.split('.')[1]) <= 6:
      autocast = tw.runner.EmptyContext
    else:
      from torch.cuda import amp
      scaler = amp.GradScaler()
      autocast = amp.autocast

    # cutmix
    # if cfg.model_gsm:
    #   random_cutmix = kornia.augmentation.RandomCutMix(height=512, width=512, num_mix=2, p=1.0)

    # abbr
    loss_l1 = nn.functional.l1_loss
    loss_mse = nn.functional.mse_loss

    # training
    while self.Epoch < cfg.train_epoch:

      self.Epoch += 1
      self.Model.train()

      for (true_pha, true_fgr), true_bgr in train_loader:

        # --------------------------------------------------------------------
        # prepare data
        # --------------------------------------------------------------------
        self.Step += 1

        true_pha = true_pha.to(device, non_blocking=True)
        true_fgr = true_fgr.to(device, non_blocking=True)
        true_bgr = true_bgr.to(device, non_blocking=True)
        true_pha, true_fgr, true_bgr = self._random_crop(true_pha, true_fgr, true_bgr)

        # --------------------------------------------------------------------
        # augment foreground
        # --------------------------------------------------------------------

        true_src = true_bgr.clone()
        aug_shadow_idx = torch.rand(len(true_src)) < 0.3
        if aug_shadow_idx.any():
          aug_shadow = true_pha[aug_shadow_idx].mul(0.3 * random.random())
          aug_shadow = kornia.random_affine(aug_shadow, degrees=(-5, 5), translate=(0.2, 0.2), scale=(0.5, 1.5), shear=(-5, 5))  # nopep8
          aug_shadow = kornia.filters.box_blur(aug_shadow, (random.choice(range(20, 40)),) * 2)
          true_src[aug_shadow_idx] = true_src[aug_shadow_idx].sub_(aug_shadow).clamp_(0, 1)
          del aug_shadow
        del aug_shadow_idx

        # augment with noise
        aug_noise_idx = torch.rand(len(true_src)) < 0.4
        if aug_noise_idx.any():
          true_src[aug_noise_idx] = true_src[aug_noise_idx].add_(torch.randn_like(true_src[aug_noise_idx]).mul_(0.03 * random.random())).clamp_(0, 1)  # nopep8
          true_bgr[aug_noise_idx] = true_bgr[aug_noise_idx].add_(torch.randn_like(true_bgr[aug_noise_idx]).mul_(0.03 * random.random())).clamp_(0, 1)  # nopep8
        del aug_noise_idx

        # --------------------------------------------------------------------
        # augment background
        # --------------------------------------------------------------------

        # augment background with jitter
        aug_jitter_idx = torch.rand(len(true_src)) < 0.8
        if aug_jitter_idx.any():
          true_bgr[aug_jitter_idx] = kornia.augmentation.ColorJitter(0.18, 0.18, 0.18, 0.1)(true_bgr[aug_jitter_idx])
        del aug_jitter_idx

        # augment background with affine
        aug_affine_idx = torch.rand(len(true_bgr)) < 0.3
        if aug_affine_idx.any():
          true_bgr[aug_affine_idx] = kornia.random_affine(true_bgr[aug_affine_idx], degrees=(-1, 1), translate=(0.01, 0.01))  # nopep8
        del aug_affine_idx

        # extra: augment cutmix
        # if cfg.model_gsm and random.random() < 0.3:
        #   true_bgr = random_cutmix(true_bgr, torch.zeros(true_bgr.size(0)).long())[0]

        # --------------------------------------------------------------------
        # FORWARD
        # --------------------------------------------------------------------
        losses = {}

        # Composite foreground onto source
        true_src = true_fgr * true_pha + true_src * (1 - true_pha)

        # for gsm
        if cfg.model_gsm:
          true_bgr[:, 0], true_bgr[:, 1], true_bgr[:, 2] = 120.0 / 255.0, 1.0, 155.0 / 255.0
          
        # amp training if possible
        with autocast():

          pred_pha, pred_fgr, pred_pha_sm, pred_fgr_sm, pred_err_sm, _ = self.Model(true_src, true_bgr)

          true_pha_sm = kornia.resize(true_pha, pred_pha_sm.shape[2:])
          true_fgr_sm = kornia.resize(true_fgr, pred_fgr_sm.shape[2:])

          true_msk = true_pha != 0
          true_msk_sm = true_pha_sm != 0

          # tvf.to_pil_image(true_pha[0].cpu()).save(os.path.join('true_pha.png'))
          # tvf.to_pil_image(true_pha_sm[0].cpu()).save(os.path.join('true_pha_sm.png'))
          # tvf.to_pil_image(true_msk[0].byte().cpu()).save(os.path.join('true_msk.png'))
          # tvf.to_pil_image(true_src[0].cpu()).save(os.path.join('true_src.png'))
          # tvf.to_pil_image(true_bgr[0].cpu()).save(os.path.join('true_bgr.png'))

          losses['pha_l1'] = loss_l1(pred_pha, true_pha)
          losses['pha_sm_l1'] = loss_l1(pred_pha_sm, true_pha_sm)
          losses['pha_sobel'] = loss_l1(kornia.sobel(pred_pha), kornia.sobel(true_pha))
          losses['pha_sm_sobel'] = loss_l1(kornia.sobel(pred_pha_sm), kornia.sobel(true_pha_sm))
          losses['fgr_l1'] = loss_l1(pred_fgr * true_msk, true_fgr * true_msk)
          losses['fgr_sm_l1'] = loss_l1(pred_fgr_sm * true_msk_sm, true_fgr_sm * true_msk_sm)
          losses['fgr_err_l1'] = loss_mse(kornia.resize(pred_err_sm, true_pha.shape[2:]),
                                          kornia.resize(pred_pha_sm, true_pha.shape[2:]).sub(true_pha).abs())

          # summing
          loss = sum(loss for loss in losses.values())

        # amp training if possible
        if int(torch.__version__.split('.')[1]) <= 6:
          self.Optim.zero_grad()
          loss.backward()
          self.Optim.step()

        else:
          scaler.scale(loss).backward()
          scaler.step(self.Optim)
          scaler.update()
          self.Optim.zero_grad()

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

      if tw.runner.reach(self.Epoch, cfg.log_save) and self.Master:
        self._dump()

      if tw.runner.reach(self.Epoch, cfg.log_val) and self.Master:
        self._val_refine(loader=val_loader)

  def _train_base(self, **kwargs):
    """train base
    """

  def _val_refine(self, **kwargs):
    """val refine
    """
    cfg = self.Config
    device = self.Config.device
    start_time = tw.timer.tic()
    total = 0

    # reset
    self.Model.eval()

    # build dataloader
    if 'loader' in kwargs and kwargs['loader'] is not None:
      val_loader = kwargs['loader']
    else:
      val_loader = self._build_dataset(tw.phase.val)

    # create folder for every epoch
    root = tw.fs.mkdirs(f'{cfg.root}/val/epoch_{self.Epoch}_step_{self.Step}/')

    # create a stat
    stat = tw.stat.AverSet()
    loss_l1 = nn.functional.l1_loss
    loss_mse = nn.functional.mse_loss

    # start
    with torch.no_grad():
      for (true_pha, true_fgr), true_bgr in tqdm.tqdm(val_loader):
        total += true_pha.size(0)

        # -------------------------------------------------------------------
        # prepare data
        # -------------------------------------------------------------------

        true_pha = true_pha.cuda(non_blocking=True)
        true_fgr = true_fgr.cuda(non_blocking=True)
        true_bgr = true_bgr.cuda(non_blocking=True)
        true_src = true_pha * true_fgr + (1 - true_pha) * true_bgr

        # for gsm
        if cfg.model_gsm:
          true_bgr[:, 0], true_bgr[:, 1], true_bgr[:, 2] = 120.0 / 255.0, 1.0, 155.0 / 255.0

        pred_pha, pred_fgr, pred_pha_sm, pred_fgr_sm, pred_err_sm, _ = self.Model(true_src, true_bgr)

        true_pha_sm = kornia.resize(true_pha, pred_pha_sm.shape[2:])
        true_fgr_sm = kornia.resize(true_fgr, pred_fgr_sm.shape[2:])

        true_msk = true_pha != 0
        true_msk_sm = true_pha_sm != 0

        losses = {
            'pha_l1': 255.0 * loss_l1(pred_pha, true_pha),
            'pha_sm_l1': 255.0 * loss_l1(pred_pha_sm, true_pha_sm),
            'pha_sobel': 255.0 * loss_l1(kornia.sobel(pred_pha), kornia.sobel(true_pha)),
            'pha_sm_sobel': 255.0 * loss_l1(kornia.sobel(pred_pha_sm), kornia.sobel(true_pha_sm)),
            'fgr_l1': 255.0 * loss_l1(pred_fgr * true_msk, true_fgr * true_msk),
            'fgr_sm_l1': 255.0 * loss_l1(pred_fgr_sm * true_msk_sm, true_fgr_sm * true_msk_sm),
            'pha_err_l1': 255.0 * loss_mse(kornia.resize(pred_err_sm, true_pha.shape[2:]), kornia.resize(pred_pha_sm, true_pha.shape[2:]).sub(true_pha).abs()),  # nopep8
        }
        stat.update(losses.keys(), losses.values())

    # stat
    elapsed = tw.timer.duration(start_time, tw.timer.tic())
    throughput = tw.timer.throughput(elapsed, total)
    keys = list(stat.keys()) + ['time', 'throughtput']
    vals = list(stat.values()) + [elapsed, throughput]
    tw.runner.log(keys=keys, values=vals, step=self.Step, epoch=self.Epoch, tag='val', writer=self.Writer)

  def _val_base(self, **kwargs):
    """val
    """

  def _viz_write_image(self, output_folder, name, bgr, fgr, pha, err=None, ref=None):
    """write out to image
    """
    # output composite
    fgr = self._split_compression(fgr)
    com = fgr * pha + bgr * (1 - pha)

    # output to com
    tvf.to_pil_image(com[0].cpu()).save(os.path.join(output_folder, name + '.com.png'))
    # output predicted alpha matte
    tvf.to_pil_image(pha[0].cpu()).save(os.path.join(output_folder, name + '.pha.png'))
    # output foreground
    tvf.to_pil_image(fgr[0].cpu()).save(os.path.join(output_folder, name + '.fgr.png'))
    # output error map
    if err is not None:
      err = nn.functional.interpolate(err, com.shape[2:], mode='bilinear', align_corners=False)
      tvf.to_pil_image(err[0].cpu()).save(os.path.join(output_folder, name + '.err.png'))

    # output reference map
    if ref is not None:
      ref = nn.functional.interpolate(ref, com.shape[2:], mode='nearest')
      tvf.to_pil_image(ref[0].cpu()).save(os.path.join(output_folder, name + '.ref.png'))

  def _viz_write_video(self, writers, bgr, fgr, pha, err=None, ref=None):
    """write out to video
    """
    fgr = self._split_compression(fgr)
    com = fgr * pha + bgr * (1 - pha)

    writers['com'].write_tensor(com, is_rgb=True)
    writers['pha'].write_tensor(pha, is_rgb=True)
    writers['fgr'].write_tensor(fgr, is_rgb=True)

    if err is not None:
      err = nn.functional.interpolate(err, com.shape[2:], mode='bilinear', align_corners=False)
      writers['err'].write_tensor(err, is_rgb=True)

    if ref is not None:
      ref = nn.functional.interpolate(ref, com.shape[2:], mode='nearest')
      writers['ref'].write_tensor(err, is_rgb=True)

  def _viz(self, **kwargs):
    """viz
    """
    cfg = self.Config
    device = cfg.device
    images, videos = tw.media.collect(cfg.viz_input)
    err, ref = None, None

    # to eval
    self.Model.eval()

    # check output folder
    if not os.path.exists(cfg.viz_output):
      tw.fs.mkdirs(cfg.viz_output)
    if not os.path.isdir(cfg.viz_output):
      raise ValueError(f"{cfg.viz_output} is not a folder path.")

    # open background
    if not cfg.model_gsm and not cfg.model_sgsm:
      bgr = Image.open(cfg.viz_bgr)
      bgr = tvf.to_tensor(bgr).to(device, non_blocking=True).unsqueeze(0)[:, :3, :, :]

    # open target background
    if cfg.viz_target_bgr is None:
      tgt_bgr = torch.tensor([120/255, 255/255, 155/255], device=device).view(1, 3, 1, 1)
    else:
      tgt_bgr = Image.open(cfg.viz_target_bgr)
      tgt_bgr = tvf.to_tensor(tgt_bgr).to(device, non_blocking=True).unsqueeze(0)[:, :3, :, :]

    # ----------------------------------------------------------------------
    #   PROCESS IMAGES
    # ----------------------------------------------------------------------

    for filepath in tqdm.tqdm(images):

      assert os.path.exists(filepath), f"Failed to open {filepath}."
      src = Image.open(filepath)
      src = tvf.to_tensor(src).to(device, non_blocking=True).unsqueeze(0)[:, :3, :, :]

      if cfg.model_gsm:
        bgr = src.clone()
        bgr[:, 0], bgr[:, 1], bgr[:, 2] = 120.0 / 255.0, 1.0, 155.0 / 255.0

      if cfg.model_gsm and bgr.shape != src.shape:
        _, _, h, w = src.shape
        bgr = nn.functional.interpolate(bgr, [h, w])
        
      if cfg.model_sgsm:
        bgr = None

      if cfg.model_name == 'mattingbase':
        pha, fgr, err, _ = self.Model(src, bgr)
      elif cfg.model_name == 'mattingrefine':
        pha, fgr, _, _, err, ref = self.Model(src, bgr)

      if cfg.viz_target_bgr is not None:
        _, _, h, w = src.shape
        tgt_bgr = nn.functional.interpolate(tgt_bgr, [h, w])

      # write out
      pathname = os.path.basename(filepath)[:-4]
      self._viz_write_image(cfg.viz_output, pathname, tgt_bgr, fgr, pha, err, ref)

    # ----------------------------------------------------------------------
    #   PROCESS VIDEOS
    # ----------------------------------------------------------------------

    for filepath in videos:

      try:
        # parser video into numpy format frame
        vid_name = os.path.basename(filepath)[:-4]

        # reader
        reader = tw.media.VideoReader(filepath, to_rgb=True, to_tensor=True)

        # writer
        if cfg.viz_type == 'video':
          writers = {}
          for k in ['com', 'pha', 'fgr', 'err', 'ref']:
            output_path = os.path.join(cfg.viz_output, vid_name + f'.{k}.mp4')
            writers[k] = tw.media.VideoWriter(output_path, reader.width, reader.height, reader.fps)

        # inference each frame
        for fid, src in enumerate(tqdm.tqdm(reader)):

          # src and bgr
          src = src.to(device, non_blocking=True).unsqueeze(0)

          if cfg.model_gsm:
            bgr = src.clone()
            bgr[:, 0], bgr[:, 1], bgr[:, 2] = 120.0 / 255.0, 1.0, 155.0 / 255.0

          if cfg.model_gsm and bgr.shape != src.shape:
            _, _, h, w = src.shape
            bgr = nn.functional.interpolate(bgr, [h, w])
            
          if cfg.model_sgsm:
            bgr = None

          if cfg.model_name == 'mattingbase':
            pha, fgr, err, _ = self.Model(src, bgr)
          elif cfg.model_name == 'mattingrefine':
            pha, fgr, _, _, err, ref = self.Model(src, bgr)

          if cfg.viz_target_bgr is not None:
            _, _, h, w = src.shape
            tgt_bgr = nn.functional.interpolate(tgt_bgr, [h, w])

          # output composite
          if cfg.viz_type == 'video':
            self._viz_write_video(writers, tgt_bgr, fgr, pha, err, ref)

          elif cfg.viz_type == 'image':
            # output composite
            com = fgr * pha + bgr * (1 - pha)
            # output to com
            tw.fs.mkdirs(os.path.join(cfg.viz_output, vid_name, 'com'))
            tvf.to_pil_image(com[0].cpu()).save(os.path.join(cfg.viz_output, vid_name, 'com', "%08d.png" % fid))  # nopep8
            # output predicted alpha matte
            tw.fs.mkdirs(os.path.join(cfg.viz_output, vid_name, 'pha'))
            tvf.to_pil_image(pha[0].cpu()).save(os.path.join(cfg.viz_output, vid_name, 'pha', "%08d.png" % fid))  # nopep8
            # output foreground
            tw.fs.mkdirs(os.path.join(cfg.viz_output, vid_name, 'fgr'))
            tvf.to_pil_image(fgr[0].cpu()).save(os.path.join(cfg.viz_output, vid_name, 'fgr', "%08d.png" % fid))  # nopep8

      except Exception as e:
        tw.logger.error('{}'.format(e))

  def _onnx(self, **kwargs):
    """onnx
    """
    cfg = self.Config
    device = cfg.device

    # support fp32 or fp16
    precision = torch.float32
    self.Model.to(precision)
    self.Model.eval()

    # dummy inputs
    src = torch.randn(1, 3, 720, 1280).to(precision).to(device)
    bgr = torch.randn(1, 3, 720, 1280).to(precision).to(device)

    # compute complex
    tw.flops.register(self.Model)
    with torch.no_grad():
      self.Model(src, bgr)
    print(tw.flops.accumulate(self.Model))
    tw.flops.unregister(self.Model)

    # export onnx
    if cfg.model_name == 'mattingbase':
      input_names = ['src', 'bgr']
      output_names = ['pha', 'fgr', 'err', 'hid']
    if cfg.model_name == 'mattingrefine':
      input_names = ['src', 'bgr']
      output_names = ['pha', 'fgr', 'pha_sm', 'fgr_sm', 'err_sm', 'ref_sm']

    # dump
    tw.export.torch_to_onnx(model=self.Model,
                            args=(src, bgr),
                            output_path=f"{cfg.model_name}.{cfg.model_backbone}.onnx",
                            input_names=input_names,
                            output_names=output_names,
                            dynamic_axes={name: {0: 'batch', 2: 'height', 3: 'width'}
                                          for name in [*input_names, *output_names]})

  def _tensorrt(self, **kwargs):
    """tensorrt
    """
    cfg = self.Config
    tw.export.onnx_to_trt(
        f"{cfg.model_name}.{cfg.model_backbone}.onnx",
        f"{cfg.model_name}.{cfg.model_backbone}.engine",
        shapes={'src': {'min': (1, 1, 32, 32), 'best': (1, 1, 1280, 720), 'max': (1, 1, 1440, 1440)}},
        verbose=True)

  def __call__(self):
    """prepare basic
    """
    cfg = self.Config

    if cfg.task == 'train':
      if cfg.model_name == 'mattingrefine':
        self._train_refine()
      elif cfg.model_name == 'mattingbase':
        self._train_base()
      else:
        raise NotImplementedError(cfg.model_name)

    elif cfg.task == 'val':
      with torch.no_grad():
        if cfg.model_name == 'mattingrefine':
          self._val_refine()
        elif cfg.model_name == 'mattingbase':
          self._val_base()
        else:
          raise NotImplementedError(cfg.model_name)

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
  parser.add_argument('--dataset', type=str, default=None,
                      choices=['bigo80k', 'photomatte13k', 'distinction', 'adobe'])

  # ---------------------------------------------
  #  USED BY LOGGER
  # ---------------------------------------------
  parser.add_argument('--log', type=int, default=10, help="display interval step.")
  parser.add_argument('--log-val', type=int, default=1, help="running validation in terms of step.")
  parser.add_argument('--log-test', type=int, default=1, help="running test in terms of step.")
  parser.add_argument('--log-save', type=int, default=1, help="saveing checkpoint with interval.")

  # ---------------------------------------------
  #  USED BY MODEL-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--model-name', type=str, required=True, choices=['mattingbase', 'mattingrefine'])
  parser.add_argument('--model-path', type=str, default=None, help="loadding pretrain/last-checkpoint model.")
  parser.add_argument('--model-source', type=str, default=None)

  # model specific
  parser.add_argument('--model-backbone', type=str, required=True, choices=['resnet101', 'resnet50', 'mobilenetv2'])
  parser.add_argument('--model-backbone-scale', type=float, default=0.25)
  parser.add_argument('--model-refine-mode', type=str, default='full', choices=['full', 'sampling', 'thresholding'])
  parser.add_argument('--model-refine-sample-pixels', type=int, default=80_000)
  parser.add_argument('--model-refine-threshold', type=float, default=0.7)
  parser.add_argument('--model-refine-kernel-size', type=int, default=3)
  parser.add_argument('--model-refine-patch-crop-method', type=str, default='roi_align', choices=['unfold', 'roi_align', 'gather'])  # nopep8
  parser.add_argument('--model-refine-patch-replace-method', type=str, default='scatter_element', choices=['scatter_nd', 'scatter_element'])  # nopep8

  # gsm
  parser.add_argument('--model-gsm', action='store_true', help="using green screen matting backend.")
  parser.add_argument('--model-sgsm', action='store_true', help="using single-input green screen matting backend.")

  # ---------------------------------------------
  #  USED BY TRAIN-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--train-batchsize', type=int, default=4, help="total batch size across devices.")
  parser.add_argument('--train-epoch', type=int, default=240, help="total training epochs.")

  # ---------------------------------------------
  #  USED BY VAL-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--val-batchsize', type=int, default=1, help="total batch size across devices.")

  # ---------------------------------------------
  #  USED BY VIZ-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--viz-input', type=str, help='input path could be a folder/filepath.')
  parser.add_argument('--viz-bgr', type=str, help='image or video background.')
  parser.add_argument('--viz-target-bgr', type=str, help='target background.')
  parser.add_argument('--viz-output', type=str, help='output path should be a folder path.')
  parser.add_argument('--viz-type', type=str, default='image', choices=['image', 'video'])

  tw.runner.launch(parser, BackgroundMattingV2)
