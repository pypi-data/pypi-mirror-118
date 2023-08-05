#!/bin/bash

TASK=$1 # bbox or landmark
DETECTOR=retinaface
LANDMARK=MobileNet_GDConv_56

if [[ "$TASK" = "bbox" ]]; then

  python face_detector_demo.py \
    --device cuda:0 \
    --model-detection $DETECTOR \
    --bbox \
    --input-colorspace RGB \
    --viz-input ../../assets/face \
    --viz-output _demo/$DETECTOR

elif [[ "$TASK" = "landmark" ]]; then

  python face_detector_demo.py \
    --device cuda:1 \
    --model-detection $DETECTOR \
    --bbox \
    --model-landmark $LANDMARK \
    --landmark \
    --refine-bbox \
    --input-colorspace RGB \
    --viz-input ../../assets/face \
    --viz-output _demo/$DETECTOR_$LANDMARK

fi
