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
import torch
import torch.nn as nn
import torch.nn.functional as F

import tw


def conv1d(in_channels, out_channels, kernel_size, stride, padding, bn=True, activation=True):
  return nn.Sequential(
      nn.Conv1d(in_channels, out_channels, kernel_size, stride, padding, bias=True),
      nn.BatchNorm1d(out_channels) if bn else nn.Identity(),
      nn.LeakyReLU(negative_slope=0.2, inplace=True) if activation else nn.Identity())


def conv2d(in_channels, out_channels, kernel_size, stride, padding, bn=True, activation=True):
  return nn.Sequential(
      nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding, bias=True),
      nn.BatchNorm2d(out_channels) if bn else nn.Identity(),
      nn.LeakyReLU(negative_slope=0.2, inplace=True) if activation else nn.Identity())


class AttentionPooling(nn.Module):

  def __init__(self, d_in, d_out):
    super(AttentionPooling, self).__init__()
    self.fc = nn.Conv2d(d_in, d_in, 1, 1, 0, bias=True)
    self.mlp = conv2d(d_in, d_out, 1, 1, 0)

  def forward(self, feature_set):
    """simple attention with sum pooling: fc((softmax(fc(x)) * x).sum(dim=3))

    Args:
        feature_set ([torch.Tensor]): [bs, d_in, num_points, num_neighbor]

    Returns:
        [torch.Tensor]: [bs, d_out, num_points, 1]
    """
    att_activation = self.fc(feature_set)
    att_scores = F.softmax(att_activation, dim=3)
    f_agg = feature_set * att_scores
    f_agg = torch.sum(f_agg, dim=3, keepdim=True)
    f_agg = self.mlp(f_agg)
    return f_agg


