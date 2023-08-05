#!/bin/bash

#------------------------------------------------------------------------
# MNIST
#------------------------------------------------------------------------

# python classifier2d.py \
#   --task train \
#   --name Classifier2d.Mnist.LeNet \
#   --device cuda:0 \
#   --output_dir _outputs \
#   --multiprocess \
#   --log-val 1 \
#   --log-save 1 \
#   --model-name lenet \
#   --num_classes 10 \
#   --train-lr 0.01 \
#   --train-batchsize 128 \
#   --val-batchsize 128 \
#   --train-epoch 100 \
#   --dataset Mnist

#------------------------------------------------------------------------
# CIFAR-10
#------------------------------------------------------------------------

# python classifier2d.py \
#   --task train \
#   --name Classifier2d.Cifar10.LeNet \
#   --device cuda:0 \
#   --output_dir _outputs \
#   --log-val 1 \
#   --log-save 1 \
#   --model-name lenet \
#   --num_classes 10 \
#   --train-lr 0.01 \
#   --train-batchsize 128 \
#   --val-batchsize 128 \
#   --train-epoch 100 \
#   --dataset Cifar10

#------------------------------------------------------------------------
# IMAGENET
#------------------------------------------------------------------------

for model in efficientnet_b3
do
  python classifier2d.py \
    --task val \
    --name Classifier2d.ImageNet.$model \
    --device cuda:1 \
    --output_dir _outputs \
    --model-name $model \
    --val-batchsize 32 \
    --num_classes 1000 \
    --dataset ImageNet
done


