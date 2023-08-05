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
import argparse
import tqdm
import numpy as np

import torch
from torch import nn
from torch import distributed
from torch.utils import tensorboard
from torch.nn import functional as F

import tw
from tw import logger
from tw import transform as T
from tw.evaluator.segmentation import display_confusion_matrix

import models


class SensatUrban():

  def __init__(self, config):
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
    tw.logger.net(str(self.Model))

    # optim
    if self.Config.task == 'train':
      self.Optim = torch.optim.Adam(self.Model.parameters(), lr=self.Config.lr, weight_decay=0.0)
    else:
      self.Optim = None

    # load model and possible optimizer
    if self.Config.model_path is not None:
      self._load()

    # extend to distributed
    # if self.Config.dist_size > 1:
    if self.Config.task == 'train':
      # self.Model = torch.nn.SyncBatchNorm.convert_sync_batchnorm(self.Model)
      self.Model = torch.nn.DataParallel(self.Model)

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

  def _build_model(self):
    """build iqa models
    """
    cfg = self.Config
    device = self.Config.device

    if cfg.model == 'randlanet':
      model = models.RandLANet(
          num_classes=cfg.num_classes,
          num_layers=cfg.num_layers,
          decoder_feature_dims=cfg.decoder_feature_dims)

    elif cfg.model == 'randlanet_plus':
      model = models.RandLANetPlus(
          num_classes=cfg.num_classes,
          num_layers=cfg.num_layers,
          feature_dims=cfg.decoder_feature_dims)

    elif cfg.model == 'randlanet_multihead':
      model = models.RandLANetMultiHead(
          num_classes=cfg.num_classes,
          num_layers=cfg.num_layers,
          feature_dims=cfg.decoder_feature_dims)

    elif cfg.model.startswith('randlanet_stack'):
      stack_count = int(cfg.model.split('randlanet_stack')[1])
      model = models.RandLANetStack(
          num_classes=cfg.num_classes,
          num_layers=cfg.num_layers,
          feature_dims=cfg.decoder_feature_dims,
          num_stacks=stack_count)

    else:
      raise NotImplementedError(cfg.model)

    model.to(device)
    return model

  def _build_dataset(self, phase):
    """build dataset"""
    cfg = self.Config
    dataset = tw.datasets.SensatUrban(
        original_block_ply_path=cfg.dataset_original,
        grid_path=cfg.dataset_grid,
        phase=phase,
        batchsize=cfg.train_batchsize if phase == tw.phase.train else cfg.val_batchsize,
        step=cfg.train_steps if phase == tw.phase.train else cfg.val_steps,
        noise_init=3.5,
        num_points=cfg.num_points,
        num_layers=len(cfg.sub_sampling_ratio),
        knn_num=cfg.knn_num,
        sub_sampling_ratio=cfg.sub_sampling_ratio,
        rank=cfg.dist_rank,
        subset=cfg.subset)
    return dataset

  def _build_dataloader(self, phase, dataset):
    """build dataloader"""
    cfg = self.Config

    if phase == tw.phase.train:
      return torch.utils.data.DataLoader(
          dataset=dataset,
          batch_size=cfg.train_batchsize,
          shuffle=False,
          num_workers=8,
          collate_fn=None,
          pin_memory=False,
          drop_last=True)
    elif phase in [tw.phase.val, tw.phase.test]:
      return torch.utils.data.DataLoader(
          dataset=dataset,
          batch_size=cfg.val_batchsize,
          shuffle=False,
          num_workers=4,
          collate_fn=None,
          pin_memory=False,
          drop_last=False)
    else:
      raise NotImplementedError(phase.value)

  def _adjust_learning_rate(self, optimizer, method):

    if method == 'poly':
      lr = optimizer.param_groups[0]['lr']
      lr = lr * self.Config.lr_decay
      for param_group in optimizer.param_groups:
        param_group['lr'] = lr
      return False

    elif method == 'step':
      gamma = 0.1
      if self.Epoch in [150, 250, ]:
        for i, param_group in enumerate(optimizer.param_groups):
          param_group['lr'] = param_group['lr'] * gamma
          tw.logger.net(f'params[{i}] lr is set to {param_group["lr"]}')
        return True
      return False

    else:
      raise NotImplementedError(method)

  def _train(self):
    """training
    """
    cfg = self.Config
    device = self.Config.device
    init_step = self.Step
    stat = tw.stat.AverSet()
    start_time = tw.timer.tic()

    # build train dataset
    train_set = self._build_dataset(tw.phase.train)
    train_loader = self._build_dataloader(tw.phase.train, train_set)
    total_step = cfg.train_steps * cfg.train_epoch

    # build val dataset
    val_set = self._build_dataset(tw.phase.val)
    val_loader = self._build_dataloader(tw.phase.val, val_set)

    # print trainable parameters
    tw.checkpoint.print_trainable_variables(self.Model)

    # pixel
    class_weights = train_set.get_class_weights(train_set.num_per_class, name='cb')
    class_weights = torch.from_numpy(class_weights).float().to(device)
    self.loss_wce = nn.CrossEntropyLoss(weight=class_weights, reduction='none')

    tw.logger.train(f'class weight:{class_weights.cpu().numpy().tolist()}')

    # record
    best_iou, best_epoch, best_wts = 0, 0, 0
    scaler = torch.cuda.amp.GradScaler()

    # training
    while self.Epoch < cfg.train_epoch:

      self.Epoch += 1
      self.Model.train()
      train_set.sample_an_epoch()

      # training a epoch
      for inputs in train_loader:

        # prepare data
        self.Step += 1
        self.Optim.zero_grad()

        # parse inputs
        input_points = [item.to(device) for item in inputs[0]]
        input_neighbors = [item.to(device) for item in inputs[1]]
        input_pools = [item.to(device) for item in inputs[2]]
        input_up_samples = [item.to(device) for item in inputs[3]]
        input_features = inputs[4].to(device)
        input_labels = inputs[5].to(device)
        input_queried = inputs[6].to(device)
        input_idx = inputs[7].to(device)

        # prediction
        with torch.cuda.amp.autocast():
          losses = {}

          if cfg.model in ['randlanet', 'randlanet_plus']:
            preds = self.Model(input_points, input_neighbors, input_pools, input_up_samples, input_features)
            losses = {'loss_wce': self.loss_wce(preds.reshape(-1, cfg.num_classes), input_labels.reshape(-1)).mean()}

          elif cfg.model in ['randlanet_multihead']:
            preds = self.Model(input_points, input_neighbors, input_pools, input_up_samples, input_features)
            for idx, (pred, pool) in enumerate(zip(preds[:-1], input_pools[::-1][1:])):
              if idx < 3:
                continue
              labels = torch.gather(input_labels, 1, pool[..., 0])
              losses[f'loss_wce_{idx}'] = (idx + 1) * 2.0 / 10.0 * \
                  self.loss_wce(pred.reshape(-1, cfg.num_classes), labels.reshape(-1)).mean()
            losses['loss_wce'] = self.loss_wce(preds[-1].reshape(-1, cfg.num_classes), input_labels.reshape(-1)).mean()
            
          elif cfg.model.startswith('randlanet_stack'):
            preds = self.Model(input_points, input_neighbors, input_pools, input_up_samples, input_features)
            for i, pred in enumerate(preds):
              losses[f'loss_stack{i}'] = self.loss_wce(pred.reshape(-1, cfg.num_classes), input_labels.reshape(-1)).mean()

          else:
            raise NotImplementedError(cfg.model)

        # accumulate
        loss = sum(loss for loss in losses.values())

        # normal method
        # loss.backward()
        # self.Optim.step()

        # amp
        scaler.scale(loss).backward()
        scaler.step(self.Optim)
        scaler.update()

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

      if tw.runner.reach(self.Epoch, cfg.log_save) and self.Master:
        self._dump()

      if tw.runner.reach(self.Epoch, cfg.log_val) and self.Master:
        best_wts = self.Model.state_dict()
        reports = self._val(dataset=val_set, loader=val_loader)
        if reports['mIoU'] > best_iou:
          best_iou = reports['mIoU']
          best_epoch = self.Step
        tw.logger.val(f'best result on step:{best_epoch}, mIoU:{best_iou}')
        self.Model.train()

      # adjust lr after epoch
      tw.logger.info(f'{train_set.min_possibility}')
      changed = self._adjust_learning_rate(self.Optim, method=cfg.lr_schedule)
      # if changed:
      #   self.Model.load_state_dict(best_wts)
      #   tw.logger.info(f'Loading best model {best_epoch} when lr changed.')

  def _val(self, **kwargs):
    """val (ref, distort)"""
    cfg = self.Config
    device = self.Config.device
    start_time = tw.timer.tic()
    total = 0

    # reset
    self.Model.eval()

    # build dataloader
    if 'loader' in kwargs and 'dataset' in kwargs:
      loader = kwargs['loader']
      dataset = kwargs['dataset']
    else:
      dataset = self._build_dataset(tw.phase.val)
      loader = self._build_dataloader(tw.phase.val, dataset)

    # reset point cloud possibility
    dataset.possibility = []
    dataset.min_possibility = []
    for i, tree in enumerate(dataset.input_colors):
      dataset.possibility += [np.zeros(tree.data.shape[0])]
      dataset.min_possibility += [0.0]

    # sample a batch
    dataset.sample_an_epoch()

    # prepare results
    cloud_points = [colors.shape[0] for colors in dataset.input_colors]
    results = {
        'preds': [torch.zeros(n, cfg.num_classes).float().to(device) for n in cloud_points],
        'labels': [torch.zeros(n, ).long().to(device) for n in cloud_points],
        'counts': [torch.zeros(n, ).long().to(device) for n in cloud_points],
        # 'features': [torch.zeros(num, 6).float() for num in cloud_points],
    }
    smooth = 0.98

    # evaluator
    label_names = list(dataset.label_to_names.values())
    evaluator = tw.evaluator.PointCloudSegmentEvaluator(cfg.num_classes, label_names)
    evaluator.reset()

    # create folder for every epoch
    root = tw.fs.mkdirs(f'{cfg.root}/val/epoch_{self.Epoch}_step_{self.Step}/')

    # start
    with torch.no_grad():

      for inputs in tqdm.tqdm(loader):

        # parse inputs
        input_points = [item.to(device) for item in inputs[0]]
        input_neighbors = [item.to(device) for item in inputs[1]]
        input_pools = [item.to(device) for item in inputs[2]]
        input_up_samples = [item.to(device) for item in inputs[3]]
        input_features = inputs[4].to(device)
        input_labels = inputs[5].to(device)
        input_queried = inputs[6].to(device)
        input_idx = inputs[7].to(device)

        # prediction
        with torch.cuda.amp.autocast():
          if cfg.model in ['randlanet', 'randlanet_plus']:
            preds = self.Model(input_points, input_neighbors, input_pools, input_up_samples, input_features)
          elif cfg.model in ['randlanet_multihead']:
            preds = self.Model(input_points, input_neighbors, input_pools, input_up_samples, input_features)
            preds = preds[-1]
          elif cfg.model.startswith('randlanet_stack'):
            preds = self.Model(input_points, input_neighbors, input_pools, input_up_samples, input_features)
            preds = preds[-1]
          else:
            raise NotImplementedError(cfg.model)

        # put batch into whole clouds
        for bs_id in range(preds.size(0)):
          cloud_idx = input_idx[bs_id]
          point_idx = input_queried[bs_id]
          results['preds'][cloud_idx][point_idx] = smooth * results['preds'][cloud_idx][point_idx] + (1 - smooth) * preds[bs_id].float()  # nopep8
          results['labels'][cloud_idx][point_idx] = input_labels[bs_id]
          results['counts'][cloud_idx][point_idx] += 1

    # concat all clouds into one
    results['preds'] = torch.cat(results['preds'], dim=0)
    results['labels'] = torch.cat(results['labels'], dim=0)
    results['counts'] = torch.cat(results['counts'], dim=0)

    # make sure every point should be visited at least 4 times.
    counts = results['counts'].reshape(-1)
    tw.logger.val(str((counts.unsqueeze(dim=1) == torch.unique(counts)[None]).sum(dim=0)))

    # save prediction results
    if cfg.dump:
      torch.save(results, f'{root}/prediction.pth')

    # accumulate iou
    evaluator.append(evaluator.compute(results['preds'].reshape(-1, cfg.num_classes), results['labels'].reshape(-1)))
    reports = evaluator.accumulate()
    logger.val(display_confusion_matrix(evaluator.confusion_matrix, label_names, column_width=10))
    elapsed = tw.timer.duration(start_time, tw.timer.tic())
    throughput = tw.timer.throughput(elapsed, total)
    keys = list(reports.keys()) + ['time', 'throughtput']
    vals = list(reports.values()) + [elapsed, throughput]
    tw.runner.log(keys=keys, values=vals, step=self.Step, epoch=self.Epoch, tag='val', writer=self.Writer)

    return reports

  def _test(self, **kwargs):
    """val (ref, distort)"""
    cfg = self.Config
    device = self.Config.device
    start_time = tw.timer.tic()
    total = 0

    # reset
    self.Model.eval()

    # build dataloader
    if 'loader' in kwargs and 'dataset' in kwargs:
      loader = kwargs['loader']
      dataset = kwargs['dataset']
    else:
      dataset = self._build_dataset(tw.phase.test)
      loader = self._build_dataloader(tw.phase.test, dataset)

    # sample a batch
    dataset.sample_an_epoch()

    # create folder for every epoch
    root = tw.fs.mkdirs(f'{cfg.root}/test/epoch_{self.Epoch}_step_{self.Step}/')
    results = []

    # start
    with torch.no_grad():

      for inputs in tqdm.tqdm(loader):

        # parse inputs
        input_points = [item.to(device) for item in inputs[0]]
        input_neighbors = [item.to(device) for item in inputs[1]]
        input_pools = [item.to(device) for item in inputs[2]]
        input_up_samples = [item.to(device) for item in inputs[3]]
        input_features = inputs[4].to(device)
        input_labels = inputs[5].to(device)
        input_queried = inputs[6].to(device)
        input_idx = inputs[7].to(device)

        # prediction
        with torch.cuda.amp.autocast():
          preds = self.Model(input_points, input_neighbors, input_pools, input_up_samples, input_features)

        if cfg.dump:
          results.append((preds.cpu(), input_labels.cpu(), input_queried.cpu(), input_idx.cpu(), input_features.cpu()))

    # save prediction results
    if cfg.dump:
      torch.save(results, f'{root}/prediction.pth')

    # accumulate iou
    elapsed = tw.timer.duration(start_time, tw.timer.tic())
    throughput = tw.timer.throughput(elapsed, total)
    keys = ['time', 'throughtput']
    vals = [elapsed, throughput]
    tw.runner.log(keys=keys, values=vals, step=self.Step, epoch=self.Epoch, tag='test', writer=self.Writer)

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

    else:
      raise NotImplementedError(cfg.task)


