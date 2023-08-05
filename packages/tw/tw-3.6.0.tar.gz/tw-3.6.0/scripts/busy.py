# Copyright 2020 The KaiJIN Authors. All Rights Reserved.
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
"""Busy running"""
import os
import time
import random
import torch
import torchvision
from torch import multiprocessing as mp
from torch import distributed as dist


class BusyTasker():

  def __call__(self, device):
    model_cpu = torchvision.models.resnet18()
    model_gpu = torchvision.models.resnet152()
    model_gpu.to(device)

    count = 0
    while True:
      t1 = time.time()
      with torch.no_grad():
        inputs_cpu = torch.rand(128, 3, 224, 224).float()
        inputs_gpu = torch.rand(512, 3, 224, 224).float().to(device)
        model_gpu(inputs_gpu)
        if count % 5 == 0:
          model_cpu(inputs_cpu)
      t2 = time.time()
      torch.save(inputs_cpu, 'cpu.pth')
      torch.save(inputs_gpu, 'gpu.pth')
      # time.sleep(1.0)
      count += 1
      print('[Elapsed] {}: {}'.format(count, (t2 - t1) * 1000.0))


def dist_runner(rank, tasker, addr='localhost', port=12300):
  os.environ['MASTER_ADDR'] = addr
  os.environ['MASTER_PORT'] = port
  dist.init_process_group("nccl", rank=rank, world_size=torch.cuda.device_count())
  tasker()(device='cuda:{}'.format(rank))


if __name__ == "__main__":
  # maybe result in deadlock
  env = os.environ.copy()
  env['OMP_NUM_THREADS'] = str(1)
  # multiprocess
  num_gpus = torch.cuda.device_count()
  if num_gpus <= 0:
    raise EnvironmentError("Failed to find CUDA devices.")
  addr = 'localhost'
  port = str(random.choice(range(12300, 12400)))
  mp.spawn(dist_runner, nprocs=num_gpus, args=(BusyTasker, addr, port), join=True)
