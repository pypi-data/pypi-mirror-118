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
import unittest
import cv2
import time
import torch
from torch import nn

from torch import _ops

import torchvision
import tw


class RoIPoolTest(unittest.TestCase):

  def test_roi_pool(self):
    inputs = torch.arange(0, 16 * 16 * 2).reshape(2, 1, 16, 16).float().cuda()
    pool = tw.nn.RoIPool([1, 1], 1 / 16.0).cuda()
    rois = torch.tensor([[0, 0, 0, 32, 32], [0, 0, 0, 255, 255], [1, 0, 0, 255, 255]]).float().cuda()
    print(rois)

    print(inputs, inputs.shape)
    print(rois.shape)
    outputs = pool(inputs,rois)
    print(outputs.shape)
    print(outputs)


if __name__ == "__main__":
  unittest.main()
