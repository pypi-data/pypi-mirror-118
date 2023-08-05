# Copyright 2017 The KaiJIN Authors. All Rights Reserved.
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
import os
from tw.nn.search import KnnSearch
import unittest
import time

import cv2
import numpy as np

import torch
from torch.utils import data

import tw
import tw.transform as T


class SensatUrbanTest(unittest.TestCase):

  def test_sensat_urban(self):
    orginal_path = '_datasets/SensatUrban_Dataset/sensaturban/original_block_ply'
    grid_path = '_datasets/SensatUrban_Dataset/sensaturban/grid_0.200'
    dataset = tw.datasets.SensatUrban(orginal_path, grid_path, phase=tw.phase.train, batchsize=4, step=500)
    # dataset1 = tw.datasets.SensatUrban(orginal_path, grid_path, phase=tw.phase.val, batchsize=32, step=400)
    # dataset2 = tw.datasets.SensatUrban(orginal_path, grid_path, phase=tw.phase.test, batchsize=32, step=400)
    print(len(dataset))

    for i in range(len(dataset)):
      sample = dataset[i]
      print(dataset.min_possibility)

    # load a batch of data
    # pc_xyz, pc_features, pc_labels, pc_idx, pc_cloud_idx = [], [], [], [], []
    # for i in range(4):
    #   meta: T.PointCloudMeta = dataset0[i][0]
    #   pc_xyz.append(meta.points)
    #   pc_features.append(meta.colors)
    #   pc_labels.append(meta.labels)
    #   pc_idx.append(meta.index)
    #   pc_cloud_idx.append(meta.cloud)
    # pc_xyz = np.array(pc_xyz)
    # pc_features = np.array(pc_features)
    # pc_labels = np.array(pc_labels)
    # pc_idx = np.array(pc_idx)
    # pc_cloud_idx = np.array(pc_cloud_idx)

    # # prepare batch data
    # k_n = 16
    # num_layers = 5
    # sub_sampling_ratio = [4, 4, 4, 4, 2]
    # knn_search = tw.nn.KnnSearch(k=k_n)

    # input_points = []
    # input_neighbors = []
    # input_pools = []
    # input_up_samples = []

    # # form [4, 65536] -> [4, 256]
    # for i in range(num_layers):
    #   # find neighbour_idx of pc_xyz
    #   bs, num_points, _ = pc_xyz.shape
    #   neighbour_idx = knn_search(pc_xyz, pc_xyz)  # pc_xyz [4, 65546, 3], idx[4, 65536, 16]
    #   # sample top-k sub-samples
    #   sub_points = pc_xyz[:, :num_points // sub_sampling_ratio[i], :]  # [4, 16384, 3]
    #   pool_i = neighbour_idx[:, :num_points // sub_sampling_ratio[i], :]  # [4, 16384, 3]
    #   # find nearest points for each pc_xyz in sub_points
    #   up_i = knn_search(sub_points, pc_xyz)  # [4, 65536, 16]
    #   input_points.append(torch.tensor(pc_xyz))
    #   input_neighbors.append(torch.tensor(neighbour_idx))
    #   input_pools.append(torch.tensor(pool_i))
    #   input_up_samples.append(torch.tensor(up_i))
    #   # next, we use sub_points to sample. aka. <random pool>
    #   pc_xyz = sub_points

    # for i in zip(input_points, input_neighbors, input_pools, input_up_samples):
    #   print(i[0].shape, i[1].shape, i[2].shape, i[3].shape)


if __name__ == "__main__":
  unittest.main()
