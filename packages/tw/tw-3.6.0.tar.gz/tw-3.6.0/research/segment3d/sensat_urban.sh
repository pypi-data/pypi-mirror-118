#!/bin/bash

TASK=$1
# cambridge or birmingham

if [[ "$TASK" = "train" ]]; then
# train cambridge/birmingham only with randlanet_plus
# python sensat_urban.py \
#   --name SensatUrban.RandLANetPlus.16384.Swish.cambridge.dilatedx3 \
#   --device cuda:0 \
#   --task train \
#   --dataset sensat_urban \
#   --dataset-original _datasets/SensatUrban_Dataset/sensaturban/original_block_ply \
#   --dataset-grid _datasets/SensatUrban_Dataset/sensaturban/grid_0.200 \
#   --subset cambridge \
#   --num-points 16384 \
#   --multiprocess \
#   --train-batchsize 8 \
#   --train-steps 500 \
#   --train-epoch 300 \
#   --lr 0.0005 \
#   --lr-schedule step \
#   --val-batchsize 14 \
#   --val-steps 800 \
#   --log-val 5 \
#   --log-save 5 \
#   --knn-num 16 \
#   --model randlanet_plus

# train all with randlanet
python sensat_urban.py \
  --name SensatUrban.RandLANetStack2.16384 \
  --device cuda:0 \
  --task train \
  --dataset sensat_urban \
  --dataset-original _datasets/SensatUrban_Dataset/sensaturban/original_block_ply \
  --dataset-grid _datasets/SensatUrban_Dataset/sensaturban/grid_0.200 \
  --num-points 16384 \
  --train-batchsize 16 \
  --train-steps 500 \
  --train-epoch 300 \
  --lr 0.001 \
  --lr-schedule step \
  --val-batchsize 14 \
  --val-steps 400 \
  --log-val 5 \
  --log-save 5 \
  --knn-num 16 \
  --model randlanet_stack2

elif [[ "$TASK" = "val" ]]; then

MODEL_PATH=_archive/SensatUrban.RandLANet.16384/model.epoch-200.step-100000.pth
NAME=`echo $MODEL_PATH | cut -d"/" -f 2`
EPOCH=`echo $MODEL_PATH | cut -d"/" -f 3 | cut -d"." -f 2`
NAME=$NAME.$EPOCH

python sensat_urban.py \
  --name $NAME.VAL \
  --device cuda:3 \
  --task val \
  --dump \
  --dataset sensat_urban \
  --dataset-original _datasets/SensatUrban_Dataset/sensaturban/original_block_ply \
  --dataset-grid _datasets/SensatUrban_Dataset/sensaturban/grid_0.200 \
  --num-points 16384 \
  --val-batchsize 14 \
  --val-steps 400 \
  --log-val -1 \
  --log-save 1 \
  --knn-num 16 \
  --model randlanet \
  --model-source tw \
  --model-path $MODEL_PATH

elif [[ "$TASK" = "test" ]]; then

MODEL_PATH=_archive/SensatUrban.RandLANet.16384/model.epoch-200.step-100000.pth
NAME=`echo $MODEL_PATH | cut -d"/" -f 2`
EPOCH=`echo $MODEL_PATH | cut -d"/" -f 3 | cut -d"." -f 2`
NAME=$NAME.$EPOCH

python sensat_urban.py \
  --name $NAME.TEST \
  --device cuda:3 \
  --task test \
  --dump \
  --dataset sensat_urban \
  --dataset-original _datasets/SensatUrban_Dataset/sensaturban/original_block_ply \
  --dataset-grid _datasets/SensatUrban_Dataset/sensaturban/grid_0.200 \
  --num-points 8192 \
  --val-batchsize 14 \
  --val-steps 800 \
  --log-val -1 \
  --log-save 1 \
  --knn-num 16 \
  --model randlanet \
  --model-source tw \
  --model-path $MODEL_PATH

# test all with randlanet
# python sensat_urban.py \
#   --name $NAME.Test \
#   --device cuda:3 \
#   --task test \
#   --dump \
#   --dataset sensat_urban \
#   --dataset-original _datasets/SensatUrban_Dataset/sensaturban/original_block_ply \
#   --dataset-grid _datasets/SensatUrban_Dataset/sensaturban/grid_0.200 \
#   --num-points 8192 \
#   --val-batchsize 14 \
#   --val-steps 800 \
#   --log-val -1 \
#   --log-save 1 \
#   --knn-num 16 \
#   --model randlanet \
#   --model-source vanilla \
#   --model-path $MODEL_PATH

fi
