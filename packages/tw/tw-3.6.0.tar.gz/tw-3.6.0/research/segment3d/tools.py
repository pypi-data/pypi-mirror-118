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
"""Point Cloud Manipulate Tools

  1) ensemble multiple model
  2) merge multiple clouds into one
  3) display single model accuracy
  4) grid downsample cloud points upsample to whole.

"""
import os
import torch
import tqdm
import numpy as np
import argparse
from sklearn.metrics import confusion_matrix
from tw.evaluator.segmentation import PointCloudSegmentEvaluator, display_confusion_matrix
from tw.utils.parser_ply import read_ply, write_ply, read_ply_data


def sensat_urban(dataset, subset=''):

  names = {0: 'Ground', 1: 'HighVegetation', 2: 'Buildings', 3: 'Walls', 4: 'Bridge', 5: 'Parking',
           6: 'Rail', 7: 'TrafficRoads', 8: 'StreetFurniture', 9: 'Cars', 10: 'Footpath', 11: 'Bikes', 12: 'Water'}

  colors = {0: [85, 107, 47], 1: [0, 255, 0], 2: [255, 165, 0], 3: [41, 49, 101],
            4: [0, 0, 0], 5: [0, 0, 255], 6: [255, 0, 255], 7: [200, 200, 200],
            8: [89, 47, 95], 9: [255, 0, 0], 10: [255, 255, 0], 11: [0, 255, 255],
            12: [0, 191, 255]}

  num_points = {
      'birmingham_block_1': {'path': '_datasets/SensatUrban_Dataset/sensaturban/grid_0.200/birmingham_block_1.ply', 'num_points': 4824245, },
      'birmingham_block_5': {'path': '_datasets/SensatUrban_Dataset/sensaturban/grid_0.200/birmingham_block_5.ply', 'num_points': 6567731, },
      'cambridge_block_10': {'path': '_datasets/SensatUrban_Dataset/sensaturban/grid_0.200/cambridge_block_10.ply', 'num_points': 6640765, },
      'cambridge_block_7': {'path': '_datasets/SensatUrban_Dataset/sensaturban/grid_0.200/cambridge_block_7.ply', 'num_points': 10564913, },
      'birmingham_block_2': {'path': '_datasets/SensatUrban_Dataset/sensaturban/grid_0.200/birmingham_block_2.ply', 'num_points': 3444876, },
      'birmingham_block_8': {'path': '_datasets/SensatUrban_Dataset/sensaturban/grid_0.200/birmingham_block_8.ply', 'num_points': 5762068, },
      'cambridge_block_15': {'path': '_datasets/SensatUrban_Dataset/sensaturban/grid_0.200/cambridge_block_15.ply', 'num_points': 9570781, },
      'cambridge_block_16': {'path': '_datasets/SensatUrban_Dataset/sensaturban/grid_0.200/cambridge_block_16.ply', 'num_points': 9267511, },
      'cambridge_block_22': {'path': '_datasets/SensatUrban_Dataset/sensaturban/grid_0.200/cambridge_block_22.ply', 'num_points': 7293688, },
      'cambridge_block_27': {'path': '_datasets/SensatUrban_Dataset/sensaturban/grid_0.200/cambridge_block_27.ply', 'num_points': 8462044, },
  }

  if dataset.startswith('test'):
    if subset == 'birmingham':
      sets = ['birmingham_block_2', 'birmingham_block_8']
    elif subset == 'cambridge':
      sets = ['cambridge_block_15', 'cambridge_block_16', 'cambridge_block_22', 'cambridge_block_27']
    else:
      sets = ['birmingham_block_2', 'birmingham_block_8', 'cambridge_block_15', 'cambridge_block_16', 'cambridge_block_22', 'cambridge_block_27']  # nopep8
  elif dataset.startswith('val'):
    if subset == 'birmingham':
      sets = ['birmingham_block_1', 'birmingham_block_5']
    elif subset == 'cambridge':
      sets = ['cambridge_block_10', 'cambridge_block_7']
    else:
      sets = ['birmingham_block_1', 'birmingham_block_5', 'cambridge_block_10', 'cambridge_block_7']
  else:
    raise NotImplementedError(subset)

  point_clouds = [num_points[pc] for pc in sets]

  return point_clouds, names, colors


def _gather_batch_data(path, cloud_points, num_classes=13, output=None):
  """gather batch data into non-overlapping data

  Args:
      path ([str]): path to pth of val/test data.

  Returns:
      [dict]:
        preds: [(pc1, num_classes), (pc2, num_classes), ...]
        labels: [(pc1, ), (pc2, ), ...]
        features: [(pc1, 6), (pc2, 6), ...]
  """

  # load cache if existed.
  cache_path = f'{path[:-4]}.cache.pth' if output is None else output
  if os.path.exists(cache_path):
    whole = torch.load(cache_path, 'cpu')
    return whole

  # loading data
  data = torch.load(path, 'cpu')

  # allocate space
  whole = {
      'preds': [torch.zeros(num, num_classes).float() for num in cloud_points],
      'labels': [torch.zeros(num, ).long() for num in cloud_points],
      'features': [torch.zeros(num, 6).float() for num in cloud_points],
  }

  for item in tqdm.tqdm(data):
    # [14, 4096, 13] [14, 4096] [14, 4096] [14] [14, 4096, 6]
    preds, input_labels, input_queried, input_idx, input_features = item
    for bs_id in range(preds.size(0)):
      cloud_idx = input_idx[bs_id]
      point_idx = input_queried[bs_id]
      whole['preds'][cloud_idx][point_idx] = preds[bs_id].float()
      whole['labels'][cloud_idx][point_idx] = input_labels[bs_id]
      whole['features'][cloud_idx][point_idx] = input_features[bs_id].float()

  whole['preds'] = torch.cat(whole['preds'], dim=0)
  whole['labels'] = torch.cat(whole['labels'], dim=0)
  whole['features'] = torch.cat(whole['features'], dim=0)

  # save to file
  torch.save(whole, cache_path)
  return whole


