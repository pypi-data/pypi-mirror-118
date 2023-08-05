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
"""Face Detector Demo"""
import os
import tqdm
import argparse
import numpy as np
import cv2
import tw


class FaceDetectorDemo():

  def __init__(self, config):
    """Face detector demo

    Args:
        config (parser): configuration from command line.
    """

    self.config = config
    device = config.device

    # initialize detector
    if self.config.model_detection == 'dsfd':
      self.detector = tw.contrib.face_detection.DSFD(device=device)
    elif self.config.model_detection == 'faceboxes':
      self.detector = tw.contrib.face_detection.FaceBoxes(device=device)
    elif self.config.model_detection == 'mtcnn':
      self.detector = tw.contrib.face_detection.MTCNN(device=device)
    elif self.config.model_detection == 'pyramidbox':
      self.detector = tw.contrib.face_detection.PyramidBox(device=device)
    elif self.config.model_detection == 'retinaface':
      self.detector = tw.contrib.face_detection.RetinafaceDetector(device=device)
    elif self.config.model_detection == 's3fd':
      self.detector = tw.contrib.face_detection.S3FD(device=device)
    elif self.config.model_detection == 'tinyface':
      self.detector = tw.contrib.face_detection.TinyFace(device=device)
    else:
      self.detector = None

    # initialize landmark
    if self.config.model_landmark == 'MobileNet_GDConv':
      self.landmarker = tw.contrib.face_landmark.MobileFace(
          device=device,
          net='MobileNet_GDConv',
          pretrain='_checkpoints/face_landmark/mobileface/mobilenet_224_model_best_gdconv_external.pth.tar')
    elif self.config.model_landmark == 'MobileNet_GDConv_56':
      self.landmarker = tw.contrib.face_landmark.MobileFace(
          device=device,
          net='MobileNet_GDConv_56',
          pretrain='_checkpoints/face_landmark/mobileface/mobilenet_56_model_best_gdconv.pth.tar')
    elif self.config.model_landmark == 'MobileNet_GDConv_SE':
      self.landmarker = tw.contrib.face_landmark.MobileFace(
          device=device,
          net='MobileNet_GDConv_SE',
          pretrain='_checkpoints/face_landmark/mobileface/MobileNetV2_SE_RE_model_best.pth.tar')
    elif self.config.model_landmark == 'MobileFaceNet':
      self.landmarker = tw.contrib.face_landmark.MobileFace(
          device=device,
          net='MobileFaceNet',
          pretrain='_checkpoints/face_landmark/mobileface/mobilefacenet_model_best.pth.tar')
    elif self.config.model_landmark == 'PFLD':
      self.landmarker = tw.contrib.face_landmark.MobileFace(
          device=device,
          net='PFLD',
          pretrain='_checkpoints/face_landmark/mobileface/pfld_model_best.pth.tar')
    else:
      self.landmarker = None

  def inference(self, frame):
    """Inference a numpy like frame [H, W, C] [0-255] in RGB format.

    Args:
        frame ([np.ndarray]): frame with [H, W, C] shape and [0-255] uint8 RGB.

    Raises:
        NotImplementedError: [description]
        NotImplementedError: [description]
        NotImplementedError: [description]

    Returns:
        [bboxes]: [N, (x1, y1, x2, y2, conf, label)]
        [pts]: [N, pts(68), 2(x, y)]
    """

    bboxes = None
    pts = None

    if self.config.bbox:
      if self.config.model_detection in ['mtcnn', 'retinaface']:
        bboxes, _ = self.detector.detect_faces(frame)
      elif self.config.model_detection in ['dsfd', 'faceboxes', 'pyramidbox', 's3fd', 'tinyface']:
        bboxes = self.detector.detect_faces(frame)
      else:
        raise NotImplementedError(self.config.model_detection)

    if self.config.landmark:
      if self.config.model_landmark in ['MobileNet_GDConv', 'MobileNet_GDConv_56', 'MobileNet_GDConv_SE', 'MobileFaceNet', 'PFLD']:
        pts = []
        for bbox in bboxes:
          # crop face
          x1, y1, x2, y2 = bbox[0:4]
          x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
          w = x2 - x1 + 1
          h = y2 - y1 + 1
          face = frame[y1: y2, x1: x2]
          inputs = self.landmarker.preprocess(face)
          coords = self.landmarker.detect(inputs)
          coords = self.landmarker.postprocess(coords, x1, y1, w, h)
          coords = coords.detach().cpu().numpy()
          pts.append(coords)
      else:
        raise NotImplementedError(self.config.landmark)

    return bboxes, pts

  def draw_bboxes(self, image, bounding_boxes, fill=0.0, thickness=2, color=None):
    """[summary]

    Args:
        image ([type]): [description]
        bounding_boxes ([type]): [description]
        fill (float, optional): [description]. Defaults to 0.0.
        thickness (int, optional): [description]. Defaults to 3.

    Returns:
        [type]: [description]
    """

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
      if color is None:
        color = (255, int(bbox[4] * 255), 0)
      output = cv2.rectangle(output, p1, p2, color, thickness)

    return output

  def draw_pts(self, image, pts_list):
    """[summary]

    Args:
        image ([type]): [description]
        pts_list ([type]): [num_pts, pairs, (x, y)]

    Returns:
        [type]: [description]
    """

    output = image.copy()

    for pts in pts_list:
      for x, y in pts:
        output = cv2.circle(output, (int(x), int(y)), radius=0, color=(255, 0, 0), thickness=3)

    return output

  def __call__(self):

    cfg = self.config
    device = self.config.device
    viz_input = self.config.viz_input
    viz_output = self.config.viz_output

    images, videos = tw.media.collect(viz_input)
    if not os.path.exists(viz_output):
      os.makedirs(viz_output)

    # process videos
    for file_id, filepath in enumerate(sorted(videos)):

      try:
        # 188_BigoLiveBenchmark/over-exposed/094_720x1280.mp4
        dst = '/'.join(filepath.split('/')[-3:])
        dst = os.path.join(viz_output, dst)
        if not os.path.exists(os.path.dirname(dst)):
          os.makedirs(os.path.dirname(dst))

        # output in terms of video
        reader = tw.media.VideoReader(filepath, to_rgb=True)
        writer = tw.media.VideoWriter(dst, reader.width, reader.height, reader.fps)
        tw.logger.info(f'Processing {filepath} -> {dst}, {file_id} / {len(videos)}')

        # output bboxes
        fw_bbox = open(dst + '.bboxes.txt', 'w')

        # output landmarks
        if cfg.landmark:
          fw_pts = open(dst + '.pts.txt', 'w')

        # use pts to inference bounding box
        if cfg.refine_bbox:
          assert cfg.landmark
          fw_bbox_refine = open(dst + '.bboxes_refine.txt', 'w')

        for idx, frame in enumerate(tqdm.tqdm(reader)):

          # inference bboxes and pts
          bboxes, pts = self.inference(frame)

          # copy to prepare render meta info
          rendered = frame.copy()

          # inference bboxes
          if bboxes is not None:
            rendered = self.draw_bboxes(rendered, bboxes)
            # to log
            for bbox in bboxes:
              fw_bbox.write(f'{idx}, {bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]}, {bbox[4]}, 0\n')

          # inference points
          if pts is not None:
            rendered = self.draw_pts(rendered, pts)

            # to log
            for p in pts:
              fw_pts.write('{}, {}\n'.format(idx, ', '.join([f'{i[0]}, {i[1]}' for i in p])))

            # convert landmarks to bbox
            if cfg.refine_bbox:
              refine_bbox = []
              for p in pts:
                x1, y1 = np.min(p[:, 0]), np.min(p[:, 1])
                x2, y2 = np.max(p[:, 0]), np.max(p[:, 1])
                refine_bbox.append((x1, y1, x2, y2, 1.0))
                fw_bbox_refine.write(f'{idx}, {x1}, {y1}, {x2}, {y2}, 1.0, 0\n')
              rendered = self.draw_bboxes(rendered, refine_bbox, color=(0, 0, 255))

          # convert to BGR
          # cv2.imwrite('test.png', cv2.cvtColor(rendered, cv2.COLOR_RGB2BGR))
          writer.write(cv2.cvtColor(rendered, cv2.COLOR_RGB2BGR))

        fw_bbox.close()
        if cfg.landmark:
          fw_pts.close()
        if cfg.refine_bbox:
          fw_bbox_refine.close()

      except:
        print(f'Failed to process {filepath}')

    # process images
    for filepath in tqdm.tqdm(sorted(images)):

      dst = os.path.join(viz_output, os.path.basename(filepath))

      # output bboxes
      fw_bbox = open(dst + '.bboxes.txt', 'w')

      # output landmarks
      if cfg.landmark:
        fw_pts = open(dst + '.pts.txt', 'w')

      # use pts to inference bounding box
      if cfg.refine_bbox:
        assert cfg.landmark
        fw_bbox_refine = open(dst + '.bboxes_refine.txt', 'w')

      frame = cv2.imread(filepath)
      frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

      # inference bboxes and pts
      bboxes, pts = self.inference(frame)

      # copy to prepare render meta info
      rendered = frame.copy()

      # inference bboxes
      if bboxes is not None:
        rendered = self.draw_bboxes(rendered, bboxes)
        # to log
        for idx, bbox in enumerate(bboxes):
          fw_bbox.write(f'{idx}, {bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]}, {bbox[4]}, 0\n')

      # inference points
      if pts is not None:
        rendered = self.draw_pts(rendered, pts)

        # to log
        for idx, p in enumerate(pts):
          fw_pts.write('{}, {}\n'.format(idx, ', '.join([f'{i[0]}, {i[1]}' for i in p])))

        # convert landmarks to bbox
        if cfg.refine_bbox:
          refine_bbox = []
          for idx, p in enumerate(pts):
            x1, y1 = np.min(p[:, 0]), np.min(p[:, 1])
            x2, y2 = np.max(p[:, 0]), np.max(p[:, 1])
            refine_bbox.append((x1, y1, x2, y2, 1.0))
            fw_bbox_refine.write(f'{idx}, {x1}, {y1}, {x2}, {y2}, 1.0, 0\n')
          rendered = self.draw_bboxes(rendered, refine_bbox, color=(0, 0, 255))

      # convert to BGR
      cv2.imwrite(dst, cv2.cvtColor(rendered, cv2.COLOR_RGB2BGR))

      fw_bbox.close()
      if cfg.landmark:
        fw_pts.close()
      if cfg.refine_bbox:
        fw_bbox_refine.close()


