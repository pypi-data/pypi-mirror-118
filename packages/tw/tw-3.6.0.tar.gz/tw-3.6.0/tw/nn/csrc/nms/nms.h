// Copyright 2018 The KaiJIN Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// ==============================================================================
#ifndef _TW_DNN_OPS_NMS_H_
#define _TW_DNN_OPS_NMS_H_

#include <torch/extension.h>

// cpu
at::Tensor nms_cpu(const at::Tensor& dets, const float threshold);

// cuda
at::Tensor nms_cuda(const at::Tensor bbox, const float threshold);

// nms
at::Tensor nms(const at::Tensor& dets, const float threshold) {
  if (dets.type().is_cuda()) {
#ifdef TW_WITH_CUDA
    if (dets.numel() == 0)
      return at::empty({0}, dets.options().dtype(at::kLong).device(at::kCPU));
    return nms_cuda(dets, threshold);
#else
    AT_ERROR("Not compiled with GPU support");
#endif
  }
  at::Tensor result = nms_cpu(dets, threshold);
  return result;
}

at::Tensor ml_nms_cuda(const at::Tensor boxes, float threshold);

at::Tensor ml_nms(const at::Tensor& dets,
                  const at::Tensor& scores,
                  const at::Tensor& labels,
                  const float threshold) {
  if (dets.type().is_cuda()) {
#ifdef TW_WITH_CUDA
    // TODO raise error if not compiled with CUDA
    if (dets.numel() == 0)
      return at::empty({0}, dets.options().dtype(at::kLong).device(at::kCPU));
    auto b = at::cat({dets, scores.unsqueeze(1), labels.unsqueeze(1)}, 1);
    return ml_nms_cuda(b, threshold);
#else
    AT_ERROR("Not compiled with GPU support");
#endif
  }
  AT_ERROR("CPU version not implemented");
}

#endif
