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
"""Blind IQA System
"""
import os
import argparse
import tqdm
import numpy as np

import torch
from torch import nn
from torch import distributed
from torch.utils import tensorboard

import tw
from tw import logger
from tw import transform as T

import models
import common


def exp_lr_scheduler(optimizer, epoch, lr_decay_epoch=10):
  """Decay learning rate by a factor of DECAY_WEIGHT every lr_decay_epoch epochs."""
  decay_rate = 0.8**(epoch // lr_decay_epoch)
  if epoch % lr_decay_epoch == 0:
    tw.logger.net('decay_rate is set to {}'.format(decay_rate))
  for param_group in optimizer.param_groups:
    param_group['lr'] = param_group['lr'] * decay_rate
  return optimizer, True


def step_lr_scheduler(optimizer, epoch, steps=[40, 20], gamma=0.2):
  """Decay learning rate by a factor of DECAY_WEIGHT every lr_decay_epoch epochs."""
  if epoch in steps:
    for i, param_group in enumerate(optimizer.param_groups):
      param_group['lr'] = param_group['lr'] * gamma
      tw.logger.net(f'params[{i}] lr is set to {param_group["lr"]}')
    return optimizer, True
  return optimizer, False


class BlindIQA():

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

    # optim
    if self.Config.task == 'train':
      if self.Config.model.startswith('koncept'):
        self.Optim = torch.optim.Adam([
            {'params': self.Model.head.parameters(), 'lr': 1e-2},
            {'params': self.Model.cls_head.parameters(), 'lr': 1e-2},
            {'params': self.Model.backbone.parameters(), 'lr': 1e-4}
        ], lr=1e-2, weight_decay=0.0)
      elif self.Config.model.startswith('patchiqa'):
        mode = self.Config.model.split('.')[2]
        if mode == 'base':
          params_group = [
              {'params': self.Model.head.parameters(), 'lr': 1e-3},
              {'params': self.Model.reg_head.parameters(), 'lr': 1e-3},
              {'params': self.Model.backbone.parameters(), 'lr': 1e-4}]
        elif mode in ['feedback', 'roi']:
          params_group = [
              {'params': self.Model.head.parameters(), 'lr': 1e-3},
              {'params': self.Model.reg_head.parameters(), 'lr': 1e-3},
              {'params': self.Model.roi_head.parameters(), 'lr': 1e-3},
              {'params': self.Model.roi_reg_head.parameters(), 'lr': 1e-3},
              {'params': self.Model.backbone.parameters(), 'lr': 1e-4}]
        else:
          raise NotImplementedError(mode)
        self.Optim = torch.optim.Adam(params_group, lr=1e-3, weight_decay=0.0)
      else:
        self.Optim = torch.optim.Adam(self.Model.parameters(), lr=1e-4, weight_decay=0.0)

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

    if cfg.model == 'hyper_iqa':
      model = models.HyperNet(16, 112, 224, 112, 56, 28, 14, 7)

    elif cfg.model.startswith('base'):
      backbone = cfg.model.split('.')[1]
      model = models.BaseIQA(backbone=backbone)

    elif cfg.model.startswith('compose'):
      backbone = cfg.model.split('.')[1]
      model = models.ComposeBlindIQA(backbone=backbone)

    elif cfg.model.startswith('koncept'):
      backbone = cfg.model.split('.')[1]
      model = models.KonCept512(backbone=backbone)

    elif cfg.model.startswith('patchiqa'):
      backbone = cfg.model.split('.')[1]
      model = models.PatchIQA(backbone=backbone, mode=cfg.model.split('.')[2])

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

  def _compute_rank_loss(self, preds, labels, margin):
    bs = labels.size(0)
    cross_preds = preds.reshape(bs, 1) - preds.reshape(1, bs)
    cross_labels = labels.reshape(bs, 1) - labels.reshape(1, bs)
    rankloss = margin - cross_preds * cross_labels
    zero = torch.zeros_like(rankloss)
    rankloss = torch.where(rankloss > 0, rankloss, zero)
    rankloss = rankloss.sum() / torch.nonzero(rankloss, as_tuple=False).size(0)
    return rankloss

  def _optimize(self, samples, **kwargs):
    """forward phase

    Args:
        inputs ([torch.Tensor]): [N, C, H, W]
        labels ([torch.Tesnor]): [N, ]

    Returns:
        losses (dict): 
    """
    cfg = self.Config
    device = self.Config.device
    losses = {}

    if cfg.model == 'hyper_iqa':
      inputs = samples[0].float().to(device, non_blocking=True)
      labels = samples[1].float().to(device, non_blocking=True)

      paras = self.Model(inputs)
      model_target = models.TargetNet(paras).to(device)
      for param in model_target.parameters():
        param.requires_grad = False
      preds = model_target(paras['target_in_vec'])
      loss_l1 = self.loss_l1(preds.squeeze(), labels.float())
      losses['loss_l1'] = loss_l1

    elif cfg.model.startswith('base'):
      inputs = samples[0].float().to(device, non_blocking=True)
      labels = samples[1].float().to(device, non_blocking=True)
      preds = self.Model(inputs)
      loss_l1 = self.loss_l1(preds.squeeze(), labels.float())
      losses['loss_l1'] = loss_l1
      losses['loss_rank'] = self._compute_rank_loss(preds, labels, margin=10)

    elif cfg.model.startswith('compose') or cfg.model.startswith('koncept'):
      inputs = samples[0].float().to(device, non_blocking=True)
      labels = samples[1].float().to(device, non_blocking=True)
      preds = self.Model(inputs)
      losses['loss_mse'] = self.loss_mse(preds.squeeze(), labels.float())
      # losses['loss_rank'] = self._compute_rank_loss(preds, labels, margin=1e-6)

    elif cfg.model.startswith('patchiqa'):
      inputs, labels, boxes, boxes_labels = [], [], [], []
      for sample in samples:
        inputs.append(sample[0].bin)
        labels.append(sample[0].label)
        boxes.append(sample[1].bboxes)
        boxes_labels.append(sample[1].label)
      inputs = torch.stack(inputs).float().to(device, non_blocking=True)  # n, c, h, w
      labels = torch.tensor(labels).float().to(device, non_blocking=True)  # n,
      bboxes = torch.tensor(boxes).float().to(device, non_blocking=True)  # n, 3, 4
      bboxes_labels = torch.tensor(boxes_labels).float().to(device, non_blocking=True)  # n, 3
      mode = cfg.model.split('.')[2]
      if mode == 'base':
        preds = self.Model(inputs, bboxes)
        losses['loss_mse'] = self.loss_mse(preds.squeeze(), labels.float())
      elif mode == 'roi':
        pred_mos, pred_rois_mos = self.Model(inputs, bboxes)
        losses['loss_mse'] = self.loss_mse(pred_mos.squeeze(), labels.float())
        losses['loss_mse_rois'] = self.loss_mse(pred_rois_mos.squeeze(), bboxes_labels.float())
      elif mode == 'feedback':
        pred_mos, pred_rois_mos = self.Model(inputs, bboxes)
        losses['loss_mse'] = self.loss_mse(pred_mos.squeeze(), labels.float())
        losses['loss_mse_rois'] = self.loss_mse(pred_rois_mos.squeeze(), bboxes_labels.float())
      else:
        raise NotImplementedError(mode)

    return losses

  def _inference(self, inputs, **kwargs):
    """forward phase

    Args:
        inputs ([torch.Tensor]): [N, C, H, W]

    Returns:
        predictions ([troch.Tensor]): [N, ]
    """
    cfg = self.Config
    device = self.Config.device
    model = self.Model.module if cfg.multiprocess else self.Model

    if cfg.model == 'hyper_iqa':
      paras = model(inputs)
      model_target = models.TargetNet(paras).to(device)
      for param in model_target.parameters():
        param.requires_grad = False
      preds = model_target(paras['target_in_vec'])
      return preds

    elif cfg.model.startswith('base'):
      return model(inputs).squeeze()

    elif cfg.model.startswith('compose'):
      return model(inputs).squeeze()

    elif cfg.model.startswith('koncept'):
      return model(inputs).squeeze()

    elif cfg.model.startswith('patchiqa'):
      return model(inputs).squeeze()

    raise NotImplementedError

  def _train(self):
    """training
    """
    cfg = self.Config
    device = self.Config.device
    init_step = self.Step
    stat = tw.stat.AverSet()
    start_time = tw.timer.tic()

    # build train dataset
    train_loader = common.build_dataset(cfg, tw.phase.train, blind_mode=True)
    total_step = len(train_loader) * cfg.train_epoch

    # print trainable parameters
    tw.checkpoint.print_trainable_variables(self.Model)

    # pixel
    self.loss_l1 = nn.L1Loss().to(device)
    self.loss_mse = nn.MSELoss().to(device)

    # record
    best_plcc, best_srocc, best_epoch, best_wts = 0, 0, 0, 0

    # training
    while self.Epoch < cfg.train_epoch:

      self.Epoch += 1
      self.Model.train()

      # sync model parameters
      self.Optim, lr_changed = step_lr_scheduler(self.Optim, self.Epoch, steps=[20, 30, 40], gamma=0.1)
      if lr_changed:
        if self.Master:
          self.Model.load_state_dict(best_wts)
        if self.Config.multiprocess:
          for p in self.Model.parameters():
            distributed.broadcast(p, src=0)
        tw.logger.net(f'reloading best params on epoch: {best_epoch}')

      # training a epoch
      for samples in train_loader:

        # prepare data
        self.Step += 1

        # inference
        losses = self._optimize(samples)

        # accumulate
        loss = sum(loss for loss in losses.values())
        self.Optim.zero_grad()
        loss.backward()
        self.Optim.step()

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
                        values=[eta] + stat.values() + [self.Optim.param_groups[0]['lr']],
                        step=self.Step,
                        epoch=self.Epoch,
                        tag='train',
                        iters_per_epoch=len(train_loader),
                        writer=self.Writer)
          stat.reset()

      if tw.runner.reach(self.Step, cfg.log_save) and self.Master:
        self._dump()

      if tw.runner.reach(self.Epoch, cfg.log_val) and self.Master:
        best_wts = self.Model.state_dict()
        reports = self._val()
        if reports['plcc'] > best_plcc:
          best_plcc = reports['plcc']
          best_srocc = reports['srocc']
          best_epoch = self.Epoch
        tw.logger.val(f'best result on epoch:{best_epoch}, srocc:{best_srocc}, plcc:{best_plcc}')

      if tw.runner.reach(self.Epoch, cfg.log_test) and self.Master:
        self._test()

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
      loader = common.build_dataset(cfg, tw.phase.val, blind_mode=True)

    # create folder for every epoch
    root = tw.fs.mkdirs(f'{cfg.root}/val/epoch_{self.Epoch}_step_{self.Step}/')
    result_path = os.path.join(root, 'prediction.txt')
    result = open(result_path, 'w')

    # start
    with torch.no_grad():

      for images, labels, paths in tqdm.tqdm(loader):

        total += images.size(0)

        images = images.float().to(device, non_blocking=True)
        labels = labels.float().to(device, non_blocking=True)

        if images.ndim == 5:
          preds = []
          for image in images:
            pred = self._inference(image)
            preds.append(pred.mean())
          preds = torch.tensor(preds)
        else:
          preds = self._inference(images)
          if preds.ndim == 0:
            preds = preds.reshape([-1])

        # write to file
        for path, label, pred in zip(paths, labels, preds):
          result.write('{} {} {}\n'.format(path, label.item(), pred.item()))

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

    return reports

  def _test(self, **kwargs):
    """test (ref, distort)"""
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
      loader = common.build_dataset(cfg, tw.phase.test, blind_mode=True)

    # create folder for every epoch
    root = tw.fs.mkdirs(f'{cfg.root}/test/epoch_{self.Epoch}_step_{self.Step}/')
    result_path = os.path.join(root, 'prediction.txt')
    result = open(result_path, 'w')

    # start
    with torch.no_grad():

      for images, labels, paths in tqdm.tqdm(loader):

        total += images.size(0)

        images = images.float().to(device, non_blocking=True)
        labels = labels.float().to(device, non_blocking=True)

        if images.ndim == 5:
          preds = []
          for image in images:
            pred = self._inference(image)
            preds.append(pred.mean())
          preds = torch.tensor(preds)
        else:
          preds = self._inference(images)
          if preds.ndim == 0:
            preds = preds.reshape([-1])

        # write to file
        for path, label, pred in zip(paths, labels, preds):
          result.write('{} {} {}\n'.format(path, label.item(), pred.item()))

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

    return reports

  def _viz(self, **kwargs):
    """inference a mp4/yuv video clip"""
    cfg = self.Config
    device = cfg.device

    # visualize during training
    if 'viz_output' in kwargs:
      viz_output = kwargs['viz_output']
    else:
      viz_output = cfg.viz_output

    if 'viz_input' in kwargs:
      viz_input = kwargs['viz_input']
    else:
      viz_input = cfg.viz_input

    # mkdir
    images, videos = tw.media.collect(viz_input)
    if not os.path.exists(viz_output):
      os.makedirs(viz_output)

    # to eval
    self.Model.eval()

    # process video
    for filepath in sorted(videos):
      reader = tw.media.VideoReader(filepath, to_rgb=False, to_tensor=False)
      results = []
      print(filepath)
      for i, src in enumerate(reader):
        meta = common.transform_val([T.ImageMeta(binary=src)], cfg)[0]
        images = meta.bin.float().to(device).unsqueeze(dim=0)
        preds = self._inference(images)
        results.append(preds.item())
        # if i == 30:
        #   break
        print(i, preds.item())
      print(np.mean(results), np.min(results), np.std(results))
      print('========')
      # print(filepath, results, np.mean(results), np.std(results))

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
  tw.runner.launch(parser, BlindIQA)
