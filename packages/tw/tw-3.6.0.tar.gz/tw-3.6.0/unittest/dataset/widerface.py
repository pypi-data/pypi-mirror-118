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
from tw.datasets.widerface import WiderFace
import tw.transform as T


class WiderfaceTest(unittest.TestCase):

  def _transform_rgb_train(self, metas):
    T.random_zoom_in_crop(metas)
    T.random_photometric_distortion(metas)
    T.pad_to_square(metas)
    T.random_hflip(metas)
    T.resize(metas, 640, 640)
    # T.to_tensor(metas, mean=[104.0, 117.0, 123.0])
    return metas
  
  def test_widerface(self):
    path = 'research/detection/_datasets/widerface/train/label.txt'
    dataset = WiderFace(path, self._transform_rgb_train)

    img, bbox, pts = dataset[3]

    print(img.bin.shape)
    print(pts.keypoints.shape)
    print(bbox.bboxes.shape)
    
    print(bbox.bboxes)
    print(pts.keypoints)

    render = tw.drawer.boundingbox(img.bin, bbox.bboxes, labels=bbox.label)
    render = tw.drawer.keypoints(render, pts.keypoints, radius=2)
    cv2.imwrite('demo.png', render)


if __name__ == "__main__":
  unittest.main()
