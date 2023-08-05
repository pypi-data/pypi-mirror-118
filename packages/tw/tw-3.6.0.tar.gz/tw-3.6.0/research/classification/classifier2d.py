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
r"""classifier"""
import math
import argparse
import tqdm
import functools
import cv2

import torch
from torch import nn

from torch.utils import data, tensorboard

import tw
from tw import logger
from tw import transform as T


class FastLoader(torch.utils.data.Dataset):
  """convert tw meta into tensor directly. cache the val/test dataset for next
    loader.
  """

  def __init__(self, dataset: torch.utils.data.Dataset, **kwargs):
    # store dataset
    self.dataset = dataset
    tw.logger.info('Total loading {} samples.'.format(len(self)))

  def __len__(self):
    return len(self.dataset)

  def __getitem__(self, idx):
    img_meta = self.dataset[idx][0]
    return img_meta.bin, img_meta.label


class Classifier2d():

  def __init__(self, config):
    """classification for 2d image.
    """
    self.Config = config

    # overwrite when dist
    if self.Config.dist_size > 1:
      self.Config.device = 'cuda:{}'.format(self.Config.dist_rank)
    self.Master = True if self.Config.dist_rank == 0 else False

    # evaluation and tensorboard
    self.Evaluator = tw.evaluator.TopkEvaluator(topk=5)
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
      self.Model = torch.nn.SyncBatchNorm.convert_sync_batchnorm(self.Model)
      self.Model = torch.nn.parallel.DistributedDataParallel(self.Model, device_ids=[self.Config.dist_rank])

  def _build_dataset(self, phase: tw.phase):
    """build train/val datasets
    """
    cfg = self.Config

    # build target datasets
    if phase == tw.phase.train:
      if cfg.dataset == 'Mnist':
        dataset = tw.datasets.Mnist(
            path='_datasets/classification/mnist/train.txt',
            transform=self._transform_cifar_train)
      elif cfg.dataset == 'Cifar10':
        dataset = tw.datasets.Cifar10(
            path='_datasets/classification/cifar-10-batches-py/',
            transform=self._transform_cifar_train,
            phase=tw.phase.train)
      elif cfg.dataset == 'ImageNet':
        dataset = tw.datasets.ImageNet(
            path='_datasets/classification/ImageNet/train.txt',
            transform=self._transform_vgg_train)

    elif phase == tw.phase.val:
      if cfg.dataset == 'Mnist':
        dataset = tw.datasets.Mnist(
            path='_datasets/classification/mnist/test.txt',
            transform=self._transform_cifar_val)
      elif cfg.dataset == 'Cifar10':
        dataset = tw.datasets.Cifar10(
            path='_datasets/classification/cifar-10-batches-py/',
            transform=self._transform_cifar_val,
            phase=tw.phase.val)
      elif cfg.dataset == 'ImageNet':
        trans = functools.partial(self._transform_vgg_val, 
                                  size=self.Model.SIZE,
                                  crop_ratio=self.Model.CROP,
                                  scale=self.Model.SCALE,
                                  mean=self.Model.MEAN,
                                  std=self.Model.STD)
        dataset = tw.datasets.ImageNet(path='_datasets/ImageNet/val.txt', transform=trans)

    # build fast loader
    dataset = FastLoader(dataset)

    # build data loader
    if phase == tw.phase.train:
      return torch.utils.data.DataLoader(
          dataset=dataset,
          batch_size=cfg.train_batchsize,
          shuffle=True,
          num_workers=8,
          collate_fn=None,
          pin_memory=False,
          drop_last=True)

    elif phase == tw.phase.val:
      return torch.utils.data.DataLoader(
          dataset=dataset,
          batch_size=cfg.val_batchsize,
          shuffle=False,
          num_workers=8,
          collate_fn=None,
          pin_memory=False,
          drop_last=False)

    raise NotImplementedError

  def _build_optim(self, model: nn.Module):
    """build optimizer
    """
    cfg = self.Config

    if cfg.train_optimizer == 'adam':
      return torch.optim.Adam([{'params': model.parameters(), 'lr': cfg.train_lr}])

    elif cfg.train_optimizer == 'sgd':
      return torch.optim.SGD([{'params': model.parameters(), 'lr': cfg.train_lr, 'momentum': 0.9}])

    else:
      raise NotImplementedError(cfg.train_optimizer)

  def _build_model(self):
    """build model
    """
    cfg = self.Config
    
    models = {
      # 'lenet': tw.models.lenet.lenet,
      'alexnet': tw.models.alexnet.alexnet,
      'vgg11': tw.models.vgg.vgg11,
      'vgg13': tw.models.vgg.vgg13,
      'vgg16': tw.models.vgg.vgg16,
      'vgg19': tw.models.vgg.vgg19,
      'vgg11_bn': tw.models.vgg.vgg11_bn,
      'vgg13_bn': tw.models.vgg.vgg13_bn,
      'vgg16_bn': tw.models.vgg.vgg16_bn,
      'vgg19_bn': tw.models.vgg.vgg19_bn,
      'densenet121': tw.models.densenet.densenet121,
      'densenet161': tw.models.densenet.densenet161,
      'densenet169': tw.models.densenet.densenet169,
      'densenet201': tw.models.densenet.densenet201,
      'googlenet': tw.models.googlenet.googlenet,

      'resnet18': tw.models.resnet.resnet18,
      'resnet34': tw.models.resnet.resnet34,
      'resnet50': tw.models.resnet.resnet50,
      'resnet101': tw.models.resnet.resnet101,
      'resnet152': tw.models.resnet.resnet152,
      'resnext50_32x4d': tw.models.resnet.resnext50_32x4d,
      'resnext101_32x8d': tw.models.resnet.resnext101_32x8d,

      'wide_resnet50_2': tw.models.resnet.wide_resnet50_2,
      'wide_resnet101_2': tw.models.resnet.wide_resnet101_2,

      'squeezenet1_0': tw.models.squeezenet.squeezenet1_0,
      'squeezenet1_1': tw.models.squeezenet.squeezenet1_1,

      'shufflenet_v2_x0_5': tw.models.shufflenet_v2.shufflenet_v2_x0_5,
      'shufflenet_v2_x1_0': tw.models.shufflenet_v2.shufflenet_v2_x1_0,
      'shufflenet_v2_x1_5': tw.models.shufflenet_v2.shufflenet_v2_x1_5,
      'shufflenet_v2_x2_0': tw.models.shufflenet_v2.shufflenet_v2_x2_0,

      'senet154': tw.models.senet.senet154,
      'se_resnet50': tw.models.senet.se_resnet50,
      'se_resnet101': tw.models.senet.se_resnet101,
      'se_resnet152': tw.models.senet.se_resnet152,
      'se_resnext50_32x4d': tw.models.senet.se_resnext50_32x4d,
      'se_resnext101_32x4d': tw.models.senet.se_resnext101_32x4d,
      
      'resnet18d': tw.models.resnet.resnet18d,
      'resnet34d': tw.models.resnet.resnet34d,
      'resnet26': tw.models.resnet.resnet26,
      'resnet26d': tw.models.resnet.resnet26d,
      'resnet50d': tw.models.resnet.resnet50d,
      'resnet101d': tw.models.resnet.resnet101d,
      'resnet152d': tw.models.resnet.resnet152d,
      'resnet200d': tw.models.resnet.resnet200d,
      
      'resnext50d_32x4d': tw.models.resnet.resnext50d_32x4d,
      'resnext101_32x4d': tw.models.resnet.resnext101_32x4d,
      'resnext101_64x4d': tw.models.resnet.resnext101_64x4d,

      'ig_resnext101_32x8d': tw.models.resnet.ig_resnext101_32x8d,
      'ig_resnext101_32x16d': tw.models.resnet.ig_resnext101_32x16d,
      'ig_resnext101_32x32d': tw.models.resnet.ig_resnext101_32x32d,
      'ig_resnext101_32x48d': tw.models.resnet.ig_resnext101_32x48d,

      'ssl_resnet18': tw.models.resnet.ssl_resnet18,
      'ssl_resnet50': tw.models.resnet.ssl_resnet50,
      'ssl_resnext50_32x4d': tw.models.resnet.ssl_resnext50_32x4d,
      'ssl_resnext101_32x4d': tw.models.resnet.ssl_resnext101_32x4d,
      'ssl_resnext101_32x8d': tw.models.resnet.ssl_resnext101_32x8d,
      'ssl_resnext101_32x16d': tw.models.resnet.ssl_resnext101_32x16d,
      
      'swsl_resnet18': tw.models.resnet.swsl_resnet18,
      'swsl_resnet50': tw.models.resnet.swsl_resnet50,
      'swsl_resnext50_32x4d': tw.models.resnet.swsl_resnext50_32x4d,
      'swsl_resnext101_32x4d': tw.models.resnet.swsl_resnext101_32x4d,
      'swsl_resnext101_32x8d': tw.models.resnet.swsl_resnext101_32x8d,
      'swsl_resnext101_32x16d': tw.models.resnet.swsl_resnext101_32x16d,
      
      'resnetrs50': tw.models.resnet.resnetrs50,
      'resnetrs101': tw.models.resnet.resnetrs101,
      'resnetrs152': tw.models.resnet.resnetrs152,
      'resnetrs200': tw.models.resnet.resnetrs200,
      'resnetrs270': tw.models.resnet.resnetrs270,
      'resnetrs350': tw.models.resnet.resnetrs350,
      'resnetrs420': tw.models.resnet.resnetrs420,
      
      'ecaresnet26t': tw.models.resnet.ecaresnet26t,
      'ecaresnet50d': tw.models.resnet.ecaresnet50d,
      'ecaresnet50t': tw.models.resnet.ecaresnet50t,
      'ecaresnetlight': tw.models.resnet.ecaresnetlight,
      'ecaresnet101d': tw.models.resnet.ecaresnet101d,
      'ecaresnet200d': tw.models.resnet.ecaresnet200d,
      'ecaresnet269d': tw.models.resnet.ecaresnet269d,
      'ecaresnext26t_32x4d': tw.models.resnet.ecaresnext26t_32x4d,
      'ecaresnext50t_32x4d': tw.models.resnet.ecaresnext50t_32x4d,
      
      'mobilenetv3_large_075': tw.models.mobilenet_v3.mobilenetv3_large_075,
      'mobilenetv3_large_100': tw.models.mobilenet_v3.mobilenetv3_large_100,
      'mobilenetv3_large_100_miil': tw.models.mobilenet_v3.mobilenetv3_large_100_miil,
      'mobilenetv3_large_100_miil_in21k': tw.models.mobilenet_v3.mobilenetv3_large_100_miil_in21k,
      'mobilenetv3_small_075': tw.models.mobilenet_v3.mobilenetv3_small_075,
      'mobilenetv3_small_100': tw.models.mobilenet_v3.mobilenetv3_small_100,
      'mobilenetv3_rw': tw.models.mobilenet_v3.mobilenetv3_rw,
      'tf_mobilenetv3_large_075': tw.models.mobilenet_v3.tf_mobilenetv3_large_075,
      'tf_mobilenetv3_large_100': tw.models.mobilenet_v3.tf_mobilenetv3_large_100,
      'tf_mobilenetv3_large_minimal_100': tw.models.mobilenet_v3.tf_mobilenetv3_large_minimal_100,
      'tf_mobilenetv3_small_075': tw.models.mobilenet_v3.tf_mobilenetv3_small_075,
      'tf_mobilenetv3_small_100': tw.models.mobilenet_v3.tf_mobilenetv3_small_100,
      'tf_mobilenetv3_small_minimal_100': tw.models.mobilenet_v3.tf_mobilenetv3_small_minimal_100,
      
      'drn-c-26': tw.models.drn.drn_c_26,
      'drn-c-42': tw.models.drn.drn_c_42,
      'drn-c-58': tw.models.drn.drn_c_58,
      'drn-d-22': tw.models.drn.drn_d_22,
      'drn-d-38': tw.models.drn.drn_d_38,
      'drn-d-54': tw.models.drn.drn_d_54,
      'drn-d-105': tw.models.drn.drn_d_105,
      
      'mnasnet_050': tw.models.efficientnet.mnasnet_050,
      'mnasnet_075': tw.models.efficientnet.mnasnet_075,
      'mnasnet_100': tw.models.efficientnet.mnasnet_100,
      'mnasnet_140': tw.models.efficientnet.mnasnet_140,
      'semnasnet_050': tw.models.efficientnet.semnasnet_050,
      'semnasnet_075': tw.models.efficientnet.semnasnet_075,
      'semnasnet_100': tw.models.efficientnet.semnasnet_100,
      'semnasnet_140': tw.models.efficientnet.semnasnet_140,
      'mnasnet_small': tw.models.efficientnet.mnasnet_small,
      'mobilenetv2_100': tw.models.efficientnet.mobilenetv2_100,
      'mobilenetv2_110d': tw.models.efficientnet.mobilenetv2_110d,
      'mobilenetv2_120d': tw.models.efficientnet.mobilenetv2_120d,
      'mobilenetv2_140': tw.models.efficientnet.mobilenetv2_140,
      'fbnetc_100': tw.models.efficientnet.fbnetc_100,
      'spnasnet_100': tw.models.efficientnet.spnasnet_100,
      'eca_efficientnet_b0': tw.models.efficientnet.eca_efficientnet_b0,
      'gc_efficientnet_b0': tw.models.efficientnet.gc_efficientnet_b0,
      'efficientnet_b0': tw.models.efficientnet.efficientnet_b0,
      'efficientnet_b1': tw.models.efficientnet.efficientnet_b1,
      'efficientnet_b2': tw.models.efficientnet.efficientnet_b2,
      'efficientnet_b3': tw.models.efficientnet.efficientnet_b3,
      'efficientnet_b4': tw.models.efficientnet.efficientnet_b4,
      'efficientnet_b5': tw.models.efficientnet.efficientnet_b5,
      'efficientnet_b6': tw.models.efficientnet.efficientnet_b6,
      'efficientnet_b7': tw.models.efficientnet.efficientnet_b7,
      'efficientnet_b8': tw.models.efficientnet.efficientnet_b8,
      'efficientnet_l2': tw.models.efficientnet.efficientnet_l2,
      'efficientnet_es': tw.models.efficientnet.efficientnet_es,
      'efficientnet_em': tw.models.efficientnet.efficientnet_em,
      'efficientnet_el': tw.models.efficientnet.efficientnet_el,
      'efficientnet_cc_b0_4e': tw.models.efficientnet.efficientnet_cc_b0_4e,
      'efficientnet_cc_b0_8e': tw.models.efficientnet.efficientnet_cc_b0_8e,
      'efficientnet_cc_b1_8e': tw.models.efficientnet.efficientnet_cc_b1_8e,
      'efficientnet_lite0': tw.models.efficientnet.efficientnet_lite0,
      'efficientnet_lite1': tw.models.efficientnet.efficientnet_lite1,
      'efficientnet_lite2': tw.models.efficientnet.efficientnet_lite2,
      'efficientnet_lite3': tw.models.efficientnet.efficientnet_lite3,
      'efficientnet_lite4': tw.models.efficientnet.efficientnet_lite4,
      'efficientnetv2_rw_t': tw.models.efficientnet.efficientnetv2_rw_t,
      'gc_efficientnetv2_rw_t': tw.models.efficientnet.gc_efficientnetv2_rw_t,
      'efficientnetv2_rw_s': tw.models.efficientnet.efficientnetv2_rw_s,
      'efficientnetv2_rw_m': tw.models.efficientnet.efficientnetv2_rw_m,
      'efficientnetv2_s': tw.models.efficientnet.efficientnetv2_s,
      'efficientnetv2_m': tw.models.efficientnet.efficientnetv2_m,
      'efficientnetv2_l': tw.models.efficientnet.efficientnetv2_l,
      'tf_efficientnet_b0': tw.models.efficientnet.tf_efficientnet_b0,
      'tf_efficientnet_b1': tw.models.efficientnet.tf_efficientnet_b1,
      'tf_efficientnet_b2': tw.models.efficientnet.tf_efficientnet_b2,
      'tf_efficientnet_b3': tw.models.efficientnet.tf_efficientnet_b3,
      'tf_efficientnet_b4': tw.models.efficientnet.tf_efficientnet_b4,
      'tf_efficientnet_b5': tw.models.efficientnet.tf_efficientnet_b5,
      'tf_efficientnet_b6': tw.models.efficientnet.tf_efficientnet_b6,
      'tf_efficientnet_b7': tw.models.efficientnet.tf_efficientnet_b7,
      'tf_efficientnet_b8': tw.models.efficientnet.tf_efficientnet_b8,
      'tf_efficientnet_b0_ap': tw.models.efficientnet.tf_efficientnet_b0_ap,
      'tf_efficientnet_b1_ap': tw.models.efficientnet.tf_efficientnet_b1_ap,
      'tf_efficientnet_b2_ap': tw.models.efficientnet.tf_efficientnet_b2_ap,
      'tf_efficientnet_b3_ap': tw.models.efficientnet.tf_efficientnet_b3_ap,
      'tf_efficientnet_b4_ap': tw.models.efficientnet.tf_efficientnet_b4_ap,
      'tf_efficientnet_b5_ap': tw.models.efficientnet.tf_efficientnet_b5_ap,
      'tf_efficientnet_b6_ap': tw.models.efficientnet.tf_efficientnet_b6_ap,
      'tf_efficientnet_b7_ap': tw.models.efficientnet.tf_efficientnet_b7_ap,
      'tf_efficientnet_b8_ap': tw.models.efficientnet.tf_efficientnet_b8_ap,
      'tf_efficientnet_b0_ns': tw.models.efficientnet.tf_efficientnet_b0_ns,
      'tf_efficientnet_b1_ns': tw.models.efficientnet.tf_efficientnet_b1_ns,
      'tf_efficientnet_b2_ns': tw.models.efficientnet.tf_efficientnet_b2_ns,
      'tf_efficientnet_b3_ns': tw.models.efficientnet.tf_efficientnet_b3_ns,
      'tf_efficientnet_b4_ns': tw.models.efficientnet.tf_efficientnet_b4_ns,
      'tf_efficientnet_b5_ns': tw.models.efficientnet.tf_efficientnet_b5_ns,
      'tf_efficientnet_b6_ns': tw.models.efficientnet.tf_efficientnet_b6_ns,
      'tf_efficientnet_b7_ns': tw.models.efficientnet.tf_efficientnet_b7_ns,
      'tf_efficientnet_l2_ns_475': tw.models.efficientnet.tf_efficientnet_l2_ns_475,
      'tf_efficientnet_l2_ns': tw.models.efficientnet.tf_efficientnet_l2_ns,
      'tf_efficientnet_es': tw.models.efficientnet.tf_efficientnet_es,
      'tf_efficientnet_em': tw.models.efficientnet.tf_efficientnet_em,
      'tf_efficientnet_el': tw.models.efficientnet.tf_efficientnet_el,
      'tf_efficientnet_cc_b0_4e': tw.models.efficientnet.tf_efficientnet_cc_b0_4e,
      'tf_efficientnet_cc_b0_8e': tw.models.efficientnet.tf_efficientnet_cc_b0_8e,
      'tf_efficientnet_cc_b1_8e': tw.models.efficientnet.tf_efficientnet_cc_b1_8e,
      'tf_efficientnet_lite0': tw.models.efficientnet.tf_efficientnet_lite0,
      'tf_efficientnet_lite1': tw.models.efficientnet.tf_efficientnet_lite1,
      'tf_efficientnet_lite2': tw.models.efficientnet.tf_efficientnet_lite2,
      'tf_efficientnet_lite3': tw.models.efficientnet.tf_efficientnet_lite3,
      'tf_efficientnet_lite4': tw.models.efficientnet.tf_efficientnet_lite4,
      'tf_efficientnetv2_s': tw.models.efficientnet.tf_efficientnetv2_s,
      'tf_efficientnetv2_m': tw.models.efficientnet.tf_efficientnetv2_m,
      'tf_efficientnetv2_l': tw.models.efficientnet.tf_efficientnetv2_l,
      'tf_efficientnetv2_s_in21ft1k': tw.models.efficientnet.tf_efficientnetv2_s_in21ft1k,
      'tf_efficientnetv2_m_in21ft1k': tw.models.efficientnet.tf_efficientnetv2_m_in21ft1k,
      'tf_efficientnetv2_l_in21ft1k': tw.models.efficientnet.tf_efficientnetv2_l_in21ft1k,
      'tf_efficientnetv2_s_in21k': tw.models.efficientnet.tf_efficientnetv2_s_in21k,
      'tf_efficientnetv2_m_in21k': tw.models.efficientnet.tf_efficientnetv2_m_in21k,
      'tf_efficientnetv2_l_in21k': tw.models.efficientnet.tf_efficientnetv2_l_in21k,
      'tf_efficientnetv2_b0': tw.models.efficientnet.tf_efficientnetv2_b0,
      'tf_efficientnetv2_b1': tw.models.efficientnet.tf_efficientnetv2_b1,
      'tf_efficientnetv2_b2': tw.models.efficientnet.tf_efficientnetv2_b2,
      'tf_efficientnetv2_b3': tw.models.efficientnet.tf_efficientnetv2_b3,
      'mixnet_s': tw.models.efficientnet.mixnet_s,
      'mixnet_m': tw.models.efficientnet.mixnet_m,
      'mixnet_l': tw.models.efficientnet.mixnet_l,
      'mixnet_xl': tw.models.efficientnet.mixnet_xl,
      'mixnet_xxl': tw.models.efficientnet.mixnet_xxl,
      'tf_mixnet_s': tw.models.efficientnet.tf_mixnet_s,
      'tf_mixnet_m': tw.models.efficientnet.tf_mixnet_m,
      'tf_mixnet_l': tw.models.efficientnet.tf_mixnet_l,
    }
    
    model = models[cfg.model_name](num_classes=cfg.num_classes, pretrained=True)
    model.to(cfg.device)

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
      tw.checkpoint.load_matched_state_dict(self.Model, ckpt['state_dict'])
      if self.Optim is not None:
        self.Optim.load_state_dict(ckpt['optimizer'])
        self.Step = ckpt['global_step']
        self.Epoch = ckpt['global_epoch']

    elif cfg.model_source == 'vanilla':
      tw.checkpoint.load_matched_state_dict(self.Model, ckpt['state_dict'])

    elif cfg.model_source == 'torchvision':
      tw.checkpoint.load_matched_state_dict(self.Model, ckpt)

    else:
      raise NotImplementedError

  def _transform_cifar_train(self, metas):
    """transform
    """
    if metas[0].source == T.COLORSPACE.GRAY:
      T.change_colorspace(metas, T.COLORSPACE.GRAY, T.COLORSPACE.RGB)
    T.pad(metas, 4, 4, 4, 4)
    T.random_crop(metas, 32, 32)
    T.random_hflip(metas, 0.5)
    T.to_tensor(metas, scale=255.0, mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    return metas

  def _transform_cifar_val(self, metas):
    """transform
    """
    if metas[0].source == T.COLORSPACE.GRAY:
      T.change_colorspace(metas, T.COLORSPACE.GRAY, T.COLORSPACE.RGB)
    T.pad(metas, 4, 4, 4, 4)
    T.center_crop(metas, 32, 32)
    T.to_tensor(metas, scale=255.0, mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    return metas

  def _transform_vgg_train(self, metas, size=[224, 224], scale=255,
                           mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]):
    """transform
    """
    T.change_colorspace(metas, T.COLORSPACE.BGR, T.COLORSPACE.RGB)
    T.center_crop(metas, size[0], size[1])
    T.random_hflip(metas, 0.5)
    T.to_tensor(metas, scale=scale, mean=mean, std=std)
    return metas

  def _transform_vgg_val(self, metas, size=[224, 224], crop_ratio=0.875,
                         scale=255, mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225], **kwargs):
    """transform
    """
    T.change_colorspace(metas, T.COLORSPACE.BGR, T.COLORSPACE.RGB)
    T.shortside_resize(metas, min_size=int(math.floor(size[0] / crop_ratio)), interpolation=cv2.INTER_CUBIC)
    T.center_crop(metas, size[0], size[1])
    T.to_tensor(metas, scale=scale, mean=mean, std=std)
    return metas

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
    # criteria
    criteria = torch.nn.CrossEntropyLoss(reduction='mean')

    # training
    while self.Epoch < cfg.train_epoch:

      self.Epoch += 1
      self.Model.train()

      for samples in train_loader:

        # -------------------------------------------------------------------------
        # prepare data
        # -------------------------------------------------------------------------
        self.Step += 1

        # convert data into tensor
        images, targets = [], []
        for sample in samples:
          images.append(sample[0].bin.to(device))
          targets.append(sample[0].label)
        images = torch.stack(images, dim=0).float().to(device)
        targets = torch.tensor(targets).long().to(device)

        # -------------------------------------------------------------------------
        # FORWARD
        # -------------------------------------------------------------------------
        features = self.Model(images)

        # losses
        losses = {'loss_cls': criteria(features, targets)}

        # update
        loss = sum(loss for loss in losses.values())
        self.Optim.zero_grad()
        loss.backward()
        self.Optim.step()

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
        self._val(loader=val_loader)

  def _val(self, **kwargs):
    """validate after epoch
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
      val_loader = self._build_dataset(tw.phase.val)

    # create folder for every epoch
    root = tw.fs.mkdirs(f'{cfg.root}/val/epoch_{self.Epoch}_step_{self.Step}/')

    # start
    with torch.no_grad():
      for images, targets in tqdm.tqdm(val_loader):
        total += images.size(0)

        # -------------------------------------------------------------------
        # prepare data
        # -------------------------------------------------------------------
        images = images.to(device)
        targets = targets.long().to(device)

        # -------------------------------------------------------------------
        # FORWARD
        # -------------------------------------------------------------------
        features = self.Model(images)

        # eval
        metrics = self.Evaluator.compute(features, targets)
        self.Evaluator.append(metrics)

    # stat
    reports = self.Evaluator.accumulate()
    elapsed = tw.timer.duration(start_time, tw.timer.tic())
    throughput = tw.timer.throughput(elapsed, total)
    keys = list(reports.keys()) + ['time', 'throughtput']
    vals = list(reports.values()) + [elapsed, throughput]
    tw.runner.log(keys=keys, values=vals, step=self.Step, epoch=self.Epoch, tag='val', writer=self.Writer)

  def _viz(self, **kwargs):
    raise NotImplementedError()

  def _onnx(self, **kwargs):
    raise NotImplementedError()

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

    else:
      raise NotImplementedError(cfg.task)


if __name__ == "__main__":
  parser = argparse.ArgumentParser()

  # ---------------------------------------------
  #  USED BY CONTEXT
  # ---------------------------------------------
  parser.add_argument('--task', type=str, default=None, choices=['train', 'val', 'viz'])

  # ---------------------------------------------
  #  USED BY QUANTIZATION TRAINING
  # ---------------------------------------------

  # ---------------------------------------------
  #  USED BY HALF TRAINING
  # ---------------------------------------------

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
  parser.add_argument('--model-name', type=str, required=True)
  parser.add_argument('--model-path', type=str, default=None, help="loadding pretrain/last-checkpoint model.")
  parser.add_argument('--model-source', type=str, default=None)

  # ---------------------------------------------
  #  USED BY TRAIN-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--train-lr', type=float, default=0.01, help="total learning rate across devices.")
  parser.add_argument('--train-batchsize', type=int, default=32, help="total batch size across devices.")
  parser.add_argument('--train-epoch', type=int, default=240, help="total training epochs.")
  parser.add_argument('--train-optimizer', type=str, default='sgd', choices=['sgd', 'adam'], help="training optimizer.")

  # ---------------------------------------------
  #  USED BY VAL-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--val-batchsize', type=int, default=32, help="total batch size across devices.")

  # ---------------------------------------------
  #  USED BY DATASETS
  # ---------------------------------------------
  parser.add_argument('--dataset', type=str, default=None, choices=['Mnist', 'Cifar10', 'ImageNet'])
  parser.add_argument('--num_classes', type=int, default=10, help="number of classes.")

  tw.runner.launch(parser, Classifier2d)
