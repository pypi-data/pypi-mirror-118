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
// =============================================================================
#ifndef _TW_DNN_OPS_CA_H_
#define _TW_DNN_OPS_CA_H_

#include <torch/extension.h>

at::Tensor ca_forward_cuda(const at::Tensor& t, const at::Tensor& f);

std::tuple<at::Tensor, at::Tensor> ca_backward_cuda(const at::Tensor& dw,
                                                    const at::Tensor& t,
                                                    const at::Tensor& f);

at::Tensor ca_map_forward_cuda(const at::Tensor& weight, const at::Tensor& g);

std::tuple<at::Tensor, at::Tensor> ca_map_backward_cuda(
  const at::Tensor& dout, const at::Tensor& weight, const at::Tensor& g);

// Interface for Python
at::Tensor ca_forward(const at::Tensor& t, const at::Tensor& f) {
  if (t.type().is_cuda()) {
#ifdef TW_WITH_CUDA
    return ca_forward_cuda(t, f);
#else
    AT_ERROR("Not compiled with GPU support");
#endif
  }
  AT_ERROR("Not implemented on the CPU");
}

std::tuple<at::Tensor, at::Tensor> ca_backward(const at::Tensor& dw,
                                               const at::Tensor& t,
                                               const at::Tensor& f) {
  if (dw.type().is_cuda()) {
#ifdef TW_WITH_CUDA
    return ca_backward_cuda(dw, t, f);
#else
    AT_ERROR("Not compiled with GPU support");
#endif
  }
  AT_ERROR("Not implemented on the CPU");
}

at::Tensor ca_map_forward(const at::Tensor& weight, const at::Tensor& g) {
  if (weight.type().is_cuda()) {
#ifdef TW_WITH_CUDA
    return ca_map_forward_cuda(weight, g);
#else
    AT_ERROR("Not compiled with GPU support");
#endif
  }
  AT_ERROR("Not implemented on the CPU");
}

std::tuple<at::Tensor, at::Tensor> ca_map_backward(const at::Tensor& dout,
                                                   const at::Tensor& weight,
                                                   const at::Tensor& g) {
  if (dout.type().is_cuda()) {
#ifdef TW_WITH_CUDA
    return ca_map_backward_cuda(dout, weight, g);
#else
    AT_ERROR("Not compiled with GPU support");
#endif
  }
  AT_ERROR("Not implemented on the CPU");
}

#endif