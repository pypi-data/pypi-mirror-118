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


class ResidualDenseBlock_5C(nn.Module):
  def __init__(self, nf=64, gc=32, bias=True):
    super(ResidualDenseBlock_5C, self).__init__()
    # gc: growth channel, i.e. intermediate channels
    self.conv1 = nn.Conv2d(nf, gc, 3, 1, 1, bias=bias)
    self.conv2 = nn.Conv2d(nf + gc, gc, 3, 1, 1, bias=bias)
    self.conv3 = nn.Conv2d(nf + 2 * gc, gc, 3, 1, 1, bias=bias)
    self.conv4 = nn.Conv2d(nf + 3 * gc, gc, 3, 1, 1, bias=bias)
    self.conv5 = nn.Conv2d(nf + 4 * gc, nf, 3, 1, 1, bias=bias)
    self.lrelu = nn.LeakyReLU(negative_slope=0.2, inplace=True)

    # initialization
    for m in [self.conv1, self.conv2, self.conv3, self.conv4, self.conv5]:
      if isinstance(m, nn.Conv2d):
        nn.init.kaiming_normal_(m.weight, a=0, mode='fan_in')
        m.weight.data *= 0.1
        if m.bias is not None:
          m.bias.data.zero_()
      elif isinstance(m, nn.Linear):
        nn.init.kaiming_normal_(m.weight, a=0, mode='fan_in')
        m.weight.data *= 0.1
        if m.bias is not None:
          m.bias.data.zero_()
      elif isinstance(m, nn.BatchNorm2d):
        nn.init.constant_(m.weight, 1)
        nn.init.constant_(m.bias.data, 0.0)

  def forward(self, x):
    x1 = self.lrelu(self.conv1(x))
    x2 = self.lrelu(self.conv2(torch.cat((x, x1), 1)))
    x3 = self.lrelu(self.conv3(torch.cat((x, x1, x2), 1)))
    x4 = self.lrelu(self.conv4(torch.cat((x, x1, x2, x3), 1)))
    x5 = self.conv5(torch.cat((x, x1, x2, x3, x4), 1))
    return x5 * 0.2 + x


class RRDB(nn.Module):
  '''Residual in Residual Dense Block'''

  def __init__(self, nf, gc=32):
    super(RRDB, self).__init__()
    self.RDB1 = ResidualDenseBlock_5C(nf, gc)
    self.RDB2 = ResidualDenseBlock_5C(nf, gc)
    self.RDB3 = ResidualDenseBlock_5C(nf, gc)

  def forward(self, x):
    out = self.RDB1(x)
    out = self.RDB2(out)
    out = self.RDB3(out)
    return out * 0.2 + x


class RRDBNet(nn.Module):

  def __init__(self, in_nc, out_nc, nf, nb, gc=32):
    super(RRDBNet, self).__init__()
    RRDB_block_f = functools.partial(RRDB, nf=nf, gc=gc)

    self.conv_first = nn.Conv2d(in_nc, nf, 3, 1, 1, bias=True)

    layers = []
    for _ in range(nb):
      layers.append(RRDB_block_f())
    self.RRDB_trunk = nn.Sequential(*layers)

    self.trunk_conv = nn.Conv2d(nf, nf, 3, 1, 1, bias=True)
    # upsampling
    self.upconv1 = nn.Conv2d(nf, nf, 3, 1, 1, bias=True)
    self.upconv2 = nn.Conv2d(nf, nf, 3, 1, 1, bias=True)
    self.HRconv = nn.Conv2d(nf, nf, 3, 1, 1, bias=True)
    self.conv_last = nn.Conv2d(nf, out_nc, 3, 1, 1, bias=True)

    self.lrelu = nn.LeakyReLU(negative_slope=0.2, inplace=True)

  def forward(self, x):
    fea = self.conv_first(x)
    trunk = self.trunk_conv(self.RRDB_trunk(fea))
    fea = fea + trunk

    fea = self.lrelu(self.upconv1(F.interpolate(fea, scale_factor=2, mode='nearest')))
    # fea = self.lrelu(self.upconv2(F.interpolate(fea, scale_factor=2, mode='nearest')))
    out = self.conv_last(self.lrelu(self.HRconv(fea)))

    return out


if __name__ == "__main__":

  import tw

  model = RRDBNet(3, 3, 64, 23)
  model.eval()

  inputs = torch.rand(1, 3, 360, 640)
  
  tw.flops.register(model)
  with torch.no_grad():
    model(inputs)

  print(tw.flops.accumulate(model))
  tw.flops.unregister(model)
    