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
from tw.datasets.coco import CocoDetection
import tw.transform as T


class CocoTest(unittest.TestCase):

  def _transform_rgb_train(self, metas):

    T.random_photometric_distortion(metas)
    T.random_expand(metas, ratio_range=(1, 4), mean=(0, 0, 0))
    T.minimum_iou_random_crop(metas, min_ious=(0.1, 0.3, 0.5, 0.7, 0.9, 1.0), min_crop_size=0.3)
    T.random_hflip(metas)
    T.resize(metas, 300, 300)
    T.to_tensor(metas, mean=[104.0, 117.0, 123.0])
    return metas

  def test_coco2017(self):
    dataset = CocoDetection(root='_datasets/coco2017/val2017',
                            annotation='_datasets/coco2017/annotations/instances_val2017.json',
                            transform=self._transform_rgb_train,
                            phase=tw.phase.val,
                            with_bbox=True,
                            with_segm=False,
                            with_kps=False,
                            background_offset=1,
                            num_classes=81)

    img, bbox = dataset[10]

    print(img)
    print(bbox)

    render = tw.drawer.boundingbox(img.bin, bbox.bboxes, labels=bbox.caption, bbox_thick=1)
    # render = tw.drawer.keypoints(render, pts.keypoints, radius=2)
    cv2.imwrite('demo.png', render)


if __name__ == "__main__":
  unittest.main()