if __name__ == "__main__":

  parser = argparse.ArgumentParser()

  detect_models = [
      'dsfd',
      'faceboxes',
      'mtcnn',
      'pyramidbox',
      'retinaface',
      's3fd',
      'tinyface',
  ]

  landmark_models = [
      'MobileNet_GDConv',
      'MobileNet_GDConv_56',
      'MobileNet_GDConv_SE',
      'MobileFaceNet',
      'PFLD',
  ]

  # ---------------------------------------------
  #  USED BY MODEL-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--model-detection', type=str, default=None, choices=detect_models)
  parser.add_argument('--model-landmark', type=str, default=None, choices=landmark_models)

  parser.add_argument('--bbox', action="store_true", help="output bbox.")
  parser.add_argument('--refine-bbox', action="store_true", help="refine bbox by landmarks.")
  parser.add_argument('--landmark', action="store_true", help="output landmarks.")

  parser.add_argument('--input-colorspace', type=str, default='Y', choices=['Y', 'RGB', 'YUV'])

  # ---------------------------------------------
  #  USED BY VIZ-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--viz-input', type=str, help='input path could be a folder/filepath.')
  parser.add_argument('--viz-output', type=str, help='output path should be a folder path.')

  # generate config
  args, _ = parser.parse_known_args()

  tw.runner.launch(parser, FaceDetectorDemo)
