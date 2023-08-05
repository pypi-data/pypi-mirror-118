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
r"""RealSR models: Referenced in:
  https://github.com/jixiaozhong/RealSR
"""

import functools
import torch
import torch.nn as nn
from torch.nn import functional as F

batchnorm = nn.BatchNorm2d


class ResidualBlock_noBN(nn.Module):
  '''Residual block w/o BN
  ---Conv-ReLU-Conv-+-
   |________________|
  '''

  def __init__(self, nf=64):
    super(ResidualBlock_noBN, self).__init__()
    self.conv1 = nn.Conv2d(nf, nf, 3, 1, 1, bias=True)
    self.conv2 = nn.Conv2d(nf, nf, 3, 1, 1, bias=True)

    # initialization
    for m in [self.conv1, self.conv2]:
      if isinstance(m, nn.Conv2d):
        nn.init.kaiming_normal_(m.weight, a=0, mode='fan_in')
        m.weight.data *= 0.1
        if m.bias is not None:
          m.bias.data.zero_()

  def forward(self, x):
    identity = x
    out = F.relu(self.conv1(x), inplace=True)
    out = self.conv2(out)
    return identity + out


class MSRResNet(nn.Module):
  ''' modified SRResNet'''

  def __init__(self, in_nc=3, out_nc=3, nf=64, nb=16, upscale=4):
    super(MSRResNet, self).__init__()
    self.upscale = upscale

    self.conv_first = nn.Conv2d(in_nc, nf, 3, 1, 1, bias=True)
    basic_block = functools.partial(ResidualBlock_noBN, nf=nf)

    layers = []
    for _ in range(nb):
      layers.append(ResidualBlock_noBN(nf=nf))
    self.recon_trunk = nn.Sequential(*layers)

    # upsampling
    if self.upscale == 2:
      self.upconv1 = nn.Conv2d(nf, nf * 4, 3, 1, 1, bias=True)
      self.pixel_shuffle = nn.PixelShuffle(2)
    elif self.upscale == 3:
      self.upconv1 = nn.Conv2d(nf, nf * 9, 3, 1, 1, bias=True)
      self.pixel_shuffle = nn.PixelShuffle(3)
    elif self.upscale == 4:
      self.upconv1 = nn.Conv2d(nf, nf * 4, 3, 1, 1, bias=True)
      self.upconv2 = nn.Conv2d(nf, nf * 4, 3, 1, 1, bias=True)
      self.pixel_shuffle = nn.PixelShuffle(2)

    self.HRconv = nn.Conv2d(nf, nf, 3, 1, 1, bias=True)
    self.conv_last = nn.Conv2d(nf, out_nc, 3, 1, 1, bias=True)

    # activation function
    self.lrelu = nn.LeakyReLU(negative_slope=0.1, inplace=True)

    # initialization
    for m in [self.conv_first, self.upconv1, self.HRconv, self.conv_last]:
      if isinstance(m, nn.Conv2d):
        nn.init.kaiming_normal_(m.weight, a=0, mode='fan_in')
        m.weight.data *= 0.1
        if m.bias is not None:
          m.bias.data.zero_()

    if self.upscale == 4:
      for m in [self.upconv2]:
        if isinstance(m, nn.Conv2d):
          nn.init.kaiming_normal_(m.weight, a=0, mode='fan_in')
          m.weight.data *= 0.1
          if m.bias is not None:
            m.bias.data.zero_()

  def forward(self, x):
    fea = self.lrelu(self.conv_first(x))
    out = self.recon_trunk(fea)

    if self.upscale == 4:
      out = self.lrelu(self.pixel_shuffle(self.upconv1(out)))
      out = self.lrelu(self.pixel_shuffle(self.upconv2(out)))
    elif self.upscale == 3 or self.upscale == 2:
      out = self.lrelu(self.pixel_shuffle(self.upconv1(out)))

    out = self.conv_last(self.lrelu(self.HRconv(out)))
    base = F.interpolate(x, scale_factor=self.upscale, mode='bilinear', align_corners=False)
    out += base
    return out


if __name__ == "__main__":

  import tw

  model = MSRResNet(3, 3, 64, 23)
  model.eval()

  inputs = torch.rand(1, 3, 360, 640)

  tw.flops.register(model)
  with torch.no_grad():
    model(inputs)

  print(tw.flops.accumulate(model))
  tw.flops.unregister(model)
