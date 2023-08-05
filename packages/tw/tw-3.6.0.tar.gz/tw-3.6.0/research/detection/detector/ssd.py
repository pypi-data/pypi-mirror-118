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
import torch
from torch import nn
from torch.nn import functional as F
import tw

#!<---------------------------------------------------------------------------
#!< MobileNet-v1
#!<---------------------------------------------------------------------------


class _conv_bn(nn.Module):

  def __init__(self, inp, oup, kernel_size, stride, padding):
    super(_conv_bn, self).__init__()
    self.conv = nn.Sequential(
        nn.Conv2d(inp, oup, kernel_size, stride, padding, bias=False),
        nn.BatchNorm2d(oup),
        nn.ReLU6(inplace=True),
    )
    self.depth = oup

  def forward(self, x):
    return self.conv(x)


class _depth_sepconv(nn.Module):

  def __init__(self, inp, oup, stride):
    super(_depth_sepconv, self).__init__()

    self.conv = nn.Sequential(
        # dw
        nn.Conv2d(inp, inp, 3, stride, 1, groups=inp, bias=False),
        nn.BatchNorm2d(inp),
        nn.ReLU6(inplace=True),
        # pw
        nn.Conv2d(inp, oup, 1, 1, 0, bias=False),
        nn.BatchNorm2d(oup),
        nn.ReLU6(inplace=True),
    )
    self.depth = oup

  def forward(self, x):
    return self.conv(x)


class MobilenetV1(nn.Module):

  def __init__(self, depth_multiplier=1.0, min_depth=8, **kwargs):
    super(MobilenetV1, self).__init__()

    self.depth_multiplier = depth_multiplier
    self.min_depth = min_depth

    # define backbone network
    self.depth = lambda d: max(int(d * self.depth_multiplier), self.min_depth)
    self.features = nn.Sequential(*self.builder_backbone())

  def builder_backbone(self):

    # Conv
    layers = [_conv_bn(3, 32, 3, 2, 1)]
    in_channels = 32

    # Residual
    residual_depths = [64, 128, 128, 256, 256,
                       512, 512, 512, 512, 512, 512, 1024, 1024]
    residual_strides = [1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 2, 1]
    for index in range(len(residual_depths)):
      layers += [_depth_sepconv(in_channels, self.depth(
          residual_depths[index]), residual_strides[index])]
      in_channels = self.depth(residual_depths[index])

    return layers

  def reset_parameters(self):

    for m in self.extras.modules():
      if isinstance(m, nn.Conv2d):
        tw.nn.initialize.kaiming(m)

  def forward(self, x):

    outs = []

    for k in range(len(self.features)):
      if k in [11, 13]:
        x = self.features[k](x)
        outs.append(x)
      else:
        x = self.features[k](x)

    # for k, v in enumerate(self.extras):
    #   x = v(x)
    #   outs.append(x)

    return outs[0] if len(outs) == 1 else tuple(outs)

#!<---------------------------------------------------------------------------
#!< MobileNet-v2
#!<---------------------------------------------------------------------------


class _inverted_residual_bottleneck(nn.Module):
  def __init__(self, inp, oup, stride, expand_ratio):
    super(_inverted_residual_bottleneck, self).__init__()
    self.use_res_connect = stride == 1 and inp == oup

    if expand_ratio == 1:
      self.conv = nn.Sequential(
          # dw
          nn.Conv2d(inp * expand_ratio, inp * expand_ratio, 3,
                    stride, 1, groups=inp * expand_ratio, bias=False),
          nn.BatchNorm2d(inp * expand_ratio),
          nn.ReLU6(inplace=True),
          # pw-linear
          nn.Conv2d(inp * expand_ratio, oup, 1, 1, 0, bias=False),
          nn.BatchNorm2d(oup),
      )
    else:
      self.conv = nn.Sequential(
          nn.Sequential(
              # pw
              nn.Conv2d(inp, inp * expand_ratio,
                        1, 1, 0, bias=False),
              nn.BatchNorm2d(inp * expand_ratio),
              nn.ReLU6(inplace=True)
          ),
          nn.Sequential(
              # dw
              nn.Conv2d(inp * expand_ratio, inp * expand_ratio, 3,
                        stride, 1, groups=inp * expand_ratio, bias=False),
              nn.BatchNorm2d(inp * expand_ratio),
              nn.ReLU6(inplace=True),
              # pw-linear
              nn.Conv2d(inp * expand_ratio, oup,
                        1, 1, 0, bias=False),
              nn.BatchNorm2d(oup)
          )
      )
    self.depth = oup

  def forward(self, x):
    if self.use_res_connect:
      return x + self.conv(x)
    else:
      return self.conv(x)


# class MobilenetV2(nn.Module):

#   def __init__(self, depth_multiplier=1.0, min_depth=8, **kwargs):
#     super(MobilenetV2, self).__init__()
#     if 'output_c3' in kwargs:
#       self._output_c3 = True
#     else:
#       self._output_c3 = False

