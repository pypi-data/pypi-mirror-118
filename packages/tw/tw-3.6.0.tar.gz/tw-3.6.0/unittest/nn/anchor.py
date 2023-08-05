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

import tw
from tw.nn import anchor


class AnchorTest(unittest.TestCase):

  def test_anchor_base(self):
    anchors = anchor.generate_anchors(stride=16, sizes=(32, 64), aspect_ratios=(1, 2))
    print(anchors)

  def test_anchor_generator(self):
    gen = anchor.GeneralAnchorGenerator(
        stride=16,
        sizes=(32, 64),
        ratios=(1, 2),
        straddle_thresh=0)

    x = torch.tensor([1, 2, 3])
    y = torch.tensor([4, 5, 6])
    z = torch.tensor([7, 8])
    gx, gy, gz = torch.meshgrid(x, y, z)
    # print(gx.shape, gy.shape, gz.shape)
    # print(gx, gy, gz)

  def test_retinanet_anchor_generator(self):
    # retinanet for imagenet
    gen = anchor.RetinaNetAnchorGenerator(
        anchor_sizes=[32, 64, 128, 256, 512],
        anchor_strides=[8, 16, 32, 64, 128],
        anchor_ratios=[0.5, 1.0, 2.0],
        straddle_thresh=0.0,
        octave=2.0,
        scales_per_octave=3)

  def test_retinaface_anchor_generator(self):
    # retinaface
    gen = anchor.RetinaFaceAnchorGenerator(
        anchor_sizes=[[32, 64], [64, 128], [128, 256]],
        anchor_strides=[8, 16, 32],
        anchor_ratios=[1.0, ])

    anchors = gen.forward([[32, 32], [16, 16], [8, 8]], 256, 256)
    # print(anchors)
    print([anchor.shape for anchor in anchors])


if __name__ == "__main__":
  unittest.main()
