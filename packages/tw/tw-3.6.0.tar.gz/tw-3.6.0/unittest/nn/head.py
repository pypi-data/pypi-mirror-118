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


class HeadTest(unittest.TestCase):

  def test_fpn_yolof_dilated_encoder(self):
    FPN = tw.nn.FpnYOLOFDilatedEncoder(
      in_channels=2048,
      out_channels=512,
      block_mid_channels=128,
      num_residual_blocks=4,
      block_dilations=[2, 4, 6, 8])
    FPN.eval()
    
    HEAD = tw.nn.RoIBoxHeadYOLOF(
      num_classes=81,
      in_channels=512,
      num_anchors=4,
      num_cls_convs=2,
      num_reg_convs=4)
    
    tw.flops.register(HEAD)
    with torch.no_grad():
      out = FPN.forward(torch.rand(1, 2048, 32, 32))
      out_cls, out_reg = HEAD.forward(out)
      print(out_cls.shape, out_reg.shape)
    print(tw.flops.accumulate(HEAD))
    

if __name__ == "__main__":
  unittest.main()
