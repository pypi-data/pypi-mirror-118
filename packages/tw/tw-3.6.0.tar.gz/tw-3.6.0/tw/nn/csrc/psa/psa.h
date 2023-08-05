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
#ifndef _TW_DNN_OPS_PSA_H_
#define _TW_DNN_OPS_PSA_H_

#include <torch/extension.h>

at::Tensor psa_forward_cpu(const torch::Tensor& hc, const int forward_type);

at::Tensor psa_backward_cpu(const at::Tensor& dout,
                            const at::Tensor& hc,
                            const int forward_type);
at::Tensor psa_forward_cuda(const at::Tensor& hc, const int forward_type);

at::Tensor psa_backward_cuda(const at::Tensor& dout,
                             const at::Tensor& hc,
                             const int forward_type);

at::Tensor psa_forward(const at::Tensor& hc, const int forward_type) {
  if (hc.type().is_cuda()) {
#ifdef TW_WITH_CUDA
    return psa_forward_cuda(hc, forward_type);
#else
    AT_ERROR("Not compiled with GPU support");
#endif
  }
  return psa_forward_cpu(hc, forward_type);
}

at::Tensor psa_backward(const at::Tensor& dout,
                        const at::Tensor& hc,
                        const int forward_type) {
  if (hc.type().is_cuda()) {
#ifdef TW_WITH_CUDA
    return psa_backward_cuda(dout, hc, forward_type);
#else
    AT_ERROR("Not compiled with GPU support");
#endif
  }
  return psa_backward_cpu(dout, hc, forward_type);
}

#endif