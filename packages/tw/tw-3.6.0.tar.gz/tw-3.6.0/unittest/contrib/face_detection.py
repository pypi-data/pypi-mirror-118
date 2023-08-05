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
import tw
import time


class FaceDetectorTest(unittest.TestCase):

  def draw_bboxes(self, image, bounding_boxes, fill=0.0, thickness=3):

    # it will be returned
    output = image.copy()

    # fill with transparency
    if fill > 0.0:

      # fill inside bboxes
      img_fill = image.copy()
      for bbox in bounding_boxes:
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[2]), int(bbox[3]))
        img_fill = cv2.rectangle(img_fill, p1, p2, (0, 255, 0), -1)

      # overlay
      cv2.addWeighted(img_fill, fill, output, 1.0 - fill, 0, output)

    # edge with thickness
    for bbox in bounding_boxes:
      p1 = (int(bbox[0]), int(bbox[1]))
      p2 = (int(bbox[2]), int(bbox[3]))
      green = int(bbox[4] * 255)
      output = cv2.rectangle(output, p1, p2, (255, green, 0), thickness)

    return output

  def test_image(self):
    """test on single image for face detector.
    """
    # prepare output
    if not os.path.exists('_outputs'):
      os.mkdir('_outputs')
    dst = __file__.replace('/', '_').split('.')[0]

    # load a rgb numpy image
    image = cv2.imread('assets/face/12_Group_Group_12_Group_Group_12_24.jpg')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # prepare detector
    device = 'cpu'
    detectors = {
        'dsfd': tw.contrib.face_detection.DSFD(device=device),
        'faceboxes': tw.contrib.face_detection.FaceBoxes(device=device),
        'mtcnn': tw.contrib.face_detection.MTCNN(device=device),
        'pyramidbox': tw.contrib.face_detection.PyramidBox(device=device),
        'retinaface': tw.contrib.face_detection.RetinafaceDetector(device=device),
        's3fd': tw.contrib.face_detection.S3FD(device=device),
        'tinyface': tw.contrib.face_detection.TinyFace(device=device),
    }

    for k, det in detectors.items():

      if k in ['retinaface', 'mtcnn']:
        bboxes, _ = det.detect_faces(image)
      else:
        bboxes = det.detect_faces(image)

      render = self.draw_bboxes(image, bboxes, fill=0.2, thickness=3)
      render = cv2.cvtColor(render, cv2.COLOR_RGB2BGR)
      cv2.imwrite(f'_outputs/{dst}_{k}.png', render)


if __name__ == "__main__":
  unittest.main()
