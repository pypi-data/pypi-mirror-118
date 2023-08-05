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
"""Affine unittest

  from .primitive.affine import vflip
  from .primitive.affine import hflip
  from .primitive.affine import random_vflip
  from .primitive.affine import random_hflip
  from .primitive.affine import rotate
  from .primitive.affine import random_rotate

"""
import os
import unittest
import cv2
import numpy as np
import torch
from PIL import Image
import tw.transform as T
import matplotlib.pyplot as plt

ROOT = __file__.replace('/', '_').split('.')[0]

class base(unittest.TestCase):
  
  def __init__(self, methodName):
    super().__init__(methodName=methodName)
    self.img1 = 'assets/coco/dog.jpg'
    self.img2 = 'assets/coco/eagle.jpg'
    self.root = f'{ROOT}_{self.__class__.__name__}'
    if not os.path.exists('_outputs'):
      os.mkdir('_outputs')

  @property
  def name(self):
    return f'{ROOT}_{self.__class__.__name__}'

  def load_meta(self):
    m1 = T.ImageMeta(source=T.COLORSPACE.BGR, path=self.img1)
    m2 = T.ImageMeta(source=T.COLORSPACE.BGR, path=self.img2)
    return m1.load().numpy(), m2.load().numpy()

  def load_numpy(self):
    m1 = cv2.imread(self.img1).astype('float32')
    m2 = cv2.imread(self.img2).astype('float32')
    return m1, m2

  def load_tensor(self):
    m1 = torch.from_numpy(cv2.imread(self.img1).astype('float32'))
    m2 = torch.from_numpy(cv2.imread(self.img2).astype('float32'))
    return m1, m2

  def load_pil(self):
    m1 = Image.open(self.img1)
    m2 = Image.open(self.img2)
    return m1, m2

  def draw(self, suffix, aug_list):
    raw_list = self.load_numpy()
    size = len(aug_list)
    for i in range(size):
      plt.subplot(size, size, i + 1)
      plt.title(f'raw_{i+1}')
      plt.axis('off')
      plt.imshow(cv2.cvtColor(raw_list[i] / 255.0, cv2.COLOR_BGR2RGB))
    for i in range(size):
      plt.subplot(size, size, size + i + 1)
      plt.axis('off')
      plt.title(f'aug_{i+1}')
      plt.imshow(aug_list[i])
    plt.savefig('_outputs/' + self.name + suffix)
    plt.close()


#-----------------------------------------------------------------------
# VFLIP
#-----------------------------------------------------------------------
class vflip(base):

  def test_meta(self):
    m1, m2 = self.load_meta()
    sample = [m1, m2]
    T.change_colorspace(sample, src=T.COLORSPACE.BGR, dst=T.COLORSPACE.RGB)
    T.vflip(sample)
    self.draw('_meta.png', [m1.bin / 255.0, m2.bin / 255.0])

  def test_numpy(self):
    m1, m2 = self.load_numpy()
    m1 = T.change_colorspace(m1, src=T.COLORSPACE.BGR, dst=T.COLORSPACE.RGB)
    m2 = T.change_colorspace(m2, src=T.COLORSPACE.BGR, dst=T.COLORSPACE.RGB)
    m1 = T.vflip(m1)
    m2 = T.vflip(m2)
    self.draw('_numpy.png', [m1 / 255.0, m2 / 255.0])

  def test_tensor(self):
    m1, m2 = self.load_tensor()
    m1 = m1.permute(2, 0, 1) / 255.0
    m2 = m2.permute(2, 0, 1) / 255.0
    m1 = T.change_colorspace(m1, src=T.COLORSPACE.BGR, dst=T.COLORSPACE.RGB)
    m2 = T.change_colorspace(m2, src=T.COLORSPACE.BGR, dst=T.COLORSPACE.RGB)
    m1 = T.vflip(m1)
    m2 = T.vflip(m2)
    self.draw('_tensor.png', [m1.permute(1, 2, 0).numpy(), m2.permute(1, 2, 0).numpy()])

  def test_pil(self):
    m1, m2 = self.load_pil()
    m1 = T.vflip(m1)
    m2 = T.vflip(m2)
    self.draw('_pil.png', [m1, m2])


