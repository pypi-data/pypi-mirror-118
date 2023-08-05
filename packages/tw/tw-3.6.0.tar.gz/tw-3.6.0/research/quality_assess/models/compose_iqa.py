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
"""compose iqa
    [N, C, H, W] -> Network ->
        -> c2
        -> c3
        -> c4
        -> c5
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import tw
from torch.hub import load_state_dict_from_url


class ComposeBlindIQA(nn.Module):

  def __init__(self, backbone):
    super(ComposeBlindIQA, self).__init__()

    if backbone == 'mobilenet_v2':
      self.backbone = tw.models.mobilenet_v2.mobilenet_v2(num_classes=1, output_backbone=True)
      ckpt = load_state_dict_from_url('https://download.pytorch.org/models/mobilenet_v2-b0353104.pth')
      tw.checkpoint.load_matched_state_dict(self.backbone, ckpt)
      self.head = nn.Sequential(nn.Dropout(0.2), nn.Linear(1432, 1))

    elif backbone == 'vgg16':
      self.backbone = tw.models.vgg.vgg16(num_classes=1, output_backbone=True)
      ckpt = load_state_dict_from_url('https://download.pytorch.org/models/vgg16-397923af.pth')
      tw.checkpoint.load_matched_state_dict(self.backbone, ckpt)

    elif backbone == 'resnet50':
      self.backbone = tw.models.resnet.resnet50(num_classes=1, output_backbone=True)
      ckpt = load_state_dict_from_url('https://download.pytorch.org/models/resnet50-19c8e357.pth')
      tw.checkpoint.load_matched_state_dict(self.backbone, ckpt)
      self.head = nn.Sequential(nn.Linear(3840, 1))

    elif backbone == 'resnet18':
      self.backbone = tw.models.resnet.resnet18(num_classes=1)
      ckpt = load_state_dict_from_url('https://download.pytorch.org/models/resnet18-5c106cde.pth')
      tw.checkpoint.load_matched_state_dict(self.backbone, ckpt, output_backbone=True)
      self.head = nn.Sequential(nn.Linear(3840, 1))

    elif backbone == 'swsl_resnet18':
      self.backbone = tw.models.resnet.swsl_resnet18(pretrained=True, output_backbone=True)
      self.head = nn.Sequential(nn.Linear(960, 1))
      self.map_c2 = nn.Identity()# nn.Sequential(nn.Conv2d(64, 128, 1, 1, 0), nn.BatchNorm2d(128), nn.LeakyReLU(0.2))
      self.map_c3 = nn.Identity()# nn.Sequential(nn.Conv2d(128, 128, 1, 1, 0), nn.BatchNorm2d(128), nn.LeakyReLU(0.2))
      self.map_c4 = nn.Identity()# nn.Sequential(nn.Conv2d(256, 128, 1, 1, 0), nn.BatchNorm2d(128), nn.LeakyReLU(0.2))
      self.map_c5 = nn.Identity()# nn.Sequential(nn.Conv2d(512, 128, 1, 1, 0), nn.BatchNorm2d(128), nn.LeakyReLU(0.2))

    else:
      raise NotImplementedError(backbone)

    # for p in self.modules():
    #   if isinstance(p, nn.BatchNorm2d):
    #     p.weight.requires_grad = False
    #     p.bias.requires_grad = False

  def forward(self, inputs):
    c2, c3, c4, c5 = self.backbone(inputs)
    p2 = F.adaptive_avg_pool2d(c2, 1)
    p3 = F.adaptive_avg_pool2d(c3, 1)
    p4 = F.adaptive_avg_pool2d(c4, 1)
    p5 = F.adaptive_avg_pool2d(c5, 1)
    # print(p2.shape, p3.shape, p4.shape, p5.shape)
    merge = torch.cat([p2, p3, p4, p5], dim=1).mean([2, 3])
    # print(merge.shape)
    output = self.head(merge)
    return output


class ComposeFullRefIQA(nn.Module):

  def __init__(self, backbone):
    super(ComposeFullRefIQA, self).__init__()

    if backbone == 'mobilenet_v2':
      self.backbone = tw.models.mobilenet_v2.mobilenet_v2(num_classes=1, output_backbone=True)
      ckpt = load_state_dict_from_url('https://download.pytorch.org/models/mobilenet_v2-b0353104.pth')
      tw.checkpoint.load_matched_state_dict(self.backbone, ckpt)

    elif backbone == 'vgg16':
      self.backbone = tw.models.vgg.vgg16(num_classes=1, output_backbone=True)
      ckpt = load_state_dict_from_url('https://download.pytorch.org/models/vgg16-397923af.pth')
      tw.checkpoint.load_matched_state_dict(self.backbone, ckpt)

    elif backbone == 'resnet50':
      self.backbone = tw.models.resnet.resnet50(num_classes=1, output_backbone=True)
      ckpt = load_state_dict_from_url('https://download.pytorch.org/models/resnet50-19c8e357.pth')
      tw.checkpoint.load_matched_state_dict(self.backbone, ckpt)

    elif backbone == 'resnet18':
      self.backbone = tw.models.resnet.resnet18(num_classes=1)
      ckpt = load_state_dict_from_url('https://download.pytorch.org/models/resnet18-5c106cde.pth')
      tw.checkpoint.load_matched_state_dict(self.backbone, ckpt, output_backbone=True)

    else:
      raise NotImplementedError(backbone)

  def forward(self, inputs):
    c2, c3, c4, c5 = self.backbone(inputs)
    print(c2.shape, c3.shape, c4.shape, c5.shape)
