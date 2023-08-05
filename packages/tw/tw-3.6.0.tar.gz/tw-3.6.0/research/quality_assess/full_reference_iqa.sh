#!/bin/bash

TASK=$1
DATASET=CSIQ
MODEL=ssim

source ./common.sh

if [[ "$TASK" = "test" ]]; then

python full_reference_iqa.py \
    --name FRIQA.$MODEL.$DATASET \
    --device cuda:0 \
    --task test \
    --dataset $DATASET \
    --dataset-test $DATSET_TEST \
    --repeat 1 \
    --model $MODEL \
    --input-colorspace RGB

elif [[ "$TASK" = "val" ]]; then

python full_reference_iqa.py \
    --name FRIQA.$MODEL.$DATASET \
    --device cuda:0 \
    --task val \
    --dataset $DATASET \
    --repeat 25 \
    --dataset-val $DATASET_VAL \
    --model $MODEL \
    --input-colorspace RGB

fi