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

import functools
import torch
import torch.nn as nn
from torch.nn import functional as F


class NLayerDiscriminator(nn.Module):
  """Defines a PatchGAN discriminator"""

  def __init__(self, in_nc, nf=64, n_layers=3, norm_layer=nn.BatchNorm2d):
    r"""Construct a PatchGAN discriminator

    Parameters:
        in_nc (int)  -- the number of channels in input images
        nf (int)       -- the number of filters in the last conv layer
        n_layers (int)  -- the number of conv layers in the discriminator
        norm_layer      -- normalization layer
    """

    super(NLayerDiscriminator, self).__init__()
    use_bias = False
    kw = 4
    padw = 1
    sequence = [nn.Conv2d(in_nc, nf, kernel_size=kw, stride=2, padding=padw), nn.LeakyReLU(0.2, True)]
    nf_mult = 1
    nf_mult_prev = 1
    for n in range(1, n_layers):  # gradually increase the number of filters
      nf_mult_prev = nf_mult
      nf_mult = min(2 ** n, 8)
      sequence += [
          nn.Conv2d(nf * nf_mult_prev, nf * nf_mult, kernel_size=kw, stride=2, padding=padw, bias=use_bias),
          norm_layer(nf * nf_mult),
          nn.LeakyReLU(0.2, True)
      ]

    nf_mult_prev = nf_mult
    nf_mult = min(2 ** n_layers, 8)
    sequence += [
        nn.Conv2d(nf * nf_mult_prev, nf * nf_mult, kernel_size=kw, stride=1, padding=padw, bias=use_bias),
        norm_layer(nf * nf_mult),
        nn.LeakyReLU(0.2, True)
    ]

    sequence += [nn.Conv2d(nf * nf_mult, 1, kernel_size=kw, stride=1, padding=padw)]  # output 1 channel prediction map
    # TODO
    self.model = nn.Sequential(*sequence)

  def forward(self, x):
    """Standard forward."""
    return self.model(x)
