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

from torch import nn as nn


class VGGStyleDiscriminator(nn.Module):
  """VGG style discriminator with input size 128 x 128.

  It is used to train SRGAN and ESRGAN.

  Args:
      num_in_ch (int): Channel number of inputs. Default: 3.
      num_feat (int): Channel number of base intermediate features.
          Default: 64.
  """

  def __init__(self, num_in_ch, num_feat, input_size=128):
    super(VGGStyleDiscriminator, self).__init__()
    self.input_size = input_size

    self.conv0_0 = nn.Conv2d(num_in_ch, num_feat, 3, 1, 1, bias=True)
    self.conv0_1 = nn.Conv2d(num_feat, num_feat, 4, 2, 1, bias=False)
    self.bn0_1 = nn.BatchNorm2d(num_feat, affine=True)

    self.conv1_0 = nn.Conv2d(num_feat, num_feat * 2, 3, 1, 1, bias=False)
    self.bn1_0 = nn.BatchNorm2d(num_feat * 2, affine=True)
    self.conv1_1 = nn.Conv2d(num_feat * 2, num_feat * 2, 4, 2, 1, bias=False)
    self.bn1_1 = nn.BatchNorm2d(num_feat * 2, affine=True)

    self.conv2_0 = nn.Conv2d(num_feat * 2, num_feat * 4, 3, 1, 1, bias=False)
    self.bn2_0 = nn.BatchNorm2d(num_feat * 4, affine=True)
    self.conv2_1 = nn.Conv2d(num_feat * 4, num_feat * 4, 4, 2, 1, bias=False)
    self.bn2_1 = nn.BatchNorm2d(num_feat * 4, affine=True)

    self.conv3_0 = nn.Conv2d(num_feat * 4, num_feat * 8, 3, 1, 1, bias=False)
    self.bn3_0 = nn.BatchNorm2d(num_feat * 8, affine=True)
    self.conv3_1 = nn.Conv2d(num_feat * 8, num_feat * 8, 4, 2, 1, bias=False)
    self.bn3_1 = nn.BatchNorm2d(num_feat * 8, affine=True)

    self.conv4_0 = nn.Conv2d(num_feat * 8, num_feat * 8, 3, 1, 1, bias=False)
    self.bn4_0 = nn.BatchNorm2d(num_feat * 8, affine=True)
    self.conv4_1 = nn.Conv2d(num_feat * 8, num_feat * 8, 4, 2, 1, bias=False)
    self.bn4_1 = nn.BatchNorm2d(num_feat * 8, affine=True)

    if input_size // 128 >= 2:
      self.conv5_0 = nn.Conv2d(num_feat * 8, num_feat * 8, 3, 1, 1, bias=False)
      self.bn5_0 = nn.BatchNorm2d(num_feat * 8, affine=True)
      self.conv5_1 = nn.Conv2d(num_feat * 8, num_feat * 8, 4, 2, 1, bias=False)
      self.bn5_1 = nn.BatchNorm2d(num_feat * 8, affine=True)

    self.linear1 = nn.Linear(num_feat * 8 * 4 * 4, 100)
    self.linear2 = nn.Linear(100, 1)

    # activation function
    self.lrelu = nn.LeakyReLU(negative_slope=0.2, inplace=True)

  def forward(self, x):
    assert x.size(2) in [128, 256] and x.size(3) in [128, 256], (
        f'Input spatial size must be 128x128 or 256x256, '
        f'but received {x.size()}.')

    feat = self.lrelu(self.conv0_0(x))
    feat = self.lrelu(self.bn0_1(self.conv0_1(feat)))  # output spatial size: (64, 64)

    feat = self.lrelu(self.bn1_0(self.conv1_0(feat)))
    feat = self.lrelu(self.bn1_1(self.conv1_1(feat)))  # output spatial size: (32, 32)

    feat = self.lrelu(self.bn2_0(self.conv2_0(feat)))
    feat = self.lrelu(self.bn2_1(self.conv2_1(feat)))  # output spatial size: (16, 16)

    feat = self.lrelu(self.bn3_0(self.conv3_0(feat)))
    feat = self.lrelu(self.bn3_1(self.conv3_1(feat)))  # output spatial size: (8, 8)

    feat = self.lrelu(self.bn4_0(self.conv4_0(feat)))
    feat = self.lrelu(self.bn4_1(self.conv4_1(feat)))  # output spatial size: (4, 4)

    if self.input_size == 256:
      feat = self.lrelu(self.bn5_0(self.conv5_0(feat)))
      feat = self.lrelu(self.bn5_1(self.conv5_1(feat)))  # output spatial size: (4, 4)

    feat = feat.view(feat.size(0), -1)
    feat = self.lrelu(self.linear1(feat))
    out = self.linear2(feat)
    return out
