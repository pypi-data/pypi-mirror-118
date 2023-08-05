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
import time
import torch

import tw
from tw.nn import fpn


class FpnTest(unittest.TestCase):

  def test_fpn_yolof_dilated_encoder(self):
    model = fpn.FpnYOLOFDilatedEncoder(
        in_channels=2048,
        out_channels=512,
        block_mid_channels=128,
        num_residual_blocks=4,
        block_dilations=[2, 4, 6, 8])
    model.eval()

    tw.flops.register(model)
    with torch.no_grad():
      out = model.forward(torch.rand(1, 2048, 32, 32))
      print(out.shape)
    print(tw.flops.accumulate(model))


if __name__ == "__main__":
  unittest.main()
