r"""Video Demo like: https://www.youtube.com/watch?v=MwCgvYtOLS0

  Usage:
    video_demo vid_raw vid_processed output_path

"""

import os
import sys
import cv2
import tqdm
import numpy as np
from multiprocessing import Pool


def render_image(blur, clean, pos, width):
  pos = int(pos)
  blur[:, pos:, :] = clean[:, pos:, :]
  blur[:, pos - width: pos + width, :] = 192
  blur[:, pos - width + 1: pos + width - 1, :] = 255
  return blur


def merge(paths):
  raw_path, new_path, out_path, i, count = paths
  raw_img = cv2.imread(raw_path)
  new_img = cv2.imread(new_path)
  h, w, c = new_img.shape
  raw_img = cv2.resize(raw_img, (w, h))

  # if h < w:
  #   render = np.concatenate([raw_img, new_img], axis=0)
  # else:
  #   render = np.concatenate([raw_img, new_img], axis=1)
  # cv2.imwrite(out_path, render)

  # left and right comparsion
  if i <= count // 4:
    raw_img = render_image(raw_img, new_img, w / 2, 2)

  # from mid-blur to blur (left to right)
  elif i <= count // 2:
    s = (w / 2) / (count / 4)
    raw_img = render_image(raw_img, new_img, (w / 2) + (i - count / 4) * s, 2)

  # from blur to clean (right to left)
  elif i <= 3 * count // 4:
    s = w / (count / 4)
    raw_img = render_image(raw_img, new_img, w - (i - count / 2) * s, 2)

  # keep clean
  else:
    raw_img[:, :, :] = new_img[:, :, :]

  cv2.imwrite(out_path, raw_img)


def demo_on_image(raw_path, new_path):
  r"""
  """
  raw_fold = sorted(os.listdir(raw_path))
  new_fold = sorted(os.listdir(new_path))

  raw_size = len(raw_fold)
  new_size = len(new_fold)
  min_size = min(raw_size, new_size)

  raw_fold = raw_fold[:min_size]
  new_fold = new_fold[:min_size]

  pairs = [p for p in zip(raw_fold, new_fold)]
  count = len(pairs)

  out_path = new_path + '-merge'
  if not os.path.exists(out_path):
    os.mkdir(out_path)

  image_paths = []
  num_frozen_frames = 60

  c = 0
  for i, (raw, new) in enumerate(tqdm.tqdm(pairs)):
    raw_img = os.path.join(raw_path, raw)
    new_img = os.path.join(new_path, new)
    assert os.path.exists(raw_img) and os.path.exists(new_img)

    # if i == count // 4:
    #   for _ in range(num_frozen_frames):
    #     c += 1
    #     out_img = '{}/{:08d}.png'.format(out_path, c)
    #     image_paths.append((raw_img, new_img, out_img, i, count))

    # else:
    c += 1
    out_img = '{}/{:08d}.png'.format(out_path, c)
    image_paths.append((raw_img, new_img, out_img, i, count))

  with Pool(16) as p:
    p.map(merge, image_paths)

  os.system(f'ffmpeg -framerate 25 -i {out_path}/%08d.png -c:v libx264 -crf 18 -vf fps=25 -pix_fmt yuv420p {out_path}.mp4')  # nopep8


