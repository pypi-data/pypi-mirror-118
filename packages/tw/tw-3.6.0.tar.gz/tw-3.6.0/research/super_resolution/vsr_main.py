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
"""Vsr collections"""
import warnings  # nopep8
warnings.filterwarnings("ignore")  # nopep8

import argparse
import tw

from vsr_bigolive_game import BigoliveGameVsr
from vsr_blind import BlindVsr
from vsr_likee import LikeeVsr
from vsr_gan import GanVsr
from vsr_frame_recurrent import FrVsr

if __name__ == "__main__":

  parser = argparse.ArgumentParser()

  model_types = {
      'bigolive_game_vsr': BigoliveGameVsr,
      'blind_vsr': BlindVsr,
      'likee_vsr': LikeeVsr,
      'gan_vsr': GanVsr,
      'frvsr': FrVsr,
  }

  # ---------------------------------------------
  #  USED BY COMMON
  # ---------------------------------------------
  parser.add_argument('--task', type=str, default=None, choices=['train', 'val', 'test', 'viz', 'onnx', 'trt'])
  parser.add_argument('--dataset-train', type=str, default='_datasets/BigoliveGameSR/PAPER.protocal.txt')
  parser.add_argument('--dataset-val', type=str, default='_datasets/BigoliveGameSR/PAPER.protocal.txt')
  parser.add_argument('--dataset-test', type=str, default='_datasets/BigoliveGameSRNewTest/combine')

  # ---------------------------------------------
  #  USED BY LOGGER
  # ---------------------------------------------
  parser.add_argument('--log', type=int, default=10, help="display interval step.")
  parser.add_argument('--log-val', type=int, default=1, help="running validation in terms of step.")
  parser.add_argument('--log-test', type=int, default=1, help="running test in terms of step.")
  parser.add_argument('--log-save', type=int, default=1, help="saveing checkpoint with interval.")

  # ---------------------------------------------
  #  USED BY MODEL-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--model-type', type=str, choices=model_types.keys())
  parser.add_argument('--model-encoder', type=str, default=None)
  parser.add_argument('--model-generator', type=str, default=None)
  parser.add_argument('--model-discriminator', type=str, default=None)
  parser.add_argument('--model-path', type=str, default=None, help="loadding pretrain/last-checkpoint model.")
  parser.add_argument('--model-source', type=str, default=None)
  parser.add_argument('--input-colorspace', type=str, default='Y', choices=['Y', 'RGB', 'YUV'])

  # ---------------------------------------------
  #  USED BY TRAIN-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--train-lr', type=float, default=0.0001, help="total learning rate across devices.")
  parser.add_argument('--train-batchsize', type=int, default=4, help="total batch size across devices.")
  parser.add_argument('--train-epoch', type=int, default=240, help="total training epochs.")
  parser.add_argument('--train-optimizer', type=str, default='sgd', choices=['sgd', 'adam'], help="training optimizer.")

  # ---------------------------------------------
  #  USED BY VAL-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--val-batchsize', type=int, default=1, help="total batch size across devices.")

  # ---------------------------------------------
  #  USED BY VIZ-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--viz-input', type=str, help='input path could be a folder/filepath.')
  parser.add_argument('--viz-output', type=str, help='output path should be a folder path.')

  # generate config
  args, _ = parser.parse_known_args()

  tw.runner.launch(parser, model_types[args.model_type])
