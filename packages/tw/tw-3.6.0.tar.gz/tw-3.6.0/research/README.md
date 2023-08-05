
# Research

## Base Context

```python
import argparse

import torch
from torch import nn

import tw
from tw.transform import functional as F


class GreenScreenMatting():

  def __init__(self, config):
    """init
    """

  def _transform_train(self, metas):
    """transform_train
    """

  def _transform_val(self, metas):
    """transform_val
    """

  def _dump(self):
    """dump
    """

  def _load(self):
    """load
    """

  def _build_dataset(self, phase: tw.phase):
    """build_dataset
    """

  def _build_optim(self, model: nn.Module):
    """build_optim
    """

  def _build_model(self):
    """build_model
    """

  def _train(self, **kwargs):
    """train
    """

  def _val(self, **kwargs):
    """val
    """

  def _viz(self, **kwargs):
    """viz
    """

  def _onnx(self, **kwargs):
    """onnx
    """

  def _tensorrt(self, **kwargs):
    """tensorrt
    """

  def __call__(self):
    """call
    """


if __name__ == "__main__":

  parser = argparse.ArgumentParser()

  # ---------------------------------------------
  #  USED BY COMMON
  # ---------------------------------------------
  parser.add_argument('--task', type=str, default=None, choices=['train', 'val', 'viz', 'onnx', 'tensorrt'])
  parser.add_argument('--dataset', type=str, default=None, choices=['LikeeSR'])

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
  parser.add_argument('--model-name', type=str, required=True)
  parser.add_argument('--model-path', type=str, default=None, help="loadding pretrain/last-checkpoint model.")
  parser.add_argument('--model-source', type=str, default=None)

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

  tw.runner.launch(parser, GreenScreenMatting)


```