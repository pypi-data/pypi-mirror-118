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
r"""VNIMA models
"""

import torch
import torch.nn as nn


class NIMA(nn.Module):
  """Neural IMage Assessment model by Google."""

  def __init__(self, base_model, fc_in, num_classes=10):
    super(NIMA, self).__init__()
    self.features = base_model  # for vgg16 and mobilenet v2
    self.classifier = nn.Sequential(
        nn.Dropout(p=0.75),
        nn.Linear(in_features=fc_in, out_features=num_classes),  # for mobilenetv2
        nn.Softmax())

  def forward(self, x):
    out = self.features(x)
    out = out.view(out.size(0), -1)
    out = self.classifier(out)
    return out


class VNIMA(nn.Module):
  """Video image assessment model based on NIMA."""

  def __init__(self, base_model, fc_in, num_classes=5):
    super(VNIMA, self).__init__()
    self.features = TimeDistributed(base_model.features)

    self.classifier = nn.Sequential(
        nn.Dropout(0.2),
        nn.Linear(in_features=fc_in, out_features=num_classes),
        nn.Softmax(dim=1)
    )

  def forward(self, x):
    out = self.features(x)  # mv2: [batch_size, frames, 1280, 1, 1] ; resnet18: [batch_size, frames, 512, 1, 1]
    out = torch.sum(out, 1)*1.0/out.shape[1]
    out = out.view(out.size(0), -1)
    out = self.classifier(out)
    return out


class TimeDistributed(nn.Module):
  def __init__(self, module):
    super(TimeDistributed, self).__init__()
    self.base_model = module

  def forward(self, x):
    assert x.ndim == 5, "The dimension of the input tensor must be 5."

    batch_size, frames, channels, height, weight = x.size()
    x_reshaped = x.contiguous().view(-1, channels, height, weight)
    y = self.base_model(x_reshaped)
    y = nn.functional.adaptive_avg_pool2d(y, 1)

    # We have to reshape Y
    # (samples, timesteps, output_size)
    y = y.contiguous().view(batch_size, frames, y.size(1), y.size(2), y.size(3))
    return y


# def single_emd_loss(p, q, r=2):
#     """Earth Mover's Distance of one sample.

#     Args:
#         p: true distribution of shape num_classes × 1.
#         q: estimated distribution of shape num_classes × 1.
#         r: norm parameter.
#     """
#     assert p.shape == q.shape, "Length of the two distribution must be the same."
#     length = p.shape[0]
#     emd_loss = 0.0
#     for i in range(1, length + 1):
#         emd_loss += torch.abs(sum(p[:i] - q[:i])) ** r
#     return (emd_loss / length) ** (1. / r)


# def emd_loss(p, q, r=2):
#     """Earth Mover's Distance on a batch.

#     Args:
#         p: true distribution of shape mini_batch_size × num_classes × 1.
#         q: estimated distribution of shape mini_batch_size × num_classes × 1.
#         r: norm parameters.
#     """
#     assert p.shape == q.shape, "Shape of the two distribution batches must be the same."
#     mini_batch_size = p.shape[0]
#     loss_vector = []
#     for i in range(mini_batch_size):
#         loss_vector.append(single_emd_loss(p[i], q[i], r=r))
#     return sum(loss_vector) / mini_batch_size

# def emd_cross_loss(pred, label):
#     """(EMD + cross entropy) / 2 loss on a batch.

#     Args:
#         pred: predictions of shape mini_batch_size × num_classes.
#         label: labels of shape mini_batch_size × num_classes x 1.

#     Returns:
#         Mean loss of a batch.
#     """
#     num_classes = pred.shape[1]
#     CEloss = nn.CrossEntropyLoss()(pred, label.argmax(1).view(-1,))
#     pred = pred.view(-1, num_classes, 1)
#     EMDloss = emd_loss(label, pred)
#     loss = (CEloss + EMDloss) / 2
#     return loss
