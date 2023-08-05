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

import functools
from typing import Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F

import tw

# ACTIVATION = functools.partial(nn.LeakyReLU, negative_slope=0.2, inplace=True)
# ACTIVATION_FN = functools.partial(F.leaky_relu, negative_slope=0.2)

# ACTIVATION = tw.nn.Swish
# SwishFn = tw.nn.Swish()
# ACTIVATION_FN = SwishFn.forward

# ACTIVATION = functools.partial(tw.nn.Mish, inplace=True)
# from tw.nn.activation import mish
# ACTIVATION_FN = mish


class _BNBase(nn.Sequential):

  def __init__(self, in_size, batch_norm=None, name=""):
    super().__init__()
    self.add_module(name + "bn", batch_norm(in_size, momentum=0.1))
    nn.init.constant_(self[0].weight, 1.0)
    nn.init.constant_(self[0].bias, 0)


class BatchNorm1d(_BNBase):

  def __init__(self, in_size: int, *, name: str = ""):
    super().__init__(in_size, batch_norm=nn.BatchNorm1d, name=name)


class BatchNorm2d(_BNBase):

  def __init__(self, in_size: int, name: str = ""):
    super().__init__(in_size, batch_norm=nn.BatchNorm2d, name=name)


class _ConvBase(nn.Sequential):

  def __init__(
          self,
          in_size,
          out_size,
          kernel_size,
          stride,
          padding,
          activation,
          bn,
          init,
          conv=None,
          batch_norm=None,
          bias=True,
          preact=False,
          name="",
          instance_norm=False,
          instance_norm_func=None
  ):
    super().__init__()
    
    # bn = False
    # instance_norm=False

    bias = bias and (not bn)
    conv_unit = conv(
        in_size,
        out_size,
        kernel_size=kernel_size,
        stride=stride,
        padding=padding,
        bias=bias
    )
    nn.init.normal_(conv_unit.weight, 0, 0.01)
    # init(conv_unit.weight)
    if bias:
      nn.init.normal_(conv_unit.bias, 0, 0.01)
      # nn.init.constant_(conv_unit.bias, 0)

    if bn:
      if not preact:
        bn_unit = batch_norm(out_size)
      else:
        bn_unit = batch_norm(in_size)
    if instance_norm:
      if not preact:
        in_unit = instance_norm_func(out_size, affine=False, track_running_stats=False)
      else:
        in_unit = instance_norm_func(in_size, affine=False, track_running_stats=False)

    if preact:
      if bn:
        self.add_module(name + 'bn', bn_unit)

      if activation is not None:
        self.add_module(name + 'activation', activation)

      if not bn and instance_norm:
        self.add_module(name + 'in', in_unit)

    self.add_module(name + 'conv', conv_unit)

    if not preact:
      if bn:
        self.add_module(name + 'bn', bn_unit)

      if activation is not None:
        self.add_module(name + 'activation', activation)

      if not bn and instance_norm:
        self.add_module(name + 'in', in_unit)


class Conv1d(_ConvBase):

  def __init__(
          self,
          in_size: int,
          out_size: int,
          *,
          kernel_size: int = 1,
          stride: int = 1,
          padding: int = 0,
          activation=nn.LeakyReLU(0.2, inplace=True),
          bn: bool = False,
          init=nn.init.kaiming_normal_,
          bias: bool = True,
          preact: bool = False,
          name: str = "",
          instance_norm=False
  ):
    super().__init__(
        in_size,
        out_size,
        kernel_size,
        stride,
        padding,
        activation,
        bn,
        init,
        conv=nn.Conv1d,
        batch_norm=BatchNorm1d,
        bias=bias,
        preact=preact,
        name=name,
        instance_norm=instance_norm,
        instance_norm_func=nn.InstanceNorm1d
    )


class Conv2d(_ConvBase):

  def __init__(
          self,
          in_size: int,
          out_size: int,
          *,
          kernel_size: Tuple[int, int] = (1, 1),
          stride: Tuple[int, int] = (1, 1),
          padding: Tuple[int, int] = (0, 0),
          activation=nn.LeakyReLU(0.2, inplace=True),
          bn: bool = False,
          init=nn.init.kaiming_normal_,
          bias: bool = True,
          preact: bool = False,
          name: str = "",
          instance_norm=False
  ):
    super().__init__(
        in_size,
        out_size,
        kernel_size,
        stride,
        padding,
        activation,
        bn,
        init,
        conv=nn.Conv2d,
        batch_norm=BatchNorm2d,
        bias=bias,
        preact=preact,
        name=name,
        instance_norm=instance_norm,
        instance_norm_func=nn.InstanceNorm2d
    )


