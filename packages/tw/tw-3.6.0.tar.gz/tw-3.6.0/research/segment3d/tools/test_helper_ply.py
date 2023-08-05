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

import numpy as np
from tw.utils import parser_ply


def read_ply_data(path, with_rgb=True, with_label=True):
  data = parser_ply.read_ply(path)
  xyz = np.vstack((data['x'], data['y'], data['z'])).T
  if with_rgb and with_label:
    rgb = np.vstack((data['red'], data['green'], data['blue'])).T
    labels = data['class']
    return xyz.astype(np.float32), rgb.astype(np.uint8), labels.astype(np.uint8)
  elif with_rgb and not with_label:
    rgb = np.vstack((data['red'], data['green'], data['blue'])).T
    return xyz.astype(np.float32), rgb.astype(np.uint8)
  elif not with_rgb and with_label:
    labels = data['class']
    return xyz.astype(np.float32), labels.astype(np.uint8)
  elif not with_rgb and not with_label:
    return xyz.astype(np.float32)

# downsampled data
xyz, rgb, labels = read_ply_data('_datasets/SensatUrban_Dataset/sensaturban/grid_0.200/birmingham_block_0.ply')
print(xyz.shape, rgb.shape, labels.shape)
print(xyz[0], rgb[0], labels[0])

# original data
xyz, rgb, labels = read_ply_data('_datasets/SensatUrban_Dataset/sensaturban/original_block_ply/birmingham_block_0.ply')
print(xyz.shape, rgb.shape, labels.shape)
print(xyz[0], rgb[0], labels[0])
