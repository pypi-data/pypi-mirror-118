
#include "nms/nms.h"
#include "roi_align/roi_align.h"
#include "roi_pool/roi_pool.h"
#include "sigmoid_focal_loss/sigmoid_focal_loss.h"
#include "dcn/deform_conv.h"
#include "dcn/deform_pool.h"
#include "psa/psa.h"
#include "ca/ca.h"


PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
  m.def("nms", &nms, "non-maximum suppression");
  m.def("ml_nms", &ml_nms, "multilabel non-maximum suppression");
  m.def("roi_align_forward", &ROIAlign_forward, "ROIAlign_forward");
  m.def("roi_align_backward", &ROIAlign_backward, "ROIAlign_backward");
  m.def("roi_pool_forward", &ROIPool_forward, "ROIPool_forward");
  m.def("roi_pool_backward", &ROIPool_backward, "ROIPool_backward");
  m.def("sigmoid_focalloss_forward", &SigmoidFocalLoss_forward, "SigmoidFocalLoss_forward");
  m.def("sigmoid_focalloss_backward", &SigmoidFocalLoss_backward, "SigmoidFocalLoss_backward");
  // dcn-v2
  m.def("deform_conv_forward", &deform_conv_forward, "deform_conv_forward");
  m.def("deform_conv_backward_input", &deform_conv_backward_input, "deform_conv_backward_input");
  m.def("deform_conv_backward_parameters", &deform_conv_backward_parameters, "deform_conv_backward_parameters");
  m.def("modulated_deform_conv_forward", &modulated_deform_conv_forward, "modulated_deform_conv_forward");
  m.def("modulated_deform_conv_backward", &modulated_deform_conv_backward, "modulated_deform_conv_backward");
  m.def("deform_psroi_pooling_forward", &deform_psroi_pooling_forward, "deform_psroi_pooling_forward");
  m.def("deform_psroi_pooling_backward", &deform_psroi_pooling_backward, "deform_psroi_pooling_backward");
  // ca
  m.def("ca_forward", &ca_forward, "ca_forward");
  m.def("ca_backward", &ca_backward, "ca_backward");
  m.def("ca_map_forward", &ca_map_forward, "ca_map_forward");
  m.def("ca_map_backward", &ca_map_backward, "ca_map_backward");
  // psa
  m.def("psa_forward", &psa_forward, "psa_forward");
  m.def("psa_backward", &psa_backward, "psa_backward");
}