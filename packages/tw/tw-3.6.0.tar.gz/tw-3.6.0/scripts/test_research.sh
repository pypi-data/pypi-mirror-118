#!/bin/bash

# test all reserach bash scripts
echo "Start to test all research bash scripts."

# super resolution
pushd research/super_resolution
# ./vsr_blind.sh viz
# ./vsr_frame_recurrent.sh viz
# ./vsr_gan.sh viz
# ./vsr_likee.sh viz
popd

# video quality assessment
pushd research/quality_assess
# ./vqa_likee.sh viz
popd

# green screen matting
pushd research/matting
# ./gsm.sh viz_img
popd

# detector
pushd research/detection
# ./face_detector_demo.sh bbox
# ./face_detector_demo.sh landmark
popd

