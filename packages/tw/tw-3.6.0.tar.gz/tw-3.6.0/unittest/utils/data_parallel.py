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
""" DataParallel

Pros:
  - automatically separate data into n cards

Cons:

"""
import os
import argparse
import random
import shutil
import socket
import time

import cv2
import numpy as np

from multiprocessing import Process

import torch
from torch import nn

import tw


class DataGenerator(torch.utils.data.Dataset):
  def __init__(self, func='cos', phase=tw.phase.train):
    super(DataGenerator, self).__init__()
    if phase == tw.phase.train:
      xs = np.arange(0, 8000)
    else:
      xs = np.arange(8000, 10000)

    if func == 'cos':
      ys = 100 * np.cos(xs)
    else:
      ys = None

    self.targets = []
    for x, y in zip(xs, ys):
      self.targets.append((x, y))

  def __len__(self):
    return len(self.targets)

  def __getitem__(self, idx):
    return self.targets[idx]


class SimpleNet(nn.Module):
  def __init__(self):
    super(SimpleNet, self).__init__()
    self.map = nn.Sequential(
        nn.Linear(1, 16),
        # nn.BatchNorm1d(16),
        nn.ReLU(),
        nn.Linear(16, 32),
        # nn.BatchNorm1d(32),
        nn.ReLU(),
        nn.Linear(32, 64),
        # nn.BatchNorm1d(64),
        nn.ReLU(),
        nn.Linear(64, 1))

  def forward(self, x):
    print(x, x.shape, x.device)
    return self.map(x)


def data_parallel_test():
  # disable random
  torch.manual_seed(42)
  np.random.seed(42)
  device = 'cuda:0'

  # build network
  model = SimpleNet().to(device)
  model = torch.nn.SyncBatchNorm.convert_sync_batchnorm(model)
  model = nn.DataParallel(model, device_ids=[0, 1, 2, 3])

  # build optimizer
  optim = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=0.0)
  loss_fn = torch.nn.MSELoss()

  # build loader
  train_loader = torch.utils.data.DataLoader(
      dataset=DataGenerator(func='cos', phase=tw.phase.train),
      batch_size=32,
      shuffle=False,
      num_workers=4,
      collate_fn=None,
      pin_memory=False,
      drop_last=True)
  val_loader = torch.utils.data.DataLoader(
      dataset=DataGenerator(func='cos', phase=tw.phase.val),
      batch_size=1,
      shuffle=False,
      num_workers=1,
      collate_fn=None,
      pin_memory=False,
      drop_last=False)

  # train
  while(1):
    for step, data in enumerate(train_loader):
      xs, ys = data
      xs = xs.unsqueeze(dim=1).float().to(device)
      ys = ys.unsqueeze(dim=1).float().to(device)
      print(xs.shape, ys.shape, xs.device)

      output = model(xs)

      loss = loss_fn(output, ys)
      optim.zero_grad()
      loss.backward()
      optim.step()

if __name__ == "__main__":
  torch.backends.cudnn.deterministic = True
  torch.backends.cudnn.benchmark = False
  data_parallel_test()
#   num_gpus = torch.cuda.device_count()
#   if num_gpus <= 0:
#     raise EnvironmentError("Failed to find CUDA devices.")
#   addr = 'localhost'
#   port = str(random.choice(range(12300, 12400)))
#   tw.logger.init('unittest.distributed.log', './')
#   mp.spawn(dist_test, nprocs=num_gpus, args=(addr, port), join=True)
