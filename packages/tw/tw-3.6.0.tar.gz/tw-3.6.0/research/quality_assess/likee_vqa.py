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
"""LikeeVQA

  Input: [N, D, C, H, W]
  Output: [N, 5]

"""
import os
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

import models


class VqaModelWrapper(nn.Module):

  r"""Compose model module for different training type.
  """

  def __init__(self, net_e: nn.Module = None):
    super(VqaModelWrapper, self).__init__()
    self.netE = net_e


class VideoLabelDataset(torch.utils.data.Dataset):

  def __init__(self, path, label_type, transform,
               phase=tw.phase.train, interval=1, length=30,
               **kwargs):
    # check
    assert interval >= 1
    assert length >= 1
    assert label_type in [float, int]
    tw.fs.raise_path_not_exist(path)
    self.phase = phase
    self.interval = interval
    self.length = length

    # parse
    res, _ = tw.parser.parse_from_text(path, [str, label_type], [True, False])
    self.targets = []
    for path, label in zip(res[0], res[1]):
      self.targets.append((path, label))

    self.transform = transform
    tw.logger.info(f'Totally loading {len(self.targets)} samples.')

  def __len__(self):
    return len(self.targets)

  def __getitem__(self, idx):
    """sample a short of sequence"""
    try:
      path, label = self.targets[idx]

      if self.phase == tw.phase.train:
        # random sample
        pass

      else:
        reader = tw.media.VideoReader(path)

        # actually cover length
        size = self.interval * self.length
        if size >= reader.count:
          interval = reader.count // self.length
        else:
          interval = self.interval

        seqs = []
        for i, src in enumerate(reader):
          if i % interval == 0:
            seqs.append(src)
          if len(seqs) == self.length:
            break
        vid_meta = T.VideoMeta(binary=seqs)
        vid_meta.numpy()
        vid_meta.label = label
        vid_meta.path = path

      return self.transform([vid_meta])

    except:
      return self.__getitem__(idx + 1)