# demo_on_image(new_path='_demo/ALL128-FENet.B422.C32-vid_base-LOL.CLIP1',
#               raw_path='_datasets/BigoliveGameSRNewTest/LOL_clip1')
# demo_on_image(new_path='_demo/frvsr-FENetWithWarp.B422.C32-viz-refine-LOL.CLIP2',
#               raw_path='_datasets/BigoliveGameSRNewTest/LOL_clip2')
# demo_on_image(new_path='_demo/ALL128-FENet.B422.C32-vid_base-LOL.CLIP3',
#               raw_path='_datasets/BigoliveGameSRNewTest/LOL_clip3')
# demo_on_image(new_path='_demo/ALL128-FENet.B422.C32-vid_base-SVID_20210427_105357_1',
#               raw_path='_datasets/BigoliveGameSRNewTest/SVID_20210427_105357_1/mtd_SVID_20210427_105357_1_0_640x312.mp4.fold')
# demo_on_image(new_path='_demo/ALL128-FENet.B422.C32-vid_base-SVID_20210427_105627_1',
#               raw_path='_datasets/BigoliveGameSRNewTest/SVID_20210427_105627_1/mtd_SVID_20210427_105627_1_0_640x312.mp4.fold')
# demo_on_image(new_path='_demo/ALL128-FENet.B422.C32-vid_base-SVID_20210427_110149_1',
#               raw_path='_datasets/BigoliveGameSRNewTest/SVID_20210427_110149_1/mtd_SVID_20210427_110149_1_0_640x312.mp4.fold')
# demo_on_image(new_path='_demo/ALL128-FENet.B422.C32-vid_base-SVID_20210427_110805_1',
#               raw_path='_datasets/BigoliveGameSRNewTest/SVID_20210427_110805_1/mtd_SVID_20210427_110805_1_0_640x312.mp4.fold')
# demo_on_image(new_path='_demo/ALL128-FENet.B422.C32-vid_base-SVID_20210427_110917_1',
#               raw_path='_datasets/BigoliveGameSRNewTest/SVID_20210427_110917_1/mtd_SVID_20210427_110917_1_0_640x312.mp4.fold')
# demo_on_image(new_path='_demo/frvsr-FENetWithWarp.B422.C32-viz-refine-SVID_20210506_151543_1',
#               raw_path='_datasets/BigoliveGameSRNewTest/Screen_Recording_Part2/SVID_20210506_151543_1/demo_SVID_20210506_151543_1_0__312.0x640.0.mp4.fold')
# demo_on_image(new_path='_demo/ALL128-FENet.B422.C32-vid_base-SVID_20210506_151655_1',
#               raw_path='_datasets/BigoliveGameSRNewTest/Screen_Recording_Part2/SVID_20210506_151655_1/demo_SVID_20210506_151655_1_0__312.0x640.0.mp4.fold')
# demo_on_image(new_path='_demo/ALL128-FENet.B422.C32-vid_base-SVID_20210506_152405_1',
#               raw_path='_datasets/BigoliveGameSRNewTest/Screen_Recording_Part2/SVID_20210506_152405_1/demo_SVID_20210506_152405_1_0__312.0x640.0.mp4.fold')
# demo_on_image(new_path='_demo/ALL128-FENetWithWarp.B422.C32-gvsr_base-SVID_20210506_154544_1',
#               raw_path='_datasets/BigoliveGameSRNewTest/Screen_Recording_Part2/SVID_20210506_154544_1/demo_SVID_20210506_154544_1_0__640.0x312.0.mp4.fold')
# demo_on_image(new_path='_demo/ALL128-FENet.B422.C32-vid_base-SVID_20210506_154824_1',
#               raw_path='_datasets/BigoliveGameSRNewTest/Screen_Recording_Part2/SVID_20210506_154824_1/demo_SVID_20210506_154824_1_0__640.0x312.0.mp4.fold')
# demo_on_image(new_path='_demo/ALL128-FENet.B422.C32-vid_base-SVID_20210506_154954_1',
#               raw_path='_datasets/BigoliveGameSRNewTest/Screen_Recording_Part2/SVID_20210506_154954_1/demo_SVID_20210506_154954_1_0__640.0x312.0.mp4.fold')
# demo_on_image(new_path='_demo/ALL128-FENet.B422.C32-vid_base-SVID_20210506_155555_1',
#               raw_path='_datasets/BigoliveGameSRNewTest/Screen_Recording_Part2/SVID_20210506_155555_1/demo_SVID_20210506_155555_1_0__640.0x312.0.mp4.fold')
# demo_on_image(new_path='_demo/ALL128-FENet.B422.C32-vid_base-SVID_20210506_155819_1',
#               raw_path='_datasets/BigoliveGameSRNewTest/Screen_Recording_Part2/SVID_20210506_155819_1/demo_SVID_20210506_155819_1_0__640.0x312.0.mp4.fold')
# demo_on_image(new_path='_demo/ALL128-FENet.B422.C32-vid_base-SVID_20210506_155912_1',
#               raw_path='_datasets/BigoliveGameSRNewTest/Screen_Recording_Part2/SVID_20210506_155912_1/demo_SVID_20210506_155912_1_0__640.0x312.0.mp4.fold')


for fold in os.listdir('/data4/jk/tw/research/super_resolution/_datasets/0518/result/'):
  raw = os.path.join('/data4/jk/tw/research/super_resolution/_datasets/0518/result', fold)
  new = os.path.join('_demo/', 'blind_' + fold)
  if os.path.exists(raw) and os.path.exists(new):
  # print(raw, new)
    demo_on_image(raw_path=raw, new_path=new)