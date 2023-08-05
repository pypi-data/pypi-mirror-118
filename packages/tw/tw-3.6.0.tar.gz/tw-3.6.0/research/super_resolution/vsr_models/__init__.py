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
"""Vsr related models
"""

# encoder
from .fenet import FENetWithMoco, FENetEncoder

# generator
from .fenet import FENet, FENetWithBranch, FENetWithWarp
from .spsrnet import SPSRNet
from .msrresnet import MSRResNet
from .rrdbnet import RRDBNet
from .dasr import DASR

# discriminator
from .vgg_discriminator import VGGStyleDiscriminator
from .nlayer_discriminator import NLayerDiscriminator
