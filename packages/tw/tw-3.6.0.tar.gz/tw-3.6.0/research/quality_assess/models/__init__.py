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

from .vnima import VNIMA
from .hyper_iqa import HyperNet, TargetNet
from .base_iqa import BaseIQA
from .compose_iqa import ComposeBlindIQA, ComposeFullRefIQA
from .koncept512 import KonCept512
from .patch_iqa import PatchIQA