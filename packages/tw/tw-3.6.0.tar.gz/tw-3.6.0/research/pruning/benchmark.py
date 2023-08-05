# Copyright 2018 The KaiJIN Authors. All Rights Reserved.
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
r"""benchmark backbone performance
"""

import os
import time
import argparse
import numpy as np

import torch
import tw

MODEL_LIST = {
    'alexnet': {'model': tw.models.alexnet.alexnet, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'bcnn': {'model': tw.models.bcnn.BilinearCNN, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'efficientnet': {'model': tw.models.efficientnet.efficientnet_b0, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'densenet_121': {'model': tw.models.densenet.densenet121, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'densenet_161': {'model': tw.models.densenet.densenet161, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'densenet_169': {'model': tw.models.densenet.densenet169, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'densenet_201': {'model': tw.models.densenet.densenet201, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'drn_a_50': {'model': tw.models.drn.drn_a_50, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'drn_c_26': {'model': tw.models.drn.drn_c_26, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'drn_c_42': {'model': tw.models.drn.drn_c_42, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'drn_c_58': {'model': tw.models.drn.drn_c_58, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'drn_d_22': {'model': tw.models.drn.drn_d_22, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'drn_d_24': {'model': tw.models.drn.drn_d_24, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'drn_d_38': {'model': tw.models.drn.drn_d_38, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'drn_d_40': {'model': tw.models.drn.drn_d_40, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'drn_d_54': {'model': tw.models.drn.drn_d_54, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'drn_d_105': {'model': tw.models.drn.drn_d_105, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'mixnet_s': {'model': tw.models.mixnet.mixnet_s, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'mixnet_m': {'model': tw.models.mixnet.mixnet_m, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'mixnet_l': {'model': tw.models.mixnet.mixnet_l, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'mobilenet_v1': {'model': tw.models.mobilenet_v1.mobilenet_v1, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'mobilenet_v2': {'model': tw.models.mobilenet_v2.mobilenet_v2, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'mobilenet_v3_small': {'model': tw.models.mobilenet_v3.mobilenetv3_small, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'mobilenet_v3_large': {'model': tw.models.mobilenet_v3.mobilenetv3_large, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'resnet_tf_50': {'model': tw.models.resnet_tf.resnet50, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'resnet_tf_101': {'model': tw.models.resnet_tf.resnet101, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'resnet_tf_152': {'model': tw.models.resnet_tf.resnet152, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'resnet_18': {'model': tw.models.resnet.resnet18, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'resnet_34': {'model': tw.models.resnet.resnet34, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'resnet_50': {'model': tw.models.resnet.resnet50, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'resnet_101': {'model': tw.models.resnet.resnet101, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'resnet_152': {'model': tw.models.resnet.resnet152, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'senet154': {'model': tw.models.senet.senet154, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'se_resnet50': {'model': tw.models.senet.se_resnet50, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'se_resnet101': {'model': tw.models.senet.se_resnet101, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'se_resnet152': {'model': tw.models.senet.se_resnet152, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'se_resnext50_32x4d': {'model': tw.models.senet.se_resnext50_32x4d, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'se_resnext101_32x4d': {'model': tw.models.senet.se_resnext101_32x4d, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'shufflenet_v2_x0_5': {'model': tw.models.shufflenet_v2.shufflenet_v2_x0_5, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'shufflenet_v2_x1_0': {'model': tw.models.shufflenet_v2.shufflenet_v2_x1_0, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'shufflenet_v2_x1_5': {'model': tw.models.shufflenet_v2.shufflenet_v2_x1_5, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'shufflenet_v2_x2_0': {'model': tw.models.shufflenet_v2.shufflenet_v2_x2_0, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'squeezenet1_0': {'model': tw.models.squeezenet.squeezenet1_0, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'squeezenet1_1': {'model': tw.models.squeezenet.squeezenet1_1, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'vgg11': {'model': tw.models.vgg.vgg11, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'vgg11_bn': {'model': tw.models.vgg.vgg11_bn, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'vgg13': {'model': tw.models.vgg.vgg13, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'vgg13_bn': {'model': tw.models.vgg.vgg13_bn, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'vgg16': {'model': tw.models.vgg.vgg16, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'vgg16_bn': {'model': tw.models.vgg.vgg16_bn, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'vgg19': {'model': tw.models.vgg.vgg19, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'vgg19_bn': {'model': tw.models.vgg.vgg19_bn, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'xception_65': {'model': tw.models.xception.xception_65, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'xception_71': {'model': tw.models.xception.xception_71, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},
    'xception_a': {'model': tw.models.xception.xception_a, 'params': {}, 'input': [torch.rand([1, 3, 224, 224])]},

    # segmentation
    'bisenet': {'model': tw.models.bisenet.BiSeNet, 'params': {'num_classes': 19, 'arch': 'resnet18'}, 'input': [torch.rand([1, 3, 512, 512])]},
    'ccnet': {'model': tw.models.ccnet.CCNet, 'params': {'num_classes': 19, 'arch': 'resnet18'}, 'input': [torch.rand([1, 3, 512, 512])]},
    'cgnet': {'model': tw.models.cgnet.CGNet, 'params': {'num_classes': 19}, 'input': [torch.rand([1, 3, 512, 512])]},
    'danet': {'model': tw.models.danet.DANet, 'params': {'num_classes': 19, 'arch': 'resnet18'}, 'input': [torch.rand([1, 3, 512, 512])]},
    'dfanet': {'model': tw.models.dfanet.DFANet, 'params': {'num_classes': 19, 'arch': 'xception_a'}, 'input': [torch.rand([1, 3, 512, 512])]},
    'dunet': {'model': tw.models.dunet.DUNet, 'params': {'num_classes': 19, 'arch': 'resnet18'}, 'input': [torch.rand([1, 3, 512, 512])]},
    'encnet': {'model': tw.models.encnet.EncNet, 'params': {'num_classes': 19, 'arch': 'resnet18'}, 'input': [torch.rand([1, 3, 512, 512])]},
    'enet': {'model': tw.models.enet.ENet, 'params': {'num_classes': 19}, 'input': [torch.rand([1, 3, 512, 512])]},
    'erfnet': {'model': tw.models.erfnet.ERFNet, 'params': {'num_classes': 19}, 'input': [torch.rand([1, 3, 512, 512])]},
    'espnet': {'model': tw.models.espnet.ESPNetV2, 'params': {'num_classes': 19}, 'input': [torch.rand([1, 3, 512, 512])]},
    'fastscnn': {'model': tw.models.fastscnn.FastSCNN, 'params': {'num_classes': 19}, 'input': [torch.rand([1, 3, 512, 512])]},
    'fcn8s': {'model': tw.models.fcn.FCN8s, 'params': {'num_classes': 19, 'arch': 'vgg16'}, 'input': [torch.rand([1, 3, 512, 512])]},
    'fcn16s': {'model': tw.models.fcn.FCN16s, 'params': {'num_classes': 19, 'arch': 'vgg16'}, 'input': [torch.rand([1, 3, 512, 512])]},
    'fcn32s': {'model': tw.models.fcn.FCN32s, 'params': {'num_classes': 19, 'arch': 'vgg16'}, 'input': [torch.rand([1, 3, 512, 512])]},
    'icnet': {'model': tw.models.icnet.ICNet, 'params': {'num_classes': 19, 'arch': 'resnet18'}, 'input': [torch.rand([1, 3, 512, 512])]},
    'lednet': {'model': tw.models.lednet.LEDNet, 'params': {'num_classes': 19}, 'input': [torch.rand([1, 3, 512, 512])]},
    'ocnet': {'model': tw.models.ocnet.OCNet, 'params': {'num_classes': 19, 'arch': 'resnet18'}, 'input': [torch.rand([1, 3, 512, 512])]},
    'psanet': {'model': tw.models.psanet.PSANet, 'params': {'num_classes': 19, 'arch': 'resnet18'}, 'input': [torch.rand([1, 3, 512, 512])]},
    'pspnet': {'model': tw.models.pspnet.PSPNet, 'params': {'num_classes': 19, 'arch': 'resnet18'}, 'input': [torch.rand([1, 3, 512, 512])]},
    'unet': {'model': tw.models.unet.UNet, 'params': {'num_classes': 19, 'in_channels': 3}, 'input': [torch.rand([1, 3, 512, 512])]},

    # matting
    'bgm_mobilenet': {'model': tw.models.bgmv2.MattingRefine, 'params': {'backbone': 'mobilenetv2', 'refine_mode': 'full'}, 'input': [torch.rand([1, 3, 512, 512]), torch.rand([1, 3, 512, 512])]},
    'bgm_resnet50': {'model': tw.models.bgmv2.MattingRefine, 'params': {'backbone': 'resnet50', 'refine_mode': 'full'}, 'input': [torch.rand([1, 3, 512, 512]), torch.rand([1, 3, 512, 512])]},
}


def benchmark(config):
  # set basic env
  torch.backends.cudnn.benchmark = True
  info = MODEL_LIST[config.model_name]

  # prepare model and inputs
  device = torch.device(config.device)
  # to device
  for i, inp in enumerate(info['input']):
    info['input'][i] = inp.to(device)

  # models
  model = info['model'](**info['params']).to(device)
  model.eval()

  if config.insight:
    # display model parameters
    tw.flops.register(model)
    with torch.no_grad():
      model(*info['input'])
    print(tw.flops.accumulate(model))
    tw.flops.unregister(model)

    # register timer layer by layer
    for k, m in model.named_modules():
      m.name = k
      m.duration = 0
      m.count = 0
      m.register_forward_pre_hook(tw.flops.register_forward_pre_hook_timer)
      m.register_forward_hook(tw.flops.register_forward_hook)

  with torch.no_grad():
    ts = []
    start = time.time()
    for _ in range(config.count):
      t1 = time.time()
      model(*info['input'])
      torch.cuda.synchronize()
      t2 = time.time()
      ts.append((t2 - t1) * 1000)
    end = time.time()

  ts = np.array(ts)

  if config.insight:
    print(tw.flops.profiler(model, np.sum(ts)))

  print('==> MODEL:', config.model_name)
  print('==> PARAM:', info['params'])
  print('==> IN :', [inp.shape for inp in info['input']])
  print('==> FPS: %.4f' % (float(config.count)/(end - start)))
  print('==> MAX: %.4f' % np.max(ts))
  print('==> MIN: %.4f' % np.min(ts))
  print('==> AVG: %.4f' % np.mean(ts))
  print('==> VAR: %.4f' % np.sqrt(np.var(ts)))
  print()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()

  # ---------------------------------------------
  #  USED BY CONTEXT
  # ---------------------------------------------
  parser.add_argument('--name', type=str, default='benchmark')
  parser.add_argument('--root', type=str, default=None, help="None for new one, use specific root.")
  parser.add_argument('--output_dir', type=str, default='_outputs', help="default output folder.")
  parser.add_argument('--pid', type=str, default=tw.timer.pid(), help="task pid.")
  parser.add_argument('--device', type=str, default='cuda:0', help='running device.')

  # ---------------------------------------------
  #  USED BY BENCHMARK
  # ---------------------------------------------
  parser.add_argument('--count', type=int, default=100, help="iterations for running.")
  parser.add_argument('--insight', action='store_true', help="insight params and flops layer by layer.")
  parser.add_argument('--model-name', type=str, required=True, choices=MODEL_LIST.keys(), help="model names.")

  # generate config
  args, _ = parser.parse_known_args()

  # maybe result in deadlock
  env = os.environ.copy()
  env['OMP_NUM_THREADS'] = str(1)

  # multiprocess
  benchmark(args)
