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
// Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved.
#ifndef _TW_DNN_OPS_DEFORM_POOL_H_
#define _TW_DNN_OPS_DEFORM_POOL_H_

#include <torch/extension.h>

void deform_psroi_pooling_cuda_forward(at::Tensor input,
                                       at::Tensor bbox,
                                       at::Tensor trans,
                                       at::Tensor out,
                                       at::Tensor top_count,
                                       const int no_trans,
                                       const float spatial_scale,
                                       const int output_dim,
                                       const int group_size,
                                       const int pooled_size,
                                       const int part_size,
                                       const int sample_per_part,
                                       const float trans_std);

void deform_psroi_pooling_cuda_backward(at::Tensor out_grad,
                                        at::Tensor input,
                                        at::Tensor bbox,
                                        at::Tensor trans,
                                        at::Tensor top_count,
                                        at::Tensor input_grad,
                                        at::Tensor trans_grad,
                                        const int no_trans,
                                        const float spatial_scale,
                                        const int output_dim,
                                        const int group_size,
                                        const int pooled_size,
                                        const int part_size,
                                        const int sample_per_part,
                                        const float trans_std);

// Interface for Python
void deform_psroi_pooling_forward(at::Tensor input,
                                  at::Tensor bbox,
                                  at::Tensor trans,
                                  at::Tensor out,
                                  at::Tensor top_count,
                                  const int no_trans,
                                  const float spatial_scale,
                                  const int output_dim,
                                  const int group_size,
                                  const int pooled_size,
                                  const int part_size,
                                  const int sample_per_part,
                                  const float trans_std) {
  if (input.type().is_cuda()) {
#ifdef TW_WITH_CUDA
    return deform_psroi_pooling_cuda_forward(input,
                                             bbox,
                                             trans,
                                             out,
                                             top_count,
                                             no_trans,
                                             spatial_scale,
                                             output_dim,
                                             group_size,
                                             pooled_size,
                                             part_size,
                                             sample_per_part,
                                             trans_std);
#else
    AT_ERROR("Not compiled with GPU support");
#endif
  }
  AT_ERROR("Not implemented on the CPU");
}

void deform_psroi_pooling_backward(at::Tensor out_grad,
                                   at::Tensor input,
                                   at::Tensor bbox,
                                   at::Tensor trans,
                                   at::Tensor top_count,
                                   at::Tensor input_grad,
                                   at::Tensor trans_grad,
                                   const int no_trans,
                                   const float spatial_scale,
                                   const int output_dim,
                                   const int group_size,
                                   const int pooled_size,
                                   const int part_size,
                                   const int sample_per_part,
                                   const float trans_std) {
  if (input.type().is_cuda()) {
#ifdef TW_WITH_CUDA
    return deform_psroi_pooling_cuda_backward(out_grad,
                                              input,
                                              bbox,
                                              trans,
                                              top_count,
                                              input_grad,
                                              trans_grad,
                                              no_trans,
                                              spatial_scale,
                                              output_dim,
                                              group_size,
                                              pooled_size,
                                              part_size,
                                              sample_per_part,
                                              trans_std);
#else
    AT_ERROR("Not compiled with GPU support");
#endif
  }
  AT_ERROR("Not implemented on the CPU");
}

#endif