#     self.depth_multiplier = depth_multiplier
#     self.min_depth = min_depth

#     # define backbone network
#     self.depth = lambda d: max(int(d * self.depth_multiplier), self.min_depth)
#     self.features = nn.Sequential(*self.builder_backbone())
#     print(self.features)

#     # define norm layer
#     # self.l2_norm = tw.nn.L2Norm(576, 20)

#     # define extra layer
#     # self.extra = extra_head  # _make_extra(self.arch, self.extra_info)

#     # self.reset_parameters()

#   def builder_backbone(self):

#     # Conv
#     layers = [_conv_bn(3, 32, 3, 2, 1)]
#     in_channels = 32

#     # Residual
#     residual_layers = [1, 2, 3, 4, 3, 3, 1]
#     residual_depths = [16, 24, 32, 64, 96, 160, 320]
#     residual_strides = [1, 2, 2, 2, 1, 2, 1]
#     residual_expand_ratio = [1, 6, 6, 6, 6, 6, 6]
#     for index in range(len(residual_layers)):
#       for num in range(residual_layers[index]):
#         stride = residual_strides[index] if num == 0 else 1
#         layers += [_inverted_residual_bottleneck(in_channels, self.depth(
#             residual_depths[index]), stride, residual_expand_ratio[index])]
#         in_channels = residual_depths[index]
#     layers += [_conv_bn(320, 1280, 1, 1, 0)]

#     return layers

#   # def reset_parameters(self):

#     # for m in self.extra.modules():
#     #   if isinstance(m, nn.Conv2d):
#     #     tw.nn.initialize.xavier(m, distribution='uniform')

#     # norm
#     # tw.nn.initialize.constant(self.l2_norm, self.l2_norm.scale)

#   def forward(self, x):

#     outs = []

#     for k in range(len(self.features)):
#       if k == 7 and self._output_c3:
#         outs.append(x)
#       if k == 14:
#         x = self.features[k].conv[0](x)
#         # x = l2.norm(x)
#         outs.append(x)
#         x = self.features[k].conv[1](x)
#       elif k == 18:
#         x = self.features[k](x)
#         # x = l2.norm(x)
#         outs.append(x)
#       else:
#         x = self.features[k](x)

#     # for k, v in enumerate(self.extra):
#     #   x = v(x)
#     #   outs.append(x)

#     return outs[0] if len(outs) == 1 else tuple(outs)


class ConvBNReLU(nn.Sequential):
  def __init__(self, in_planes, out_planes, kernel_size=3, stride=1, groups=1):
    padding = (kernel_size - 1) // 2
    super(ConvBNReLU, self).__init__(
        nn.Conv2d(in_planes, out_planes, kernel_size, stride,
                  padding, groups=groups, bias=False),
        nn.BatchNorm2d(out_planes),
        nn.ReLU6(inplace=True))


class InvertedResidual(nn.Module):
  def __init__(self, inp, oup, stride, expand_ratio):
    super(InvertedResidual, self).__init__()
    self.stride = stride
    assert stride in [1, 2]

    hidden_dim = int(round(inp * expand_ratio))
    self.use_res_connect = self.stride == 1 and inp == oup

    layers = []
    if expand_ratio != 1:
      # pw
      layers.append(ConvBNReLU(inp, hidden_dim, kernel_size=1))
    layers.extend([
        # dw
        ConvBNReLU(hidden_dim, hidden_dim, stride=stride, groups=hidden_dim),
        # pw-linear
        nn.Conv2d(hidden_dim, oup, 1, 1, 0, bias=False),
        nn.BatchNorm2d(oup),
    ])
    self.conv = nn.Sequential(*layers)

  def forward(self, x):
    if self.use_res_connect:
      return x + self.conv(x)
    else:
      return self.conv(x)


