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
"""baseline iqa
    [N, C, H, W] -> Network -> score
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import tw


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

class KonCept512(nn.Module):

  def __init__(self, backbone):
    super(KonCept512, self).__init__()

    if backbone == 'mobilenet_v2':
      self.backbone = tw.models.mobilenet_v2.mobilenet_v2(num_classes=1, output_backbone=True)
      tw.checkpoint.load_state_dict_from_url(
          self.backbone, 'https://download.pytorch.org/models/mobilenet_v2-b0353104.pth')
      num_features = 1280
      del self.backbone.classifier

    elif backbone == 'vgg16':
      self.backbone = tw.models.vgg.vgg16(num_classes=1, output_backbone=True)
      tw.checkpoint.load_state_dict_from_url(
          self.backbone, 'https://download.pytorch.org/models/vgg16-397923af.pth')

    elif backbone == 'resnet50':
      self.backbone = tw.models.resnet.resnet50(num_classes=1, output_backbone=True)
      tw.checkpoint.load_state_dict_from_url(
          self.backbone, 'https://download.pytorch.org/models/resnet50-19c8e357.pth')

    elif backbone == 'resnet18':
      self.backbone = tw.models.resnet.resnet18(num_classes=1, output_backbone=True)
      tw.checkpoint.load_state_dict_from_url(
          self.backbone, 'https://download.pytorch.org/models/resnet18-5c106cde.pth')
      num_features = 512

    elif backbone == 'mobilenetv3_large_100_miil':
      self.backbone = tw.models.mobilenet_v3.mobilenetv3_large_100_miil(
          num_classes=1, pretrained=True, output_backbone=True)
      num_features = 1280

    elif backbone == 'tf_mobilenetv3_small_100':
      self.backbone = tw.models.mobilenet_v3.tf_mobilenetv3_small_100(num_classes=1, pretrained=True, output_backbone=True)
      num_features = 1024

    elif backbone == 'resnet101d':
      self.backbone = tw.models.resnet.resnet101d(num_classes=1, pretrained=True, output_backbone=True)
      num_features = 2048
      
    elif backbone == 'ssl_resnext101_32x8d':
      self.backbone = tw.models.resnet.ssl_resnext101_32x8d(num_classes=1, pretrained=True, output_backbone=True)
      num_features = 2048
    
    elif backbone == 'efficientnet_b4':
      self.backbone = tw.models.efficientnet.efficientnet_b4(num_classes=1, pretrained=True, output_backbone=True)
      num_features = 1792
      
    elif backbone == 'inception_resnet_v2':
      self.backbone = tw.models.inceptionresnetv2.inceptionresnetv2(num_classes=1000, pretrained='imagenet', output_backbone=True)
      num_features = 1536
      del self.backbone.last_linear
      
    else:
      raise NotImplementedError(backbone)

    self.head, out_channels = _metal_iqa_head(num_features)
    self.cls_head = nn.Linear(out_channels, 1)

  def forward(self, inputs):
    c2, c3, c4, c5 = self.backbone(inputs)
    head = self.head(c5)
    mos = self.cls_head(head)
    # dist = self.dist_head(head)
    return mos
