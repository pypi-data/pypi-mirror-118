#!/bin/bash

TASK=$1

if [[ $TASK = "viz" ]]; then

python retinanet.py \
  --name RetinaNet.ResNet50 \
  --model-backbone resnet50 \
  --task viz \
  --device cpu \
  --input-colorspace RGB \
  --model-source mmdet \
  --model-path _checkpoints/detection/retinanet/retinanet_r50_fpn_1x_coco_20200130-c2398f9e.pth \
  --viz-input ../../assets/coco/mmdet.png \
  --viz-output _demo/

elif [[ $TASK = "train" ]]; then

# SSD-MobileNet-V2, 4xGPU, lr:1e-1, wd:5e-4, epoch:[50, 70, 90]
python retinanet.py \
  --name RetinaNet.MobileNetv2 \
  --model-backbone mobilenet_v2 \
  --multiprocess \
  --task train \
  --device cuda:0 \
  --model-source torchvision \
  --input-colorspace RGB \
  --train-lr 0.1 \
  --train-batchsize 32 \
  --input-height 320 \
  --input-width 320 \
  --train-epoch 80 \
  --train-optimizer sgd \
  --model-path _checkpoints/classification/imagenet/mobilenet_v2-b0353104.pth

elif [[ $TASK = "val" ]]; then

python retinanet.py \
  --name RetinaNet.VGG16 \
  --model-backbone vgg16 \
  --task val \
  --device cuda:0 \
  --model-source vanilla \
  --input-colorspace RGB \
  --model-path _checkpoints/detection/ssd/ssd300_coco_vgg16.pth \
  --model-source vanilla

fi