class Att_pooling(nn.Module):

  def __init__(self, d_in, d_out):
    super(Att_pooling, self).__init__()

    self.fc = nn.Conv2d(d_in, d_in, (1, 1), bias=True)
    self.mlp = Conv2d(d_in, d_out, kernel_size=(1, 1), bn=True, activation=nn.LeakyReLU(0.2, inplace=True))

  def forward(self, feature_set):

    att_activation = self.fc(feature_set)
    att_scores = F.softmax(att_activation, dim=3)
    f_agg = feature_set * att_scores
    f_agg = torch.sum(f_agg, dim=3, keepdim=True)
    f_agg = self.mlp(f_agg)

    return f_agg


class Building_block(nn.Module):

  def __init__(self, d_out):
    super(Building_block, self).__init__()

    self.mlp1 = Conv2d(10, d_out//2, kernel_size=(1, 1), bn=True, activation=nn.LeakyReLU(0.2, inplace=True))
    self.att_pooling_1 = Att_pooling(d_out, d_out//2)

    self.mlp2 = Conv2d(d_out//2, d_out//2, kernel_size=(1, 1), bn=True, activation=nn.LeakyReLU(0.2, inplace=True))
    self.att_pooling_2 = Att_pooling(d_out, d_out)

  def forward(self, xyz, feature, neigh_idx):

    f_xyz = self.relative_pos_encoding(xyz, neigh_idx)
    f_xyz = f_xyz.permute((0, 3, 1, 2))
    f_xyz = self.mlp1(f_xyz)
    f_neighbours = self.gather_neighbour(feature.squeeze(-1).permute((0, 2, 1)), neigh_idx)
    f_neighbours = f_neighbours.permute((0, 3, 1, 2))
    f_concat = torch.cat([f_neighbours, f_xyz], dim=1)
    f_pc_agg = self.att_pooling_1(f_concat)

    f_xyz = self.mlp2(f_xyz)
    f_neighbours = self.gather_neighbour(f_pc_agg.squeeze(-1).permute((0, 2, 1)), neigh_idx)
    f_neighbours = f_neighbours.permute((0, 3, 1, 2))
    f_concat = torch.cat([f_neighbours, f_xyz], dim=1)
    f_pc_agg = self.att_pooling_2(f_concat)

    return f_pc_agg

  def relative_pos_encoding(self, xyz, neigh_idx):

    neighbor_xyz = self.gather_neighbour(xyz, neigh_idx)
    xyz_tile = xyz.unsqueeze(2).repeat(1, 1, neigh_idx.shape[-1], 1)
    relative_xyz = xyz_tile - neighbor_xyz
    relative_dis = torch.sqrt(torch.sum(torch.pow(relative_xyz, 2), dim=-1, keepdim=True))
    relative_feature = torch.cat([relative_dis, relative_xyz, xyz_tile, neighbor_xyz], dim=-1)

    return relative_feature

  @staticmethod
  def gather_neighbour(pc, neighbor_idx):

    batch_size, num_points, d = pc.shape[0], pc.shape[1], pc.shape[2]

    index_input = neighbor_idx.reshape(batch_size, -1)
    features = torch.gather(input=pc, dim=1, index=index_input.unsqueeze(-1).repeat(1, 1, pc.shape[2]))
    features = features.reshape(batch_size, num_points, neighbor_idx.shape[-1], d)

    return features


class Dilated_res_block(nn.Module):

  def __init__(self, d_in, d_out):
    super(Dilated_res_block, self).__init__()

    self.mlp1 = Conv2d(d_in, d_out // 2, kernel_size=(1, 1), bn=True, activation=nn.LeakyReLU(0.2, inplace=True))
    self.lfa = Building_block(d_out)
    self.mlp2 = Conv2d(d_out, d_out * 2, kernel_size=(1, 1), bn=True, activation=None)
    self.shortcut = Conv2d(d_in, d_out * 2, kernel_size=(1, 1), bn=True, activation=None)

  def forward(self, feature, xyz, neigh_idx):

    f_pc = self.mlp1(feature)
    f_pc = self.lfa(xyz, f_pc, neigh_idx)
    f_pc = self.mlp2(f_pc)

    shortcut = self.shortcut(feature)

    return F.leaky_relu(f_pc + shortcut, negative_slope=0.2)


class RandLANet(nn.Module):

  def __init__(self, num_classes=13, num_layers=6, decoder_feature_dims=[16, 64, 128, 256, 512]):
    super(RandLANet, self).__init__()
    self.num_layers = num_layers
    self.num_classes = num_classes

    self.fc0 = Conv1d(6, 8, kernel_size=1, bn=True, bias=True)

    d_in = 8
    self.dilated_res_blocks = nn.ModuleList()
    for index in range(num_layers):
      d_out = decoder_feature_dims[index]
      self.dilated_res_blocks.append(Dilated_res_block(d_in, d_out))
      d_in = 2 * d_out

    d_out = d_in
    self.decoder_0 = Conv2d(d_in, d_out, kernel_size=(1, 1), bn=True, activation=nn.LeakyReLU(0.2, inplace=True))

    self.decoder_blocks = nn.ModuleList()
    for index in range(num_layers):
      if index < 4:
        d_in = d_out + 2 * decoder_feature_dims[-index - 2]
        d_out = 2 * decoder_feature_dims[-index - 2]
      else:
        d_in = 4 * decoder_feature_dims[-5]
        d_out = 2 * decoder_feature_dims[-5]
      self.decoder_blocks.append(Conv2d(d_in, d_out, kernel_size=(1, 1), bn=True, activation=nn.LeakyReLU(0.2, inplace=True)))

    self.fc1 = Conv2d(d_out, 64, kernel_size=(1, 1), bn=True, activation=nn.LeakyReLU(0.2, inplace=True))
    self.fc2 = Conv2d(64, 32, kernel_size=(1, 1), bn=True, activation=nn.LeakyReLU(0.2, inplace=True))
    self.dropout = nn.Dropout(0.5)
    self.fc3 = Conv2d(32, num_classes, kernel_size=(1, 1), bn=False, activation=nn.LeakyReLU(0.2, inplace=True))

  def forward(self, xyz, neigh_idx, sub_idx, interp_idx, features):

    features = features.transpose(1, 2)
    features = self.fc0(features)
    features = features.unsqueeze(dim=3)

    # Encoder Phase
    f_encoder_list = []
    for index in range(self.num_layers):
      f_encoder_index = self.dilated_res_blocks[index](features, xyz[index], neigh_idx[index])
      f_sampled_index = self.random_sample(f_encoder_index, sub_idx[index])
      features = f_sampled_index

      if index == 0:
        f_encoder_list.append(f_encoder_index)

      f_encoder_list.append(f_sampled_index)

    # Bridge Phase
    features = self.decoder_0(f_encoder_list[-1])

    # Decoder Phase
    f_decoder_list = []
    for index in range(self.num_layers):
      f_interp_index = self.nearest_interpolation(features, interp_idx[-index - 1])
      f_decoder_index = self.decoder_blocks[index](torch.cat([f_encoder_list[-index - 2], f_interp_index], dim=1))

      features = f_decoder_index
      f_decoder_list.append(f_decoder_index)

    # segmentation Phase
    features = self.fc1(features)
    features = self.fc2(features)
    features = self.dropout(features)
    features = self.fc3(features)
    f_out = features.squeeze(3).transpose(1, 2)

    return f_out

  @staticmethod
  def random_sample(feature, pool_idx):

    feature = feature.squeeze(dim=3)
    num_neigh = pool_idx.shape[-1]
    d = feature.shape[1]
    batch_size = pool_idx.shape[0]
    pool_idx = pool_idx.reshape(batch_size, -1)
    pool_features = torch.gather(feature, 2, pool_idx.unsqueeze(1).repeat(1, feature.shape[1], 1))
    pool_features = pool_features.reshape(batch_size, d, -1, num_neigh)
    pool_features = pool_features.max(dim=3, keepdim=True)[0]

    return pool_features

  @staticmethod
  def nearest_interpolation(feature, interp_idx):

    feature = feature.squeeze(dim=3)
    batch_size = interp_idx.shape[0]
    up_num_points = interp_idx.shape[1]
    interp_idx = interp_idx.reshape(batch_size, up_num_points)
    interpolated_features = torch.gather(feature, 2, interp_idx.unsqueeze(1).repeat(1, feature.shape[1], 1))
    interpolated_features = interpolated_features.unsqueeze(3)

    return interpolated_features
