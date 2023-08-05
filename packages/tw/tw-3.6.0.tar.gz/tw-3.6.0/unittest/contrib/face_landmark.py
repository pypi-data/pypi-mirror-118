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


class FaceLandmarkTest(unittest.TestCase):

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

  def draw_pts(self, image, pts_list):

    output = image.copy()

    for pts in pts_list:
      for x, y in pts:
        output = cv2.circle(output, (x, y), radius=0, color=(255, 0, 0), thickness=2)

    return output

  def test_image(self):
    """test on image
    """
    # prepare output
    if not os.path.exists('_outputs'):
      os.mkdir('_outputs')
    dst = __file__.replace('/', '_').split('.')[0]

    # load a rgb numpy image
    image = cv2.imread('assets/face/12_Group_Group_12_Group_Group_12_24.jpg')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    device = 'cpu'
    landmarkers = {
        'MobileNet_GDConv': tw.contrib.face_landmark.MobileFace(
            device=device,
            net='MobileNet_GDConv',
            pretrain='_checkpoints/face_landmark/mobileface/mobilenet_224_model_best_gdconv_external.pth.tar'),
        'MobileNet_GDConv_56': tw.contrib.face_landmark.MobileFace(
            device=device,
            net='MobileNet_GDConv_56',
            pretrain='_checkpoints/face_landmark/mobileface/mobilenet_56_model_best_gdconv.pth.tar'),
        'MobileNet_GDConv_SE': tw.contrib.face_landmark.MobileFace(
            device=device,
            net='MobileNet_GDConv_SE',
            pretrain='_checkpoints/face_landmark/mobileface/MobileNetV2_SE_RE_model_best.pth.tar'),
        'MobileFaceNet': tw.contrib.face_landmark.MobileFace(
            device=device,
            net='MobileFaceNet',
            pretrain='_checkpoints/face_landmark/mobileface/mobilefacenet_model_best.pth.tar'),
        'PFLD': tw.contrib.face_landmark.MobileFace(
            device=device,
            net='PFLD',
            pretrain='_checkpoints/face_landmark/mobileface/pfld_model_best.pth.tar'),
    }

    # we use retinanet as face detector
    detector = tw.contrib.face_detection.RetinafaceDetector(device=device)
    bboxes, _ = detector.detect_faces(image)
    rendered = self.draw_bboxes(image, bboxes)

    for k, landmarker in landmarkers.items():

      render_pts = rendered.copy()

      for bbox in bboxes:
        # crop face
        x1, y1, x2, y2 = bbox[0:4]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        w = x2 - x1 + 1
        h = y2 - y1 + 1
        face = image[y1: y2, x1: x2]

        # to tensor
        inputs = landmarker.preprocess(face)

        # detect faces
        t1 = time.time()
        coords = landmarker.detect(inputs)
        t2 = time.time()
        print(f'[INFO] {k} elapsed {(t2 - t1) * 1000} ms.')

        # re-aspect to image -> [68, 2] to [1, 68, 2]
        coords = landmarker.postprocess(coords, x1, y1, w, h)[None]

        render_pts = self.draw_pts(render_pts, coords.detach().cpu().numpy())

      render_pts = cv2.cvtColor(render_pts, cv2.COLOR_RGB2BGR)
      cv2.imwrite(f'_outputs/{dst}_{k}.png', render_pts)


if __name__ == "__main__":
  unittest.main()
