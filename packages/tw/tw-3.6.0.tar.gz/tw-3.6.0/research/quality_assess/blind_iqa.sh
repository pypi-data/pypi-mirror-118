#!/bin/bash

TASK=$1
DATASET=FLIVE
MODEL=patchiqa.mobilenet_v2.feedback
source ./common.sh

if [[ "$TASK" = "train" ]]; then

python blind_iqa.py \
    --name NRIQA.$MODEL.$DATASET \
    --device cuda:3 \
    --task train \
    --dataset $DATASET \
    --dataset-train $DATASET_TRAIN \
    --dataset-val $DATASET_VAL \
    --dataset-test $DATASET_TEST \
    --train-batchsize 16 \
    --train-repeat 1 \
    --val-repeat 1 \
    --log-val 1 \
    --log-save 1 \
    --input-height $INPUT_HEIGHT \
    --input-width $INPUT_WIDTH \
    --train-epoch 60 \
    --model $MODEL \
    --input-colorspace RGB

elif [[ "$TASK" = "test" ]]; then

python blind_iqa.py \
    --name NRIQA.$MODEL.$DATASET \
    --device cuda:0 \
    --task test \
    --dataset $DATASET \
    --dataset-test $DATASET_TEST \
    --model $MODEL \
    --test-repeat 1 \
    --input-colorspace RGB \
    --model-source vanilla \
    --model-path _outputs/NRIQA.patchiqa.mobilenet_v2.roi.FLIVE.210721171905/model.epoch-12.step-22680.pth

elif [[ "$TASK" = "val" ]]; then

python blind_iqa.py \
    --name NRIQA.$MODEL.$DATASET \
    --device cuda:3 \
    --task val \
    --dataset $DATASET \
    --dataset-val $DATASET_VAL \
    --val-repeat 1 \
    --model $MODEL \
    --model-source vanilla \
    --model-path _outputs/NRIQA.patchiqa.mobilenet_v2.feedback.FLIVE.210722154343/model.epoch-1.step-1890.pth
    --input-colorspace RGB

elif [[ "$TASK" = "viz" ]]; then

python blind_iqa.py \
    --name NRIQA.$MODEL.$DATASET.VIZ \
    --device cuda:1 \
    --task viz \
    --model patchiqa.mobilenet_v2.roi \
    --model-source vanilla \
    --model-path _outputs/NRIQA.patchiqa.mobilenet_v2.roi.FLIVE.210721171905/model.epoch-13.step-24570.pth \
    --input-colorspace RGB \
    --viz-input /data/jk/test2 \
    --viz-output _demo/assets

fi