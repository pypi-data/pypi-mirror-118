# Copyright 2018 The KaiJIN Authors. All Rights Reserved.
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
"""Quality Assessment Common Code
"""
import functools
import cv2
import torch
import tw
import copy
import numpy as np
from tw import logger
from tw import transform as T

#!<----------------------------------------------------------------------------
#!< AUGMENTATION
#!<----------------------------------------------------------------------------


def transform_train(metas, config):
  T.change_colorspace(metas, T.COLORSPACE.BGR, T.COLORSPACE.RGB)
  T.random_hflip(metas)
  # if config.dataset in ['KonIQ10k']:
  #   T.resize(metas, 384, 512)
  if config.dataset in ['BID']:
    T.resize(metas, 512, 512)
  if config.dataset in ['FLIVE']:
    T.pad_to_target_size(metas, 640, 640, fill_value=250, mode='center')
  # else:
  #   T.random_crop(metas, config.input_height, config.input_width)

  # T.to_tensor(metas, scale=255, mean=[0.485, 0.456, 0.406], std=(0.229, 0.224, 0.225))
  T.to_tensor(metas, scale=255, mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
  # T.to_tensor(metas, scale=255)
  return metas


def transform_val(metas, config):
  T.change_colorspace(metas, T.COLORSPACE.BGR, T.COLORSPACE.RGB)
  # if config.dataset in ['KonIQ10k']:
  #   T.resize(metas, 384, 512)
  # elif config.dataset in ['BID']:
  #   T.resize(metas, 512, 512)
  if config.dataset not in ['FLIVE']:
    # T.random_crop(metas, config.input_height, config.input_width)
    T.center_crop(metas, config.input_height, config.input_width)
  # T.to_tensor(metas, scale=255, mean=[0.485, 0.456, 0.406], std=(0.229, 0.224, 0.225))
  T.to_tensor(metas, scale=255, mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
  # T.to_tensor(metas, scale=255)
  return metas


def transform_patch_to_global(metas, config):
  T.change_colorspace(metas, T.COLORSPACE.BGR, T.COLORSPACE.RGB)
  assert config.dataset in ['FLIVE']
  T.pad_to_square(metas, fill_value=0)
  T.to_tensor(metas, scale=255, mean=[0.485, 0.456, 0.406], std=(0.229, 0.224, 0.225))
  return metas


def transform_normalize(metas, config):
  T.change_colorspace(metas, T.COLORSPACE.BGR, T.COLORSPACE.RGB)
  T.to_tensor(metas, scale=255.0)
  return metas

#!<----------------------------------------------------------------------------
#!< PATCH DATASET
#!<----------------------------------------------------------------------------


class RepeatDataset(torch.utils.data.Dataset):

  """repeat dataset

    For train:
      [c, h, w] image tensor

    For val/test:
      [n, c, h, w] all repeat image in a tensor

  """

  def __init__(self, dataset: torch.utils.data.Dataset, phase: tw.phase, repeat=1, blind_mode=True, **kwargs):
    super(RepeatDataset, self).__init__()
    self.dataset = dataset
    self.repeat = repeat
    self.phase = phase
    self.blind_mode = blind_mode

  def __len__(self):
    if self.phase == tw.phase.train:
      return len(self.dataset) * self.repeat
    else:
      return len(self.dataset)

  def __getitem__(self, idx):
    """get item"""

    if self.phase == tw.phase.train:
      index = int(idx / self.repeat)

      if self.blind_mode:
        distort_meta = self.dataset[index][0]
        return distort_meta.bin, distort_meta.label
      else:
        image_meta, distort_meta = self.dataset[index]
        return image_meta.bin, distort_meta.bin, distort_meta.label

    else:
      index = idx

      if self.blind_mode:
        distort = []
        for _ in range(self.repeat):
          metas = self.dataset[index]
          distort.append(metas[0].bin)
          distort_label = metas[0].label
          distort_path = metas[0].path
        distort = torch.stack(distort, dim=0)
        return distort, distort_label, distort_path

      else:
        ref, distort = [], []
        for _ in range(self.repeat):
          metas = self.dataset[index]
          ref.append(metas[0].bin)
          ref_path = metas[0].path
          distort.append(metas[1].bin)
          distort_label = metas[1].label
          distort_path = metas[1].path
        distort = torch.stack(distort, dim=0)
        ref = torch.stack(ref, dim=0)
        return ref, distort, distort_label, distort_path, ref_path


class PatchDataset(torch.utils.data.Dataset):

  """Image to patch

    For train:
      [c, patch_size, patch_size] a patch

    For val/test:
      [n, c, patch_size, patch_size] all patches in a image

  """

  def __init__(self, dataset: torch.utils.data.Dataset, phase: tw.phase,
               patch_size=32, stride=32, blind_mode=True, **kwargs):
    super(PatchDataset, self).__init__()
    targets = []
    self.phase = phase
    self.blind_mode = blind_mode

    if blind_mode:
      for i in range(len(dataset)):
        distort_meta: T.ImageMeta = dataset[i][0]
        distort_patches = T.non_overlap_crop_patch(distort_meta.bin, patch_size, stride)
        if phase == tw.phase.train:
          for p in distort_patches:
            meta = copy.copy(distort_meta)
            meta.bin = self.transform(p)
            targets.append([meta])
        else:
          meta = copy.copy(distort_meta)
          meta.bin = torch.stack([self.transform(p) for p in distort_patches], dim=0)
          targets.append([meta])

    else:
      for i in range(len(dataset)):
        image_meta, distort_meta = dataset[i]
        distort_patches = T.non_overlap_crop_patch(distort_meta.bin, patch_size, stride)
        image_patches = T.non_overlap_crop_patch(image_meta.bin, patch_size, stride)
        if phase == tw.phase.train:
          for ip, dp in zip(image_patches, distort_patches):
            ip_meta = copy.copy(image_meta)
            dp_meta = copy.copy(distort_meta)
            ip_meta.bin = self.transform(ip)
            dp_meta.bin = self.transform(dp)
            targets.append([ip_meta, dp_meta])
        else:
          ip_meta = copy.copy(image_meta)
          dp_meta = copy.copy(distort_meta)
          ip_meta.bin = torch.stack([self.transform(p) for p in image_patches], dim=0)
          dp_meta.bin = torch.stack([self.transform(p) for p in distort_patches], dim=0)
          targets.append([ip_meta, dp_meta])

    self.targets = targets
    tw.logger.info('Totally collect %d patches.' % len(self.targets))

  def transform(self, patch):
    raw = patch[0].numpy()  # [1, h, w] -> [h, w]
    raw = T.local_constrast_normalize(raw, p=3, q=3, c=1)
    return torch.from_numpy(raw)[None]

  def __len__(self):
    return len(self.targets)

  def __getitem__(self, idx):
    if self.blind_mode:
      if self.phase == tw.phase.train:
        return self.targets[idx][0].bin, self.targets[idx][0].label
      else:
        return self.targets[idx][0].bin, self.targets[idx][0].label, self.targets[idx][0].path
    else:
      if self.phase == tw.phase.train:
        return self.targets[idx][0].bin, self.targets[idx][1].bin, self.targets[idx][1].label
      else:
        return self.targets[idx][0].bin, self.targets[idx][1].bin, self.targets[idx][1].label, self.targets[idx][1].path


#!<----------------------------------------------------------------------------
#!< DATASET
#!<----------------------------------------------------------------------------

def build_dataset(config, phase: tw.phase, blind_mode=False, **kwargs):
  """build quality assessment datasets

  Args:
      config ([type]): argparse
      phase (tw.phase): phase
      blind_mode ([bool]): if only using distort image and labels

  Returns:
      torch.utils.data.dataloader:
  """

  if config.model in ['ssim', 'ms_ssim', 'cw_ssim', 'psnr', 'gmsd', 'nlpd',
                      'fsim', 'vsi', 'vif', 'vifs', 'mad', 'lpips', 'dists',
                      'base.cnn']:
    trans_trn = functools.partial(transform_normalize, config=config)
    trans_val = functools.partial(transform_normalize, config=config)
  else:
    trans_trn = functools.partial(transform_train, config=config)
    trans_val = functools.partial(transform_val, config=config)

  if config.dataset == 'PIPAL':
    if phase == tw.phase.train:
      split = (0, 180)
      dataset = tw.datasets.PIPAL(config.dataset_train, trans_trn, tw.phase.train, split=split, blind_mode=blind_mode)
    elif phase == tw.phase.val:
      split = (180, 200)
      dataset = tw.datasets.PIPAL(config.dataset_val, trans_val, tw.phase.train, split=split, blind_mode=blind_mode)
    elif phase == tw.phase.test:
      split = (180, 200)
      dataset = tw.datasets.PIPAL(config.dataset_test, trans_val, tw.phase.test, split=split, blind_mode=blind_mode)

  elif config.dataset == 'TID2013':
    if phase == tw.phase.train:
      split = [i for i in range(0, 20)]
      dataset = tw.datasets.TID2013(config.dataset_train, trans_trn, split=split, blind_mode=blind_mode)
    elif phase == tw.phase.val:
      split = [i for i in range(20, 25)]
      dataset = tw.datasets.TID2013(config.dataset_val, trans_val, split=split, blind_mode=blind_mode)
    elif phase == tw.phase.test:
      split = [i for i in range(20, 25)]
      dataset = tw.datasets.TID2013(config.dataset_test, trans_val, split=split, blind_mode=blind_mode)

  elif config.dataset == 'KonIQ10k':
    if phase == tw.phase.train:
      dataset = tw.datasets.KonIQ10k(config.dataset_train, trans_trn, phase=tw.phase.train)
    elif phase == tw.phase.val:
      dataset = tw.datasets.KonIQ10k(config.dataset_val, trans_val, phase=tw.phase.test)
    elif phase == tw.phase.test:
      dataset = tw.datasets.KonIQ10k(config.dataset_test, trans_val, phase=tw.phase.test)

  elif config.dataset == 'LIVEC':
    if phase == tw.phase.train:
      split = [i for i in range(0, 930)]
      dataset = tw.datasets.LIVEC(config.dataset_train, trans_trn, split=split, blind_mode=blind_mode)
    elif phase == tw.phase.val:
      split = [i for i in range(930, 1162)]
      dataset = tw.datasets.LIVEC(config.dataset_val, trans_val, split=split, blind_mode=blind_mode)
    elif phase == tw.phase.test:
      split = [i for i in range(930, 1162)]
      dataset = tw.datasets.LIVEC(config.dataset_test, trans_val, split=split, blind_mode=blind_mode)

  elif config.dataset == 'LIVEMD':
    if phase == tw.phase.train:
      split = [i for i in range(0, 12)]
      dataset = tw.datasets.LIVEMD(config.dataset_train, trans_trn, split=split, blind_mode=blind_mode)
    elif phase == tw.phase.val:
      split = [i for i in range(12, 15)]
      dataset = tw.datasets.LIVEMD(config.dataset_val, trans_val, split=split, blind_mode=blind_mode)
    elif phase == tw.phase.test:
      split = [i for i in range(12, 15)]
      dataset = tw.datasets.LIVEMD(config.dataset_test, trans_val, split=split, blind_mode=blind_mode)

  elif config.dataset == 'LIVE2005':
    if phase == tw.phase.train:
      split = [i for i in range(0, 23)]
      dataset = tw.datasets.LIVE2005(config.dataset_train, trans_trn, split=split, blind_mode=blind_mode)
    elif phase == tw.phase.val:
      split = [i for i in range(23, 29)]
      dataset = tw.datasets.LIVE2005(config.dataset_val, trans_val, split=split, blind_mode=blind_mode)
    elif phase == tw.phase.test:
      split = [i for i in range(23, 29)]
      dataset = tw.datasets.LIVE2005(config.dataset_test, trans_val, split=split, blind_mode=blind_mode)

  elif config.dataset == 'CSIQ':
    if phase == tw.phase.train:
      split = [i for i in range(24)]
      dataset = tw.datasets.CSIQ(config.dataset_train, trans_trn, split=split, blind_mode=blind_mode)
    elif phase == tw.phase.val:
      split = [i for i in range(24, 30)]
      dataset = tw.datasets.CSIQ(config.dataset_val, trans_val, split=split, blind_mode=blind_mode)
    elif phase == tw.phase.test:
      split = [i for i in range(24, 30)]
      dataset = tw.datasets.CSIQ(config.dataset_test, trans_val, split=split, blind_mode=blind_mode)

  elif config.dataset == 'FLIVE':
    if phase == tw.phase.train:
      dataset = tw.datasets.FLIVE(config.dataset_train, trans_trn, phase=phase)
    elif phase == tw.phase.val:
      dataset = tw.datasets.FLIVE(config.dataset_val, trans_val, phase=phase)
    elif phase == tw.phase.test:
      dataset = tw.datasets.FLIVE(config.dataset_test, trans_val, phase=phase)

  else:
    raise NotImplementedError

  if config.model in ['base.cnn']:
    dataset = PatchDataset(dataset, phase, blind_mode=blind_mode)
    collate_fn = None
  elif config.model.startswith('patchiqa'):
    if phase == tw.phase.train:
      collate_fn = tw.datasets.SampleCollator()
    else:
      dataset = RepeatDataset(dataset, phase, repeat=1, blind_mode=True)
      collate_fn = None
  else:
    if phase == tw.phase.train:
      repeat = config.train_repeat
    elif phase == tw.phase.val:
      repeat = config.val_repeat
    elif phase == tw.phase.test:
      repeat = config.test_repeat
    dataset = RepeatDataset(dataset, phase, repeat=repeat, blind_mode=blind_mode)
    collate_fn = None

  if phase == tw.phase.train:
    return torch.utils.data.DataLoader(
        dataset=dataset,
        batch_size=config.train_batchsize,
        shuffle=True,
        num_workers=4,
        collate_fn=collate_fn,
        pin_memory=False,
        drop_last=True)

  else:
    return torch.utils.data.DataLoader(
        dataset=dataset,
        batch_size=1,
        shuffle=False,
        num_workers=4,
        collate_fn=collate_fn,
        pin_memory=False,
        drop_last=False)


def build_argparse(parser):

  # ---------------------------------------------
  #  USED BY COMMON
  # ---------------------------------------------
  parser.add_argument('--task', type=str, default=None, choices=['train', 'val', 'test', 'viz', 'onnx', 'trt'])
  parser.add_argument('--dataset', type=str, default=None)
  parser.add_argument('--dataset-train', type=str, default=None)
  parser.add_argument('--dataset-val', type=str, default=None)
  parser.add_argument('--dataset-test', type=str, default=None)
  parser.add_argument('--train-repeat', type=int, default=1, help="repeat dataset during training.")
  parser.add_argument('--val-repeat', type=int, default=1, help="repeat dataset during validation.")
  parser.add_argument('--test-repeat', type=int, default=1, help="repeat dataset during testing.")

  # ---------------------------------------------
  #  USED BY LOGGER
  # ---------------------------------------------
  parser.add_argument('--log', type=int, default=10, help="display interval step.")
  parser.add_argument('--log-val', type=int, default=50, help="running validation in terms of step.")
  parser.add_argument('--log-test', type=int, default=None, help="running test in terms of step.")
  parser.add_argument('--log-save', type=int, default=50, help="saveing checkpoint with interval.")

  # ---------------------------------------------
  #  USED BY MODEL-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--model', type=str, default=None, help="IQA evaluator.")
  parser.add_argument('--model-path', type=str, default=None, help="loadding pretrain/last-checkpoint model.")
  parser.add_argument('--model-source', type=str, default=None)

  # ---------------------------------------------
  #  USED BY INPUT-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--input-colorspace', type=str, default='RGB', choices=['Y', 'RGB', 'YUV'])
  parser.add_argument('--input-height', type=int, default=224, help='network input height.')
  parser.add_argument('--input-width', type=int, default=224, help='network input wdith.')

  # ---------------------------------------------
  #  USED BY TRAIN-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--train-batchsize', type=int, default=32, help="total batch size across devices.")
  parser.add_argument('--train-epoch', type=int, default=100, help="total training epochs.")

  # ---------------------------------------------
  #  USED BY VIZ-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--viz-input', type=str, default='viz.txt', help='input path could be a folder/filepath.')
  parser.add_argument('--viz-output', type=str, help='output path should be a folder path.')
