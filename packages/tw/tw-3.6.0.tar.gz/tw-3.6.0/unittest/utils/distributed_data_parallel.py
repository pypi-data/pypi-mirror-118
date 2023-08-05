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
from torch import distributed as dist
from torch import multiprocessing as mp
from torch.utils.collect_env import get_pretty_env_info

import tw


class DataGenerator(torch.utils.data.Dataset):
  def __init__(self, func='cos', phase=tw.phase.train):
    super(DataGenerator, self).__init__()
    if phase == tw.phase.train:
      xs = np.arange(0, 8000) / 10000.0
    else:
      xs = np.arange(8000, 10000) / 10000.0

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
    return self.map(x)


def dist_test(rank, addr, port):
  # distributed step
  os.environ['MASTER_ADDR'] = addr
  os.environ['MASTER_PORT'] = port
  dist.init_process_group("nccl", rank=rank, world_size=torch.cuda.device_count())

  # get dist size and local size
  dist_world_size = torch.distributed.get_world_size()
  dist_rank = torch.distributed.get_rank()
  device = f'cuda:{dist_rank}'
  print('world_size:%d, rank:%d' % (dist_world_size, dist_rank))

  # disable random
  torch.manual_seed(42 + dist_rank)
  np.random.seed(42 + dist_rank)

  # build network
  model = SimpleNet().to(device)
  model = torch.nn.SyncBatchNorm.convert_sync_batchnorm(model)
  model = torch.nn.parallel.DistributedDataParallel(model, device_ids=[dist_rank])
  from torch.nn import parallel

  # build optimizer
  optim = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=0.0)
  loss_fn = torch.nn.MSELoss()

  # build loader
  train_loader = torch.utils.data.DataLoader(
      dataset=DataGenerator(func='cos', phase=tw.phase.train),
      batch_size=8,
      shuffle=True,
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
  for step, data in enumerate(train_loader):
    xs, ys = data
    xs = xs.unsqueeze(dim=1).float().to(device)
    ys = ys.unsqueeze(dim=1).float().to(device)

    output = model(xs)

    loss = loss_fn(output, ys)
    optim.zero_grad()
    loss.backward()
    optim.step()

    if step % 10 == 0:

      v1 = model.state_dict()['module.map.0.weight']
      tw.logger.train(f'rank:{dist_rank}, iter:{step}, map.0.weight:{v1.sum()}')

      # synchronized point
      dist.barrier()

      if dist_rank == 0:
        torch.nn.init.normal_(model.module.map[0].weight)
        v1 = model.state_dict()['module.map.0.weight']
        tw.logger.train(f'in rank:{dist_rank}, iter:{step}, map.0.weight:{v1.sum()}')
        tw.logger.train('')

      for k in model.parameters():
        dist.broadcast(k, src=0)

      v1 = model.state_dict()['module.map.0.weight']
      tw.logger.train(f'broad rank:{dist_rank}, iter:{step}, map.0.weight:{v1.sum()}')


if __name__ == "__main__":
  torch.backends.cudnn.deterministic = True
  torch.backends.cudnn.benchmark = False
  num_gpus = torch.cuda.device_count()
  if num_gpus <= 0:
    raise EnvironmentError("Failed to find CUDA devices.")
  addr = 'localhost'
  port = str(random.choice(range(12300, 12400)))
  tw.logger.init('unittest.distributed.log', './')
  mp.spawn(dist_test, nprocs=num_gpus, args=(addr, port), join=True)