class MobileNetV2(nn.Module):
  def __init__(self, c3=False, width_mult=1.0):
    super(MobileNetV2, self).__init__()
    block = InvertedResidual
    self.c3 = c3
    input_channel = 32
    last_channel = 1280
    inverted_residual_setting = [
        # t, c, n, s
        [1, 16, 1, 1],
        [6, 24, 2, 2],
        [6, 32, 3, 2],
        [6, 64, 4, 2],
        [6, 96, 3, 1],
        [6, 160, 3, 2],
        [6, 320, 1, 1],
    ]

    # building first layer
    input_channel = int(input_channel * width_mult)
    self.last_channel = int(last_channel * max(1.0, width_mult))
    features = [ConvBNReLU(3, input_channel, stride=2)]
    # building inverted residual blocks
    for t, c, n, s in inverted_residual_setting:
      output_channel = int(c * width_mult)
      for i in range(n):
        stride = s if i == 0 else 1
        features.append(
            block(input_channel, output_channel, stride, expand_ratio=t))
        input_channel = output_channel
    # building last several layers
    features.append(ConvBNReLU(
        input_channel, self.last_channel, kernel_size=1))
    # make it nn.Sequential
    self.features = nn.Sequential(*features)

    # building classifier
    # self.classifier = nn.Sequential(
    #     nn.Dropout(0.2),
    #     nn.Linear(self.last_channel, num_classes),
    # )

    # weight initialization
    for m in self.modules():
      if isinstance(m, nn.Conv2d):
        nn.init.kaiming_normal_(m.weight, mode='fan_out')
        if m.bias is not None:
          nn.init.zeros_(m.bias)
      elif isinstance(m, nn.BatchNorm2d):
        nn.init.ones_(m.weight)
        nn.init.zeros_(m.bias)
      elif isinstance(m, nn.Linear):
        nn.init.normal_(m.weight, 0, 0.01)
        nn.init.zeros_(m.bias)

  def forward(self, x):
    
    outs = []
    for i, layer in enumerate(self.features):
      if self.c3 and i == 7:
        outs.append(x) # [1, 32, 40, 40]
      if i == 14:
        x = layer.conv[0](x)
        outs.append(x) # [1, 576, 20, 20]
        x = layer.conv[1](x)
        x = layer.conv[2](x)
        x = layer.conv[3](x)
      elif i == 18:
        x = layer(x)
        outs.append(x) # [1, 1280, 10, 10]
      else:
        x = layer(x)

    return tuple(outs)


#!<---------------------------------------------------------------------------
#!< VGG
#!<---------------------------------------------------------------------------

class VGG16(nn.Module):
  def __init__(self, **kwargs):
    super(VGG16, self).__init__()
    # define backbone network
    self.features = nn.Sequential(
        nn.Conv2d(3, 64, 3, 1, 1),
        nn.ReLU(True),
        nn.Conv2d(64, 64, 3, 1, 1),
        nn.ReLU(True),
        nn.MaxPool2d(2, 2, 0, ceil_mode=True),
        nn.Conv2d(64, 128, 3, 1, 1),
        nn.ReLU(True),
        nn.Conv2d(128, 128, 3, 1, 1),
        nn.ReLU(True),
        nn.MaxPool2d(2, 2, 0, ceil_mode=True),
        nn.Conv2d(128, 256, 3, 1, 1),
        nn.ReLU(True),
        nn.Conv2d(256, 256, 3, 1, 1),
        nn.ReLU(True),
        nn.Conv2d(256, 256, 3, 1, 1),
        nn.ReLU(True),
        nn.MaxPool2d(2, 2, 0, ceil_mode=True),
        nn.Conv2d(256, 512, 3, 1, 1),
        nn.ReLU(True),
        nn.Conv2d(512, 512, 3, 1, 1),
        nn.ReLU(True),
        nn.Conv2d(512, 512, 3, 1, 1),
        nn.ReLU(True),  # 22
        nn.MaxPool2d(2, 2, 0, ceil_mode=True),
        nn.Conv2d(512, 512, 3, 1, 1),
        nn.ReLU(True),
        nn.Conv2d(512, 512, 3, 1, 1),
        nn.ReLU(True),
        nn.Conv2d(512, 512, 3, 1, 1),
        nn.ReLU(True),
        nn.MaxPool2d(3, 1, 1, ceil_mode=False),
        nn.Conv2d(512, 1024, 3, 1, 6, dilation=6),
        nn.ReLU(True),
        nn.Conv2d(1024, 1024, 1, 1, 0),
        nn.ReLU(True))  # 34

    # define norm layer
    # self.l2_norm = tw.nn.L2Norm(512, 20)

    # define extra layer
    # self.extra = extra_head
    self.reset_parameters()

  def reset_parameters(self):
    # backbone
    for m in self.features.modules():
      if isinstance(m, nn.Conv2d):
        tw.nn.initialize.kaiming(m)
      elif isinstance(m, nn.BatchNorm2d):
        tw.nn.initialize.constant(m, 1)
      elif isinstance(m, nn.Linear):
        tw.nn.initialize.normal(m, std=0.01)
    # extra
    # for m in self.extra.modules():
    #   if isinstance(m, nn.Conv2d):
    #     tw.nn.initialize.xavier(m, distribution='uniform')

    # norm
    # tw.nn.initialize.constant(self.l2_norm, self.l2_norm.scale)

  def forward(self, x):
    r""" x should a image tensor [n, c, h, w] """
    outs = []
    # store the backbones feature maps
    for i, layer in enumerate(self.features):
      x = layer(x)
      if i in [22, 34]:
        outs.append(x)

    # extra layer
    # for i, layer in enumerate(self.extra):
    #   x = F.relu(layer(x), inplace=True)
    #   if i % 2 == 1:
    #     outs.append(x)
    # outs[0] = self.l2_norm(outs[0])
    
    return outs[0] if len(outs) == 1 else tuple(outs)


if __name__ == "__main__":
  model = MobileNetV2()
  with torch.no_grad():
    outs = model(torch.rand(1, 3, 320, 320))
    for out in outs:
      print(out.shape)