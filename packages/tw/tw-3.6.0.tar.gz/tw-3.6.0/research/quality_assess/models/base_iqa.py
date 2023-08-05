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
from torch.hub import load_state_dict_from_url


class CNNIQAnet(nn.Module):

  def __init__(self, ker_size=7, n_kers=50, n1_nodes=800, n2_nodes=800):
    super(CNNIQAnet, self).__init__()
    self.conv1 = nn.Conv2d(1, n_kers, ker_size)
    self.fc1 = nn.Linear(2 * n_kers, n1_nodes)
    self.fc2 = nn.Linear(n1_nodes, n2_nodes)
    self.fc3 = nn.Linear(n2_nodes, 1)
    self.dropout = nn.Dropout()

  def forward(self, x):
    x = x.view(-1, x.size(-3), x.size(-2), x.size(-1))  #

    h = self.conv1(x)

    # h1 = F.adaptive_max_pool2d(h, 1)
    # h2 = -F.adaptive_max_pool2d(-h, 1)
    h1 = F.max_pool2d(h, (h.size(-2), h.size(-1)))
    h2 = -F.max_pool2d(-h, (h.size(-2), h.size(-1)))
    h = torch.cat((h1, h2), 1)  # max-min pooling
    h = h.squeeze(3).squeeze(2)

    h = F.relu(self.fc1(h))
    h = self.dropout(h)
    h = F.relu(self.fc2(h))

    q = self.fc3(h)
    return q


class BaseIQA(nn.Module):

  def __init__(self, backbone):
    super(BaseIQA, self).__init__()

    if backbone == 'mobilenet_v2':
      self.backbone = tw.models.mobilenet_v2.mobilenet_v2(num_classes=1)
      ckpt = load_state_dict_from_url('https://download.pytorch.org/models/mobilenet_v2-b0353104.pth')
      tw.checkpoint.load_matched_state_dict(self.backbone, ckpt)

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

  def forward(self, inputs):
    return self.backbone(inputs)