#-----------------------------------------------------------------------
# HFLIP
#-----------------------------------------------------------------------
class hflip(base):

  def test_meta(self):
    m1, m2 = self.load_meta()
    sample = [m1, m2]
    T.change_colorspace(sample, src=T.COLORSPACE.BGR, dst=T.COLORSPACE.RGB)
    T.hflip(sample)
    self.draw('_meta.png', [m1.bin / 255.0, m2.bin / 255.0])

  def test_numpy(self):
    m1, m2 = self.load_numpy()
    m1 = T.change_colorspace(m1, src=T.COLORSPACE.BGR, dst=T.COLORSPACE.RGB)
    m2 = T.change_colorspace(m2, src=T.COLORSPACE.BGR, dst=T.COLORSPACE.RGB)
    m1 = T.hflip(m1)
    m2 = T.hflip(m2)
    self.draw('_numpy.png', [m1 / 255.0, m2 / 255.0])

  def test_tensor(self):
    m1, m2 = self.load_tensor()
    m1 = m1.permute(2, 0, 1) / 255.0
    m2 = m2.permute(2, 0, 1) / 255.0
    m1 = T.change_colorspace(m1, src=T.COLORSPACE.BGR, dst=T.COLORSPACE.RGB)
    m2 = T.change_colorspace(m2, src=T.COLORSPACE.BGR, dst=T.COLORSPACE.RGB)
    m1 = T.hflip(m1)
    m2 = T.hflip(m2)
    self.draw('_tensor.png', [m1.permute(1, 2, 0).numpy(), m2.permute(1, 2, 0).numpy()])

  def test_pil(self):
    m1, m2 = self.load_pil()
    m1 = T.hflip(m1)
    m2 = T.hflip(m2)
    self.draw('_pil.png', [m1, m2])


#-----------------------------------------------------------------------
# ROTATE
#-----------------------------------------------------------------------
class rotate(base):

  def test_meta(self):
    m1, m2 = self.load_meta()
    sample = [m1, m2]
    T.change_colorspace(sample, src=T.COLORSPACE.BGR, dst=T.COLORSPACE.RGB)
    T.rotate(sample, 30)
    self.draw('_meta.png', [m1.bin / 255.0, m2.bin / 255.0])

  def test_numpy(self):
    m1, m2 = self.load_numpy()
    m1 = T.change_colorspace(m1, src=T.COLORSPACE.BGR, dst=T.COLORSPACE.RGB)
    m2 = T.change_colorspace(m2, src=T.COLORSPACE.BGR, dst=T.COLORSPACE.RGB)
    m1 = T.rotate(m1, 30)
    m2 = T.rotate(m2, 30)
    self.draw('_numpy.png', [m1 / 255.0, m2 / 255.0])

  def test_tensor(self):
    m1, m2 = self.load_tensor()
    m1 = m1.permute(2, 0, 1) / 255.0
    m2 = m2.permute(2, 0, 1) / 255.0
    m1 = T.change_colorspace(m1, src=T.COLORSPACE.BGR, dst=T.COLORSPACE.RGB)
    m2 = T.change_colorspace(m2, src=T.COLORSPACE.BGR, dst=T.COLORSPACE.RGB)
    m1 = T.rotate(m1[None], 30)[0]
    m2 = T.rotate(m2[None], 30)[0]
    self.draw('_tensor.png', [m1.permute(1, 2, 0).numpy(), m2.permute(1, 2, 0).numpy()])

  # def test_pil(self):
  #   raise NotImplementedError


if __name__ == "__main__":
  unittest.main()