class LikeeVqa():

  def __init__(self, config):
    self.Config = config

    # overwrite when dist
    if self.Config.dist_size > 1:
      self.Config.device = 'cuda:{}'.format(self.Config.dist_rank)
    self.Master = True if self.Config.dist_rank == 0 else False

    # evaluator
    self.Evaluator = tw.evaluator.ConfusionMatrixEvaluator(num_classes=5)
    self.Evaluator.to(self.Config.device)

    # evaluation and tensorboard
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

  def _build_dataset(self, phase: tw.phase):
    """vqa requires a sequence
    """
    cfg = self.Config

    # build target dataset
    if phase == tw.phase.train:
      return VideoLabelDataset(path=cfg.dataset_val,
                               label_type=int,
                               transform=self.transform_yuv_val,
                               phase=tw.phase.train,
                               interval=cfg.input_interval,
                               length=cfg.input_length)

    elif phase == tw.phase.val and self.Master:
      return VideoLabelDataset(path=cfg.dataset_val,
                               label_type=int,
                               transform=self.transform_yuv_val,
                               phase=tw.phase.val,
                               interval=cfg.input_interval,
                               length=cfg.input_length)

    raise NotImplementedError

  def transform_yuv_train(self, metas):
    """transform"""
    if self.Config.input_colorspace in ['YUV', 'Y']:
      T.change_colorspace(metas, T.COLORSPACE.BGR, T.COLORSPACE.BT709_FULLRANGE)
    elif self.Config.input_colorspace in ['RGB']:
      T.change_colorspace(metas, T.COLORSPACE.BGR, T.COLORSPACE.RGB)
    else:
      raise NotImplementedError(self.Config.input_colorspace)
    T.to_tensor(metas, scale=255.0)
    return metas

  def transform_yuv_val(self, metas):
    """transform"""
    if self.Config.input_colorspace in ['YUV', 'Y']:
      T.change_colorspace(metas, T.COLORSPACE.BGR, T.COLORSPACE.BT709_FULLRANGE)
    elif self.Config.input_colorspace in ['RGB']:
      T.change_colorspace(metas, T.COLORSPACE.BGR, T.COLORSPACE.RGB)
    else:
      raise NotImplementedError(self.Config.input_colorspace)
    T.shortside_resize(metas, min_size=224)
    T.center_crop(metas, 224, 224)
    T.to_tensor(metas, scale=255.0, mean=[0.485, 0.456, 0.406], std=[0.299, 0.224, 0.225])
    return metas

  def _train(self, **kwargs):
    """train likee vqa pipeline"""
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

  def _val(self, **kwargs):
    """ validation
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
      val_loader = kwargs['loader']
    else:
      val_loader = self._build_dataloader(tw.phase.val, self._build_dataset(tw.phase.val))

    # create folder for every epoch
    root = tw.fs.mkdirs(f'{cfg.root}/val/epoch_{self.Epoch}_step_{self.Step}/')

    # start
    with torch.no_grad():
      for samples in tqdm.tqdm(val_loader):
        total += len(samples)

        # convert data into tensor
        vids, labels, paths = [], [], []
        for sample in samples:
          if cfg.input_colorspace in ['RGB', 'YUV']:
            vids.append(sample[0].bin.float().to(device))
          elif cfg.input_colorspace in ['Y']:
            vids.append(sample[0].bin[:, 0].unsqueeze(dim=1).float().to(device))
          else:
            raise NotImplementedError(cfg.input_colorspace)
          labels.append(sample[0].label)
          paths.append(sample[0].path)

        # [N, C, D, H, W]
        vids = torch.stack(vids, dim=0).float().to(device).permute(0, 2, 1, 3, 4)
        labels = torch.tensor(labels).long().to(device)

        # inference
        outputs = self.Model.netE(vids)

        # eval
        metrics = self.Evaluator.compute(outputs, labels)
        self.Evaluator.append(metrics)

    # stat
    reports = self.Evaluator.accumulate()
    elapsed = tw.timer.duration(start_time, tw.timer.tic())
    throughput = tw.timer.throughput(elapsed, total)
    keys = list(reports.keys()) + ['time', 'throughtput']
    vals = list(reports.values()) + [elapsed, throughput]
    tw.runner.log(keys=keys, values=vals, step=self.Step, epoch=self.Epoch, tag='val', writer=self.Writer)

  def _transform(self, seqs, dsize=224):
    """transform a video sequence

    Args:
        seqs (torch.Tensor): a video clip with [D, C, H, W] format
        dsize (int, optional): Defaults to 224.

    Returns:
        [torch.Tensor]: normalized [D, C, 224, 224]
    """
    assert seqs.ndim == 4, "require input to be [D, C, H, W]"
    d, c, h, w = seqs.shape

    # 1. resize
    if w < h:
      ow = dsize
      oh = int(dsize * h / w)
    else:
      oh = dsize
      ow = int(dsize * w / h)

    seqs = seqs.reshape(d, c, h, w)
    seqs = nn.functional.interpolate(seqs, size=[oh, ow], mode='bilinear', align_corners=False)

    # 2. center crop
    if ow < oh:
      s = (oh - ow) // 2
      seqs = seqs[:, :, s: s + ow, :]
    else:
      s = (ow - oh) // 2
      seqs = seqs[:, :, :, s: s + oh]

    # 3. normalize
    mean = torch.tensor([0.485, 0.456, 0.406]).reshape(1, 3, 1, 1)
    std = torch.tensor([0.299, 0.224, 0.225]).reshape(1, 3, 1, 1)
    seqs = (seqs / 255.0 - mean) / std

    # 4. reshape
    seqs = torch.reshape(seqs, [n, d, c, dsize, dsize])
    return seqs

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
    _, videos = tw.media.collect(viz_input)
    if not os.path.exists(viz_output):
      os.makedirs(viz_output)
    if len(videos) == 0:
      raise ValueError("without finding any videos.")

    # to eval
    self.Model.eval()

    # process video
    for filepath in sorted(videos):
      reader = tw.media.VideoReader(filepath, to_rgb=False, to_tensor=False)
      seqs = []
      for i, src in enumerate(reader):
        if i % cfg.input_interval == 0:
          seqs.append(src)
        if len(seqs) == cfg.input_length:
          break
      vid_meta = T.VideoMeta(binary=seqs)
      sample = self.transform_yuv_val([vid_meta])
      inputs = sample[0].bin.float().to(device).unsqueeze(dim=0).permute(0, 2, 1, 3, 4)
      results = self.Model.netE(inputs)
      coeff = torch.arange(0, 5, 1).to(device).reshape(1, 5)
      print(filepath, (results * coeff).sum().mul(0.25).item(), results.cpu().numpy())

  def _build_model(self):
    """build model
    """
    cfg = self.Config

    # different input format
    if self.Config.input_colorspace in ['Y']:
      in_channels = 1
    elif self.Config.input_colorspace in ['RGB', 'YUV']:
      in_channels = 3
    else:
      raise NotImplementedError

    # build encoder
    if cfg.model_encoder == 'VNIMA.MobileNet':
      backbone = tw.models.mobilenet_v2.mobilenet_v2()
      netE = models.VNIMA(backbone, fc_in=1280, num_classes=5)
    else:
      netE = None

    model = VqaModelWrapper(net_e=netE)
    model.to(cfg.device)

    return model

  def _build_optim(self, model: nn.Module):
    """build optimizer"""
    cfg = self.Config
    optim = {}

    if cfg.train_optimizer == 'adam':
      optim['E'] = torch.optim.Adam([{'params': model.netE.parameters(), 'lr': cfg.train_lr}])

    elif cfg.train_optimizer == 'sgd':
      optim['E'] = torch.optim.SGD([{'params': model.netE.parameters(), 'lr': cfg.train_lr, 'momentum': 0.9}])

    else:
      raise NotImplementedError(cfg.train_optimizer)

    return optim

  def _dump(self):
    """dump current checkpoint
    """
    cfg = self.Config
    path = f'{cfg.root}/model.epoch-{self.Epoch}.step-{self.Step}.pth'

    torch.save({
        'state_dict': self.Model.state_dict(),
        'global_step': self.Step,
        'global_epoch': self.Epoch,
        'optimizer': {k: v.state_dict() for k, v in self.Optim.items()}
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

      if cfg.task == 'train':
        for k in self.Optim:
          self.Optim[k].load_state_dict(ckpt['optimizer'][k])

      if 'global_step' in ckpt:
        self.Step = ckpt['global_step']

      if 'global_epoch' in ckpt:
        self.Epoch = ckpt['global_epoch']

    elif cfg.model_source == 'vanilla':
      tw.checkpoint.load_matched_state_dict(self.Model, ckpt['state_dict'])

    elif cfg.model_source == 'thea-v1':
      content = tw.checkpoint.replace_prefix(ckpt, 'module.', '')
      content = tw.checkpoint.add_prefix(content, 'netE.')
      tw.checkpoint.load_matched_state_dict(self.Model, content)

    else:
      raise NotImplementedError(cfg.model_source)

  def _build_dataloader(self, phase: tw.phase, dataset):
    """ build data loader
    """
    cfg = self.Config

    if phase == tw.phase.train:
      return torch.utils.data.DataLoader(
          dataset=dataset,
          batch_size=cfg.train_batchsize,
          shuffle=True,
          num_workers=8,
          collate_fn=tw.datasets.SampleCollator(),
          pin_memory=True,
          drop_last=True)

    elif phase == tw.phase.val:
      return torch.utils.data.DataLoader(
          dataset=dataset,
          batch_size=cfg.val_batchsize,
          shuffle=False,
          num_workers=16,
          collate_fn=tw.datasets.SampleCollator(),
          pin_memory=False,
          drop_last=True)

    raise NotImplementedError

  def _tensorrt(self, **kwargs):
    """export to tensorrt models
    """
    cfg = self.Config
    tw.export.onnx_to_trt(
        cfg.model_encoder + '.onnx',
        cfg.model_encoder + '.engine',
        shapes={'input': {'min': (1, 30, 3, 32, 32),
                          'best': (1, 30, 3, 640, 360),
                          'max': (1, 30, 3, 1024, 1024)}},
        verbose=True)

  def _onnx(self, **kwargs):
    """export model to onnx
    """
    cfg = self.Config

    inputs = torch.rand(1, 30, 3, 640, 360).to(cfg.device)
    tw.flops.register(self.Model.netG)
    with torch.no_grad():
      self.Model.netE(inputs)
    print(tw.flops.accumulate(self.Model.netE))
    tw.flops.unregister(self.Model.netE)

    tw.export.torch_to_onnx(self.Model.netE.eval(),
                            torch.rand(1, 30, 3, 640, 360).to(cfg.device),
                            cfg.model_encoder + '.onnx',
                            input_names=['input', ],
                            output_names=['output', ],
                            dynamic_axes={'input': {0: 'batch', 1: 'depth', 3: 'height', 4: 'width'}})

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
  parser.add_argument('--task', type=str, default=None, choices=['train', 'val', 'test', 'viz', 'onnx', 'trt'])
  parser.add_argument('--dataset-train', type=str, default='_datasets/BigoliveGameSR/PAPER.protocal.txt')
  parser.add_argument('--dataset-val', type=str, default='_datasets/BigoliveGameSR/PAPER.protocal.txt')
  parser.add_argument('--dataset-test', type=str, default='_datasets/BigoliveGameSRNewTest/combine')

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
  parser.add_argument('--model-encoder', type=str, default=None)
  parser.add_argument('--model-path', type=str, default=None, help="loadding pretrain/last-checkpoint model.")
  parser.add_argument('--model-source', type=str, default=None)

  # ---------------------------------------------
  #  USED BY INPUT-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--input-colorspace', type=str, default='Y', choices=['Y', 'RGB', 'YUV'])
  parser.add_argument('--input-interval', type=int, default=3, help="sampling interval")
  parser.add_argument('--input-length', type=int, default=30, help="sequence length to group a sample.")

  # ---------------------------------------------
  #  USED BY TRAIN-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--train-lr', type=float, default=0.0001, help="total learning rate across devices.")
  parser.add_argument('--train-batchsize', type=int, default=4, help="total batch size across devices.")
  parser.add_argument('--train-epoch', type=int, default=100000, help="total training epochs.")
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

  # generate config
  args, _ = parser.parse_known_args()

  # runner
  tw.runner.launch(parser, LikeeVqa)