class DilatedResidualBlock(nn.Module):

  def __init__(self, d_out):
    super(DilatedResidualBlock, self).__init__()

    self.mlp1 = conv2d(10, d_out // 2, 1, 1, 0)
    self.att_pooling_1 = AttentionPooling(d_out, d_out // 2)

    self.mlp2 = conv2d(d_out // 2, d_out // 2, 1, 1, 0)
    self.att_pooling_2 = AttentionPooling(d_out, d_out)

  def forward(self, xyz, feature, neigh_idx):
    """(xyz)->LocSE + AttentivePooling + (xyz)->LocSE + Attentive Pooling

    Args:
        xyz ([torch.Tensor]): [bs, num_points, 3]
        feature ([torch.Tensor]): [bs, num_points, ndim]
        neigh_idx ([torch.Tensor]): [bs, num_points, num_neighbour]

    Returns:
        [torch.Tensor]: [bs, num_neighbour, num_points, 1]
    """

    # [bs, num_points, num_neighbour, 10]
    f_xyz = self.relative_pos_encoding(xyz, neigh_idx)

    # [bs, 10, num_points, num_neighbour]
    f_xyz = f_xyz.permute((0, 3, 1, 2))

    # [bs, ndim, num_points, num_neighbour] xyz mapping to same dim with feature
    f_xyz1 = self.mlp1(f_xyz)

    # [bs, num_points, num_neighbour, ndim]
    f_neighbours = self.gather_neighbour(feature.squeeze(-1).permute((0, 2, 1)), neigh_idx)

    # [bs, ndim, num_points, num_neighbor]
    f_neighbours = f_neighbours.permute((0, 3, 1, 2))

    # [bs, 2*ndim, num_points, num_neighbor]
    f_concat = torch.cat([f_neighbours, f_xyz1], dim=1)

    # [bs, ndim, num_points, 1]
    f_pc_agg = self.att_pooling_1(f_concat)

    # ---------

    # [bs, ndim, num_points, num_neighbor]
    f_xyz2 = self.mlp2(f_xyz1)

    # [bs, num_points, num_neighbor, ndim]
    f_neighbours = self.gather_neighbour(f_pc_agg.squeeze(-1).permute((0, 2, 1)), neigh_idx)

    # [bs, ndim, num_points, num_neighbor]
    f_neighbours = f_neighbours.permute((0, 3, 1, 2))

    # [bs, 2*ndim, num_points, num_neighbor]
    f_concat = torch.cat([f_neighbours, f_xyz2], dim=1)

    # [bs, 2*dim, num_points, 1]
    f_pc_agg = self.att_pooling_2(f_concat)

    return f_pc_agg

  def relative_pos_encoding(self, xyz, neigh_idx):
    """build relationship between xyz and its neighbours by: (x-x')^2, |x-x'|, x, x'

    Args:
        xyz ([torch.Tensor]): [bs, num_points, 3]
        neigh_idx ([torch.Tensor]): [bs, num_points, num_neighbour]

    Returns:
        [torch.Tensor]: [bs, num_points, num_neighbour, 10]
    """

    # pick current xyz neighbour points [bs, num_points, num_neighbour, 3]
    neighbor_xyz = self.gather_neighbour(xyz, neigh_idx)

    # repeat to num_neighbour points [bs, num_points, num_neighbour, 3]
    xyz_tile = xyz.unsqueeze(2).repeat(1, 1, neigh_idx.shape[-1], 1)

    # relative distance between xyz and its neighbours
    relative_xyz = xyz_tile - neighbor_xyz

    # euclidean distance (sphere)
    relative_dis = torch.sqrt(torch.sum(torch.pow(relative_xyz, 2), dim=-1, keepdim=True))

    # (x-x')^2, |x-x'|, x, x' [bs, num_points, num_neighbour, 10]
    relative_feature = torch.cat([relative_dis, relative_xyz, xyz_tile, neighbor_xyz], dim=-1)

    return relative_feature

  @staticmethod
  def gather_neighbour(pc, neighbor_idx):
    """gather point clouds neighbour points

    Args:
        pc ([torch.Tensor]): [bs, num_points, features]
        neighbor_idx ([torch.Tensor]): [bs, num_points, num_neighbor]

    Returns:
        [torch.Tensor]: [bs, num_points, num_neighbor, features]
    """
    batch_size, num_points, d = pc.shape[0], pc.shape[1], pc.shape[2]
    index_input = neighbor_idx.reshape(batch_size, -1)
    features = torch.gather(input=pc, dim=1, index=index_input.unsqueeze(-1).repeat(1, 1, pc.shape[2]))
    features = features.reshape(batch_size, num_points, neighbor_idx.shape[-1], d)
    return features


class DilatedResidualAttention(nn.Module):

  def __init__(self, d_in, d_out):
    super(DilatedResidualAttention, self).__init__()
    self.mlp1 = conv2d(d_in, d_out // 2, 1, 1, 0)
    self.lfa = DilatedResidualBlock(d_out)
    self.mlp2 = conv2d(d_out, d_out * 2, 1, 1, 0, activation=False)
    self.shortcut = conv2d(d_in, d_out * 2, 1, 1, 0, activation=False)
    self.out = nn.LeakyReLU(negative_slope=0.2, inplace=True)

  def forward(self, feature, xyz, neigh_idx):
    f_pc = self.mlp1(feature)
    f_pc = self.lfa(xyz, f_pc, neigh_idx)
    f_pc = self.mlp2(f_pc)
    shortcut = self.shortcut(feature)
    return self.out(f_pc + shortcut)


class RandLANetPlus(nn.Module):

  def __init__(self, num_classes=13, num_layers=6, feature_dims=[16, 64, 128, 256, 512]):
    super(RandLANetPlus, self).__init__()
    self.num_layers = num_layers
    self.num_classes = num_classes

    # mapping xyz-rgb to feature space
    self.stem = conv1d(6, 8, 1, 1, 0)

    # build encoder blocks
    d_in = 8
    self.dilated_res_blocks = nn.ModuleList()
    for index in range(num_layers):
      d_out = feature_dims[index]
      self.dilated_res_blocks.append(DilatedResidualAttention(d_in, d_out))
      d_in = 2 * d_out

    # build decoder blocks
    d_out = d_in
    self.decoder_0 = conv2d(d_in, d_out, 1, 1, 0)

    # from high to low
    self.decoder_blocks = nn.ModuleList()
    for index in range(num_layers):
      if index < 4:
        d_in = d_out + 2 * feature_dims[-index - 2]
        d_out = 2 * feature_dims[-index - 2]
      else:
        d_in = 4 * feature_dims[-5]
        d_out = 2 * feature_dims[-5]
      self.decoder_blocks.append(conv2d(d_in, d_out, 1, 1, 0))

    # output layer
    self.head = nn.Sequential(
        conv2d(d_out, 64, 1, 1, 0),
        conv2d(64, 32, 1, 1, 0),
        nn.Dropout(0.5),
        nn.Conv2d(32, num_classes, 1, 1, 0, bias=True))

  def forward(self, xyz, neigh_idx, sub_idx, interp_idx, features):
    # [N, points, xyz-rgb] to [N, xyz-rgb, points]
    features = features.transpose(1, 2)
    features = self.stem(features)  # [16, 8, 16384]
    # [N, xyz-rgb, points, 1]
    features = features.unsqueeze(dim=3)  # [16, 8, 16384, 1]

    # encoder phase
    # xyz:           [16, 16384, 3], [16, 4096, 3], [16, 1024, 3], [16, 256, 3], [16, 64, 3]
    # neigh_idx:     [16, 16384, 16], [16, 4096, 16], [16, 1024, 16], [16, 256, 16], [16, 64, 16]
    # sub_idx:       [16, 4096, 16], [16, 1024, 16], [16, 256, 16], [16, 64, 16], [16, 32, 16]
    # f_encode_idx:  [16, 32, 16384, 1], [16, 128, 4096, 1], [16, 256, 1024, 1], [16, 512, 256, 1], [16, 1024, 64, 1]
    # f_sample_idx:  [16, 32, 4096, 1], [16, 128, 1024, 1], [16, 256, 256, 1], [16, 512, 64, 1], [16, 1024, 32, 1]
    f_encoder_list = []
    for index in range(self.num_layers):
      f_encoder_index = self.dilated_res_blocks[index](features, xyz[index], neigh_idx[index])
      f_sampled_index = self.random_sample(f_encoder_index, sub_idx[index])
      features = f_sampled_index
      if index == 0:
        f_encoder_list.append(f_encoder_index)
      f_encoder_list.append(f_sampled_index)

    # bridge phase [16, 1024, 32, 1]
    features = self.decoder_0(f_encoder_list[-1])

    # decoder phase
    # features:         [16, 32, 16384, 1], [16, 32, 4096, 1], [16, 128, 1024, 1], [16, 256, 256, 1], [16, 512, 64, 1], [16, 1024, 32, 1]
    # interp_idx:       [16, 16384, 1], [16, 4096, 1], [16, 1024, 1], [16, 256, 1], [16, 64, 1]
    # interp_index:     [16, 1024, 64, 1], [16, 512, 256, 1], [16, 256, 1024, 1], [16, 128, 4096, 1], [16, 32, 16384, 1]
    # up_and_bilateral: [16, 1536, 64, 1], [16, 768, 256, 1], [16, 384, 1024, 1], [16, 160, 4096, 1], [16, 64, 16384, 1]
    # decoder_index:    [16, 512, 64, 1], [16, 256, 256, 1], [16, 128, 1024, 1], [16, 32, 4096, 1], [16, 32, 16384, 1]
    for index in range(self.num_layers):
      f_interp_index = self.nearest_interpolation(features, interp_idx[-index - 1])
      f_up_and_bilateral = torch.cat([f_encoder_list[-index - 2], f_interp_index], dim=1)
      f_decoder_index = self.decoder_blocks[index](f_up_and_bilateral)
      features = f_decoder_index

    # segmentation phase [16, 13, 16384, 1]
    features = self.head(features)
    # segmentation output [16, 16384, 13]
    f_out = features.squeeze(3).transpose(1, 2)

    return f_out

  @staticmethod
  def random_sample(feature, pool_idx):
    """sample point from feature in terms of pool_idx with max value.

      It actually does downsample operation among nearest points (e.g. 16) to
        pick up maximum feature value, while the feature maybe varied.

    Args:
        feature ([torch.Tensor]): [bs, ndim, num_points]
        pool_idx ([torch.Tensor]): [bs, sub_num_points, neighbour]

    Note:
        generally, num_points = scale * sub_num_points

    """
    bs, ndim = feature.shape[0], feature.shape[1]
    num_neigh = pool_idx.shape[-1]

    # [16, 32, 16384, 1]
    feature = feature.squeeze(dim=3)
    # [16, 4096 * 16]
    pool_idx = pool_idx.reshape(bs, -1)

    # index from [16, 4096 * 16] to [16, 1, 4096 * 16] and repeat second dim to [16, 32, 4096 * 16]
    index = pool_idx.unsqueeze(1).repeat(1, ndim, 1)

    # pick element according with `index` at dim 2 (num_points)
    pool_features = torch.gather(feature, 2, index)

    # [16, 32, 65536] -> [16, 32, 4096, 16]
    pool_features = pool_features.reshape(bs, ndim, -1, num_neigh)

    # select max neighbour feature -> [16, 32, 4096, 1]
    pool_features = pool_features.max(dim=3, keepdim=True)[0]

    return pool_features

  @staticmethod
  def nearest_interpolation(feature, interp_idx):
    """point cluster upsample operation.

    Args:
        feature ([torch.Tensor]): [bs, ndim, num_points, 1]
        interp_idx ([torch.Tensor]): [bs, up_num_points, neighbour, 1]

    Note:
        generally, up_num_points = scale * num_points

    """
    batch_size, up_num_points = interp_idx.shape[0], interp_idx.shape[1]
    ndim = feature.shape[1]

    # squeeze to [bs, ndim, num_points]
    feature = feature.squeeze(dim=3)

    # reshape to [bs, up_num_points]
    interp_idx = interp_idx.reshape(batch_size, up_num_points)

    # repeat to [bs, ndim, up_num_points]
    index = interp_idx.unsqueeze(1).repeat(1, ndim, 1)

    # pick up neighbour points
    interpolated_features = torch.gather(feature, 2, index)

    # [bs, ndim, up_num_points, 1]
    interpolated_features = interpolated_features.unsqueeze(3)

    return interpolated_features
