#!/bin/bash

TASK=$1

if [[ $TASK = "viz" ]]; then

python ssd.py \
  --name SSD.vgg16 \
  --model-backbone vgg16 \
  --task viz \
  --device cuda:2 \
  --input-colorspace RGB \
  --model-source vanilla \
  --model-path _checkpoints/detection/ssd/ssd300_coco_vgg16.pth \
  --viz-input ../../assets/coco/mmdet.png \
  --viz-output _demo/

elif [[ $TASK = "train" ]]; then

# SSD-MobileNet-V2, 4xGPU, lr:1e-1, wd:5e-4, epoch:[50, 70, 90]
python ssd.py \
  --name SSD.MobileNetv2 \
  --model-backbone mobilenet_v2 \
  --multiprocess \
  --task train \
  --device cuda:0 \
  --model-source tw \
  --input-colorspace RGB \
  --train-lr 0.1 \
  --train-batchsize 32 \
  --input-height 320 \
  --input-width 320 \
  --train-epoch 80 \
  --train-optimizer sgd \
  --model-path _outputs/SSD.MobileNetv2.210630180434/dp-gpu070.p0/model.epoch-35.step-128240.pth

elif [[ $TASK = "val" ]]; then

python ssd.py \
  --name SSD.VGG16 \
  --model-backbone vgg16 \
  --task val \
  --device cuda:0 \
  --model-source vanilla \
  --input-colorspace RGB \
  --model-path _checkpoints/detection/ssd/ssd300_coco_vgg16.pth \
  --model-source vanilla

fi