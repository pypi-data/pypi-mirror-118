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
"""Pad

  from .primitive.pad import pad
  from .primitive.pad import pad_to_size_divisible
  from .primitive.pad import pad_to_square
  from .primitive.pad import random_expand
  from .primitive.pad import pad_to_target_size

"""
import os
import unittest
import cv2
import numpy as np
import torch
from PIL import Image
import tw
import tw.transform as T
import matplotlib.pyplot as plt

ROOT = __file__.replace('/', '_').split('.')[0]


class base(unittest.TestCase):

  def __init__(self, methodName):
    super().__init__(methodName=methodName)
    self.img1 = 'assets/coco/dog.jpg'
    self.root = f'{ROOT}_{self.__class__.__name__}'
    if not os.path.exists('_outputs'):
      os.mkdir('_outputs')

  @property
  def name(self):
    return f'{ROOT}_{self.__class__.__name__}'

  def load_meta(self):
    m1 = T.ImageMeta(source=T.COLORSPACE.BGR, path=self.img1)
    m1.load()
    bbox1 = T.BoxListMeta()
    bbox1.add(130, 139, 570, 425, 'bicycle')
    bbox1.add(126, 225, 313, 546, 'dog')
    bbox1.set_affine_size(max_h=m1.h, max_w=m1.w)
    return [m1.numpy(), bbox1.numpy()]


# -----------------------------------------------------------------------
# pad_to_target_size
# -----------------------------------------------------------------------
class pad_to_target_size(base):

  def test_meta(self):
    sample = self.load_meta()
    T.pad_to_target_size(sample, 1024, 1024, fill_value=255)
    render = tw.drawer.boundingbox(sample[0].bin, sample[1].bboxes)
    cv2.imwrite('_outputs/unittest_transform_pad_to_target_size_meta.png', render)


if __name__ == "__main__":
  unittest.main()
