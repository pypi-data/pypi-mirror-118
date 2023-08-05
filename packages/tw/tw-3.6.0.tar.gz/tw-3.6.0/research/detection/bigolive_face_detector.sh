#!/bin/bash

TASK=$1
COLORSPACE=Y
BACKBONE=mobilenet

if [[ $TASK = "viz" ]]; then

python bigolive_face_detector.py \
  --name bigolive_face_detector.$BACKBONE.$COLORSPACE \
  --model-backbone $BACKBONE \
  --task viz \
  --device cpu \
  --input-colorspace $COLORSPACE \
  --nms-thresh 0.4 \
  --pre-conf-thresh 0.5 \
  --post-conf-thresh 0.9 \
  --model-source vanilla \
  --model-path _checkpoints/detection/bigolive_face_detector/bigolive_face_detector.mobilenet.Y.G17.giou.bbox.epoch-250.pth \
  --viz-input ../../assets/live/ \
  --viz-output _demo/retinaface.mobilenet.final

elif [[ $TASK = "train" ]]; then

# using 4card to training
python bigolive_face_detector.py \
  --name bigolive_face_detector.$BACKBONE.$COLORSPACE.G17.giou.bbox \
  --model-backbone $BACKBONE \
  --multiprocess \
  --task train \
  --device cuda:0 \
  --model-source retinaface \
  --input-colorspace $COLORSPACE \
  --train-lr 0.004 \
  --train-batchsize 32 \
  --train-epoch 250 \
  --train-optimizer sgd \
  --model-path _checkpoints/retinaface/retinaface_mobilenet0.25.pth

elif [[ $TASK = "test" ]]; then

python bigolive_face_detector.py \
  --name bigolive_face_detector.$BACKBONE.$COLORSPACE \
  --model-backbone $BACKBONE \
  --task test \
  --device cuda:0 \
  --model-source vanilla \
  --input-colorspace $COLORSPACE \
  --model-path _outputs/retinaface.mobilenet.RGB.bbox.pts.210616200809/model.epoch-250.step-100500.pth
  # --model-path _outputs/retinaface.mobilenet.RGB.210615203753/model.epoch-250.step-100500.pth

elif [[ $TASK = "onnx" ]]; then

python bigolive_face_detector.py \
  --name bigolive_face_detector.$BACKBONE.$COLORSPACE \
  --model-backbone $BACKBONE \
  --input-colorspace $COLORSPACE \
  --task onnx \
  --device cuda:0 \
  --model-source vanilla \
  --model-path _checkpoints/detection/bigolive_face_detector/bigolive_face_detector.mobilenet.Y.G17.giou.bbox.epoch-250.pth

elif [[ $TASK = "tensorrt" ]]; then

python bigolive_face_detector.py \
  --name bigolive_face_detector.$BACKBONE.$COLORSPACE \
  --model-backbone $BACKBONE \
  --input-colorspace $COLORSPACE \
  --task trt

fi
