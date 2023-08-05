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
import cv2
import unittest
import tw
import tw.transform as T
from matplotlib import pyplot as plt


class QualityAssessTest(unittest.TestCase):

  def transform(self, metas):
    # T.change_colorspace(metas, T.COLORSPACE.BGR, T.COLORSPACE.RGB)
    return metas

  def visualize(self, img1, img2, name):
    fig = plt.figure()
    plt.subplot(1, 2, 1)
    plt.imshow(img1.bin / 255.0)
    if isinstance(img1.label, list):
      plt.title('{}: {:.4f}'.format(os.path.basename(img1.path), img2.label))
      subtitle = f'FR: {name}'
    else:
      plt.title('{}: {:.4f}'.format(os.path.basename(img1.path), img1.label))
      subtitle = f'NR: {name}'
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.imshow(img2.bin / 255.0)
    plt.title('{}: {:.4f}'.format(os.path.basename(img2.path), img2.label))
    plt.axis('off')
    plt.tight_layout()
    fig.suptitle(subtitle)
    plt.savefig(f'quality_assess.{name}.png')

  def test_PIPAL(self):
    path = '_datasets/quality_assess/PIPAL'
    print(path)
    dataset = tw.datasets.PIPAL(path, self.transform, phase=tw.phase.train)
    tw.datasets.PIPAL(path, self.transform, phase=tw.phase.train, split=(0, 180))
    tw.datasets.PIPAL(path, self.transform, phase=tw.phase.train, split=(180, 200))
    tw.datasets.PIPAL(path, self.transform, phase=tw.phase.test)
    img, distort = dataset[0]
    self.visualize(img, distort, 'PIPAL')

  def test_TID2013(self):
    path = '_datasets/quality_assess/TID2013/mos_with_names.txt'
    print(path)
    dataset = tw.datasets.TID2013(path, self.transform)
    tw.datasets.TID2013(path, self.transform, split=[i for i in range(0, 20)])
    tw.datasets.TID2013(path, self.transform, split=[i for i in range(20, 25)])
    img, distort = dataset[0]
    self.visualize(img, distort, 'TID2013')

  def test_LIVE2005(self):
    path = '_datasets/quality_assess/LIVE2005'
    print(path)
    dataset = tw.datasets.LIVE2005(path, self.transform)
    tw.datasets.LIVE2005(path, self.transform, split=[i for i in range(0, 23)])
    tw.datasets.LIVE2005(path, self.transform, split=[i for i in range(23, 29)])
    img, distort = dataset[0]
    self.visualize(img, distort, 'LIVE2005')

  def test_LIVEMD(self):
    path = '_datasets/quality_assess/LIVEMD'
    print(path)
    dataset = tw.datasets.LIVEMD(path, self.transform)
    tw.datasets.LIVEMD(path, self.transform, split=[i for i in range(0, 12)])
    tw.datasets.LIVEMD(path, self.transform, split=[i for i in range(12, 15)])
    img, distort = dataset[0]
    self.visualize(img, distort, 'LIVEMD')

  def test_CSIQ(self):
    path = '_datasets/quality_assess/CSIQ/csiq.txt'
    print(path)
    dataset = tw.datasets.CSIQ(path, self.transform)
    tw.datasets.CSIQ(path, self.transform, split=[i for i in range(24)])
    tw.datasets.CSIQ(path, self.transform, split=[i for i in range(24, 30)])
    img, distort = dataset[0]
    self.visualize(img, distort, 'CSIQ')

  def test_KonIQ10k(self):
    path = '_datasets/quality_assess/koniq10k/koniq10k_scores_and_distributions.csv'
    print(path)
    dataset = tw.datasets.KonIQ10k(path, self.transform, phase=tw.phase.train)
    tw.datasets.KonIQ10k(path, self.transform, phase=tw.phase.val)
    tw.datasets.KonIQ10k(path, self.transform, phase=tw.phase.test)
    img1, img2 = dataset[0][0], dataset[1][0]
    self.visualize(img1, img2, 'KonIQ10k')

  def test_LIVEC(self):
    path = '_datasets/quality_assess/LIVEC'
    print(path)
    dataset = tw.datasets.LIVEC(path, self.transform)
    tw.datasets.LIVEC(path, self.transform, split=[i for i in range(0, 930)])
    tw.datasets.LIVEC(path, self.transform, split=[i for i in range(930, 1162)])
    img1, img2 = dataset[0][0], dataset[1][0]
    self.visualize(img1, img2, 'LIVEC')

  def test_FLIVE(self):
    path = '_datasets/quality_assess/FLIVE/all_patches.csv'
    print(path)
    dataset1 = tw.datasets.FLIVE(path, self.transform, phase=tw.phase.train)
    dataset2 = tw.datasets.FLIVE(path, self.transform, phase=tw.phase.val)
    dataset3 = tw.datasets.FLIVE(path, self.transform, phase=tw.phase.test)
    img, bbox = dataset1[394]
    print(img)
    render = tw.drawer.boundingbox(img.bin, bbox.bboxes, labels=bbox.label, bbox_thick=1)
    cv2.imwrite(f'quality_assess.FLIVE.train.png', render)
    img, bbox = dataset2[394]
    print(img)
    render = tw.drawer.boundingbox(img.bin, bbox.bboxes, labels=bbox.label, bbox_thick=1)
    cv2.imwrite(f'quality_assess.FLIVE.val.png', render)
    img, bbox = dataset3[394]
    print(img)
    render = tw.drawer.boundingbox(img.bin, bbox.bboxes, labels=bbox.label, bbox_thick=1)
    cv2.imwrite(f'quality_assess.FLIVE.test.png', render)


if __name__ == "__main__":
  tw.logger.init('unittest.dataset.quality_assess.log', './')
  unittest.main()