def _display_pointcloud_result(preds, labels, names=None, num_classes=13):
  """display point clouds IoU/Recall/Precision result.

  Args:
      preds ([torch.Tensor]): [N, num_classes]
      labels ([torch.Tensor]): [N, ]

  """
  if names is None:
    names = [str(i + 1) for i in range(num_classes)]
  evaluator = PointCloudSegmentEvaluator(num_classes=num_classes, names=names)
  evaluator.reset()
  conf_matrix = evaluator.compute(preds.reshape(-1, num_classes), labels.reshape(-1))
  evaluator.append(conf_matrix)
  print(evaluator.accumulate())
  print(display_confusion_matrix(evaluator.confusion_matrix, names, column_width=10))


def task_batch(args):
  """merging batch-style into non-overlap dataset
  """
  point_clouds, names, colors = sensat_urban(args.dataset, args.subset)
  for path in args.input[0]:
    print(path)
    pc_all = _gather_batch_data(path, [pc['num_points'] for pc in point_clouds], len(names))
    _display_pointcloud_result(pc_all['preds'], pc_all['labels'], list(names.values()), len(names))


def task_evaluate(args):
  point_clouds, names, colors = sensat_urban(args.dataset, args.subset)
  pc_all = torch.load(args.input[0][0], map_location='cpu')
  _display_pointcloud_result(pc_all['preds'], pc_all['labels'], list(names.values()), len(names))


def task_merge_city(args):
  """merging two dataset: birmingham + cambridge
  """
  assert len(args.input[0]) == 2, "input birmingham and cambridge path."
  birmingham, cambridge = args.input[0][0], args.input[0][1]
  print('birmingham:', birmingham)
  print('cambridge:', cambridge)

  # collect birmingham
  point_clouds, names, colors = sensat_urban(args.dataset, 'birmingham')
  pc_birmingham = _gather_batch_data(birmingham, [pc['num_points'] for pc in point_clouds], len(names))
  _display_pointcloud_result(pc_birmingham['preds'], pc_birmingham['labels'], list(names.values()), len(names))

  # collect cambridge
  point_clouds, names, colors = sensat_urban(args.dataset, 'cambridge')
  pc_cambridge = _gather_batch_data(cambridge, [pc['num_points'] for pc in point_clouds], len(names))
  _display_pointcloud_result(pc_cambridge['preds'], pc_cambridge['labels'], list(names.values()), len(names))

  # pc_birmingham['preds'][: 4] = 0 # bridge
  # pc_birmingham['preds'][: 11] = 0 # bike
  # pc_cambridge['preds'][: 4] = 0 # bike
  pc_cambridge['preds'][:, 6] = 0  # rail

  # merging
  preds = torch.cat([pc_birmingham['preds'], pc_cambridge['preds']], dim=0)
  labels = torch.cat([pc_birmingham['labels'], pc_cambridge['labels']], dim=0)
  features = torch.cat([pc_birmingham['features'], pc_cambridge['features']], dim=0)
  _display_pointcloud_result(preds, labels, list(names.values()), len(names))
  if args.output is not None:
    torch.save({'preds': preds, 'labels': labels, 'features': features, }, args.output)


def task_ensemble(args):
  """
  """
  _, names, _ = sensat_urban(args.dataset, '')

  # add preds and delete features
  pc_preds = []
  for path in args.input[0]:
    pred = torch.load(path, map_location='cpu')
    if 'features' in pred:
      del pred['features']
    pc_preds.append(pred)

  # ensemble by average
  preds = torch.stack([pred['preds'] for pred in pc_preds], dim=0).mean(dim=0)
  _display_pointcloud_result(preds, pc_preds[-1]['labels'], list(names.values()), len(names))

  # output ensemble result
  if args.output is not None:
    torch.save({'preds': preds, 'labels': pc_preds[-1]['labels']}, args.output)


def task_slim(args):
  """
  """
  if args.output is None:
    args.output = '_slim'

  if not os.path.exists(args.output):
    os.mkdir(args.output)

  for path in tqdm.tqdm(args.input[0]):
    pred = torch.load(path, map_location='cpu')
    if 'features' in pred:
      del pred['features']
    torch.save(pred, os.path.join(args.output, path.split('/')[1] + '.pth'))


if __name__ == "__main__":
  # select
  parser = argparse.ArgumentParser()
  args, _ = parser.parse_known_args()

  parser.add_argument('-t', '--task', type=str, default=None, choices=['batch', 'merge_city', 'ensemble', 'evaluate', 'slim'])  # nopep8
  parser.add_argument('-d', '--dataset', type=str, default='val', choices=['val', 'test'])
  parser.add_argument('-s', '--subset', type=str, default='', choices=['', 'birmingham', 'cambridge'])
  parser.add_argument('-i', '--input', type=str, default=None, action='append', nargs='*')
  parser.add_argument('-o', '--output', type=str, default=None)

  args = parser.parse_args()
  print(args)

  if args.task == 'batch':
    task_batch(args)

  elif args.task == 'evaluate':
    task_evaluate(args)

  elif args.task == 'merge_city':
    task_merge_city(args)

  elif args.task == 'ensemble':
    task_ensemble(args)

  elif args.task == 'slim':
    task_slim(args)
