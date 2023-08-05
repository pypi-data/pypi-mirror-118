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
"""PatchIQA: PaQ-2-PiQ
"""
from tw.transform.primitive import bbox
import torch
import torch.nn as nn
import torch.nn.functional as F
import tw
from torch.hub import load_state_dict_from_url


def _koncept_head(in_channels):
  head = nn.Sequential(
      nn.AdaptiveAvgPool2d(1),
      nn.Flatten(1),
      nn.Linear(in_channels, 2048),
      nn.ReLU(inplace=True),
      nn.BatchNorm1d(2048),
      nn.Dropout(p=0.25),
      nn.Linear(2048, 1024),
      nn.ReLU(inplace=True),
      nn.BatchNorm1d(1024),
      nn.Dropout(p=0.25),
      nn.Linear(1024, 256),
      nn.ReLU(inplace=True),
      nn.BatchNorm1d(256),
      nn.Dropout(p=0.5))
  return head, 256


def _metal_iqa_head(in_channels):
  head = nn.Sequential(
      nn.AdaptiveAvgPool2d(1),
      nn.Flatten(1),
      nn.Linear(in_channels, 1024),
      nn.BatchNorm1d(1024),
      nn.PReLU(),
      nn.Dropout(0.5),
      nn.Linear(1024, 512),
      nn.BatchNorm1d(512),
      nn.PReLU(),
      nn.Dropout(0.5))
  return head, 512


def _paq2piq_head(in_channels):
  head = nn.Sequential(
      nn.AdaptiveAvgPool2d(1),
      nn.Flatten(1),
      nn.BatchNorm1d(in_channels),
      nn.Dropout(0.25),
      nn.Linear(in_channels, 512, bias=True),
      nn.ReLU(),
      nn.BatchNorm1d(512),
      nn.Dropout(0.5))
  return head, 512


def _empty_head(in_channels):
  head = nn.Sequential(
      nn.AdaptiveAvgPool2d(1),
      nn.Flatten(1),
      nn.Dropout(0.5))
  return head, in_channels


class PatchIQA(nn.Module):

  def __init__(self, backbone, mode='base'):
    super(PatchIQA, self).__init__()

    if backbone == 'mobilenet_v2':
      self.backbone = tw.models.mobilenet_v2.mobilenet_v2(num_classes=1, output_backbone=True)
      ckpt = load_state_dict_from_url('https://download.pytorch.org/models/mobilenet_v2-b0353104.pth')
      tw.checkpoint.load_matched_state_dict(self.backbone, ckpt)
      num_features = 1280

    elif backbone == 'vgg16':
      self.backbone = tw.models.vgg.vgg16(num_classes=1)
      ckpt = load_state_dict_from_url('https://download.pytorch.org/models/vgg16-397923af.pth')
      tw.checkpoint.load_matched_state_dict(self.backbone, ckpt)

    elif backbone == 'resnet50':
      self.backbone = tw.models.resnet.resnet50(num_classes=1)
      ckpt = load_state_dict_from_url('https://download.pytorch.org/models/resnet50-19c8e357.pth')
      tw.checkpoint.load_matched_state_dict(self.backbone, ckpt)

    elif backbone == 'cnn':
      self.backbone = CNNIQAnet()

    elif backbone == 'shufflenet_1_0':
      self.backbone = tw.models.shufflenet_v2.shufflenet_v2_x1_0(num_classes=1)
      ckpt = load_state_dict_from_url('https://download.pytorch.org/models/shufflenetv2_x1-5666bf0f80.pth')
      tw.checkpoint.load_matched_state_dict(self.backbone, ckpt)

    elif backbone == 'resnet18':
      self.backbone = tw.models.resnet.resnet18(num_classes=1)
      ckpt = load_state_dict_from_url('https://download.pytorch.org/models/resnet18-5c106cde.pth')
      tw.checkpoint.load_matched_state_dict(self.backbone, ckpt)

    elif backbone == 'mobilenetv3_large_100_miil':
      self.backbone = tw.models.mobilenet_v3.mobilenetv3_large_100_miil(num_classes=1, pretrained=True)

    elif backbone == 'tf_mobilenetv3_small_100':
      self.backbone = tw.models.mobilenet_v3.tf_mobilenetv3_small_100(num_classes=1, pretrained=True)

    elif backbone == 'resnet101d':
      self.backbone = tw.models.resnet.resnet101d(num_classes=1, pretrained=True)

    else:
      raise NotImplementedError(backbone)

    # select mode
    self.mode = mode

    # image mapping
    self.head, base_channels = _paq2piq_head(num_features)
    
    # roi head
    if mode == 'base':
      pass
    elif mode == 'roi':
      self.roi_pool = tw.nn.RoIPool([2, 2], 1 / 32.0)
      self.roi_head, out_channels = _paq2piq_head(num_features * 3)
      self.roi_reg_head = nn.Linear(out_channels, 3)
    elif mode == 'feedback':
      self.roi_pool = tw.nn.RoIPool([2, 2], 1 / 32.0)
      self.roi_head, out_channels = _paq2piq_head(num_features * 3)
      self.roi_reg_head = nn.Linear(out_channels, 3)
      base_channels += 3
    else:
      raise NotImplementedError(mode)

    # main branch
    self.reg_head = nn.Linear(base_channels, 1)

  def forward(self, inputs, bboxes=None):
    """PatchIQA

    Args:
        inputs ([torch.Tensor]): [N, C, H, W]
        boxes ([torch.Tensor]): [N, K, 4]

    Returns:
        [torch.Tensor]: [description]
    """
    c2, c3, c4, c5 = self.backbone(inputs)
    bs = inputs.size(0)

    if self.mode == 'base':
      head = self.head(c5)
      mos = self.reg_head(head)
      return mos

    elif self.mode == 'roi':
      head = self.head(c5)
      mos = self.reg_head(head)
      if not self.training:
        return mos
      bs = bboxes.size(0)
      inds = torch.arange(bs).reshape(bs, 1).repeat(1, 3).reshape(-1, 1).to(inputs.device)
      bboxes = torch.cat([inds, bboxes.reshape(-1, 4)], dim=1)
      rois = self.roi_pool(c5, bboxes).reshape(bs, 3, -1, 2, 2).mean(dim=[-1, -2])  # [bs, k, 3]
      rois_mos = self.roi_reg_head(self.roi_head(rois.reshape(bs, -1, 1, 1)))
      return mos, rois_mos

    elif self.mode == 'feedback':
      # build 3 virtual coord
      if bboxes is None:
        bboxes = torch.tensor([[192, 92, 448, 348], [224, 224, 416, 416], [256, 356, 384, 484]])
        bboxes = bboxes[None].repeat(bs, 1, 1).to(inputs.device).float()
      
      # registration
      inds = torch.arange(bs).reshape(bs, 1).repeat(1, 3).reshape(-1, 1).to(inputs.device)
      bboxes = torch.cat([inds, bboxes.reshape(-1, 4)], dim=1)
      
      # roi pooling
      rois = self.roi_pool(c5, bboxes).reshape(bs, 3, -1, 2, 2).mean(dim=[-1, -2])  # [bs, k, 3]
      rois_mos = self.roi_reg_head(self.roi_head(rois.reshape(bs, -1, 1, 1))).reshape(bs, -1)
      
      # image pooling
      head = self.head(c5)
      
      # concat
      merge = torch.cat([rois_mos, head], dim=1)
      
      # roi_mos + image feature
      mos = self.reg_head(merge)
      
      if not self.training:
        return mos
      return mos, rois_mos

    else:
      raise NotImplementedError()
