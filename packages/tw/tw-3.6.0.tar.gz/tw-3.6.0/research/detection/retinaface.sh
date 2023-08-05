#!/bin/bash

TASK=$1
COLORSPACE=Y
BACKBONE=mobilenet

if [[ $TASK = "viz" ]]; then

python retinaface.py \
  --name retinaface.$BACKBONE.$COLORSPACE \
  --model-backbone $BACKBONE \
  --task viz \
  --device cuda:2 \
  --input-colorspace $COLORSPACE \
  --nms-thresh 0.4 \
  --conf-thresh 0.9 \
  --model-source vanilla \
  --model-path _outputs/retinaface.mobilenet.RGB.210617172228/model.epoch-250.step-100500.pth \
  --viz-input ../../assets/face/12_Group_Group_12_Group_Group_12_24.jpg \
  --viz-output _demo/retinaface.mobilenet.train4

elif [[ $TASK = "train" ]]; then

python retinaface.py \
  --name retinaface.$BACKBONE.$COLORSPACE.640 \
  --model-backbone $BACKBONE \
  --task train \
  --device cuda:2 \
  --model-source retinaface \
  --input-colorspace $COLORSPACE \
  --train-lr 0.001 \
  --train-batchsize 32 \
  --train-epoch 250 \
  --train-optimizer sgd \
  --model-path _checkpoints/retinaface/retinaface_mobilenet0.25.pth

elif [[ $TASK = "finetune" ]]; then

python retinaface.py \
  --name retinaface.$BACKBONE.$COLORSPACE \
  --model-backbone $BACKBONE \
  --task train \
  --device cuda:1 \
  --model-source vanilla \
  --input-colorspace $COLORSPACE \
  --train-lr 0.0001 \
  --train-batchsize 32 \
  --train-epoch 250 \
  --train-optimizer sgd \
  --model-path _outputs/retinaface.mobilenet.RGB.210617172228/model.epoch-250.step-100500.pth

elif [[ $TASK = "test" ]]; then

python retinaface.py \
  --name retinaface.$BACKBONE.$COLORSPACE \
  --model-backbone $BACKBONE \
  --task test \
  --device cuda:0 \
  --model-source vanilla \
  --input-colorspace $COLORSPACE \
  --model-path _checkpoints/detection/retinaface/retinaface.mobilenet.Y.640.G7.epoch-250.pth

elif [[ $TASK = "onnx" ]]; then

python retinaface.py \
  --name retinaface.$BACKBONE.$COLORSPACE \
  --model-backbone $BACKBONE \
  --input-colorspace $COLORSPACE \
  --task onnx \
  --device cuda:0 \
  --model-source retinaface \
  --model-path _checkpoints/face_detector/retinaface/mobilenet0.25_Final.pth

fi