if __name__ == "__main__":
  # ---------------------------------------------
  #  USED BY COMMON
  # ---------------------------------------------
  parser = argparse.ArgumentParser()
  args, _ = parser.parse_known_args()

  # RuntimeError: cuDNN error: CUDNN_STATUS_NOT_SUPPORTED. This error may appear if you passed in a non-contiguous input.
  torch.backends.cudnn.enabled = False

  parser.add_argument('--task', type=str, default=None, choices=['train', 'val', 'test', 'viz', 'onnx', 'trt'])
  parser.add_argument('--dump', action='store_true', help="dump point cloud inference results.")
  parser.add_argument('--parallel', type=str, default='0', help="using data parallel to training.")

  # ---------------------------------------------
  #  DATASET
  # ---------------------------------------------
  parser.add_argument('--dataset', type=str, default=None)
  parser.add_argument('--dataset-original', type=str, default='_datasets/SensatUrban_Dataset/sensaturban/original_block_ply')  # nopep8
  parser.add_argument('--dataset-grid', type=str, default='_datasets/SensatUrban_Dataset/sensaturban/grid_0.200')
  parser.add_argument('--subset', type=str, default='', help='cambridge or birmingham')
  parser.add_argument('--num-classes', type=int, default=13)
  parser.add_argument('--noise-init', type=float, default=3.5)
  parser.add_argument('--num-points', type=int, default=65536)

  # ---------------------------------------------
  #  PHASE
  # ---------------------------------------------
  parser.add_argument('--train-batchsize', type=int, default=2)
  parser.add_argument('--train-steps', type=int, default=500)
  parser.add_argument('--train-epoch', type=int, default=100)
  parser.add_argument('--val-batchsize', type=int, default=14)
  parser.add_argument('--val-steps', type=int, default=100)

  # ---------------------------------------------
  #  MODEL
  # ---------------------------------------------
  parser.add_argument('--knn-num', type=int, default=16)
  parser.add_argument('--num-layers', type=int, default=5)
  parser.add_argument('--sub-sampling-ratio', default=[4, 4, 4, 4, 2])
  parser.add_argument('--decoder-feature-dims', default=[16, 64, 128, 256, 512])

  parser.add_argument('--model', type=str, default=None)
  parser.add_argument('--model-path', type=str, default=None, help="loadding pretrain/last-checkpoint model.")
  parser.add_argument('--model-source', type=str, default=None)

  # ---------------------------------------------
  #  OPTIMIZATION
  # ---------------------------------------------
  parser.add_argument('--lr', type=float, default=1e-2)
  parser.add_argument('--lr-schedule', type=str, default='poly')
  parser.add_argument('--lr-decay', type=float, default=0.95)

  # ---------------------------------------------
  #  USED BY LOGGER
  # ---------------------------------------------
  parser.add_argument('--log', type=int, default=10, help="display interval step.")
  parser.add_argument('--log-val', type=int, default=50, help="running validation in terms of step.")
  parser.add_argument('--log-test', type=int, default=None, help="running test in terms of step.")
  parser.add_argument('--log-save', type=int, default=50, help="saveing checkpoint with interval.")

  # ---------------------------------------------
  #  USED BY VIZ-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--viz-input', type=str, default='viz.txt', help='input path could be a folder/filepath.')
  parser.add_argument('--viz-output', type=str, help='output path should be a folder path.')

  tw.runner.launch(parser, SensatUrban)
