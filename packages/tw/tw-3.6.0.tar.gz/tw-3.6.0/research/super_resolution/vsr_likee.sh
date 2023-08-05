#!/bin/bash

TASK=$1
GENERATOR=FENet.B422.C32
TYPE=likee_vsr
MODEL_PATH=_checkpoints/bigolive_game_vsr/likee_vsr-FENet.B422.C32.pth
DEVICE=cuda:3
COLORSPACE=YUV
NAME=$TYPE-$GENERATOR-$COLORSPACE-$TASK

echo "[LikeeVsr::TASK]          ${TASK}"
echo "[LikeeVsr::DEVICE]        ${DEVICE}"
echo "[LikeeVsr::GENERATOR]     ${GENERATOR}"
echo "[LikeeVsr::NAME]          ${NAME}"
echo "[LikeeVsr::MODEL_PATH]    ${MODEL_PATH}"
echo "[LikeeVsr::COLORSPACE]    ${COLORSPACE}"

if [[ "$TASK" = "train" ]]; then

python vsr_main.py \
    --name $NAME \
    --device $DEVICE \
    --task train \
    --train-lr 0.0001 \
    --train-batchsize 4 \
    --dataset-train _datasets/BigoliveGameSRNew/mtd_train.txt \
    --dataset-val _datasets/BigoliveGameSR/OneDrive/val.protocal.mtd.mini.txt \
    --dataset-test _datasets/BigoliveGameSRNewTest/combine \
    --model-type $TYPE \
    --model-generator $GENERATOR \
    --model-source tw \
    --input-colorspace $COLORSPACE \
    --train-epoch 1000 \
    --train-optimizer adam

elif [[ "$TASK" = "val" ]]; then

  python vsr_main.py \
    --name $NAME \
    --device $DEVICE \
    --task val \
    --model-type $TYPE \
    --model-generator $GENERATOR \
    --model-path $MODEL_PATH \
    --model-source tw \
    --dataset-val _datasets/BigoliveGameSR/OneDrive/val.protocal.mtd.mini.txt

elif [[ "$TASK" = "test" ]]; then

  python vsr_main.py \
    --name $NAME \
    --device $DEVICE \
    --task test \
    --model-type $TYPE \
    --model-generator $GENERATOR \
    --model-path $MODEL_PATH \
    --model-source tw \
    --dataset-test _datasets/BigoliveGameSRNewTest/combine

elif [[ "$TASK" = "onnx" ]]; then

  python vsr_main.py \
    --name $NAME \
    --device $DEVICE \
    --task onnx \
    --model-type $TYPE \
    --model-generator $GENERATOR \
    --model-source tw

elif [[ "$TASK" = "trt" ]]; then

  python vsr_main.py \
    --name $NAME \
    --device $DEVICE \
    --task trt \
    --model-type $TYPE \
    --model-generator $GENERATOR \
    --model-path $MODEL_PATH \
    --model-source tw

elif [[ "$TASK" = "viz" ]]; then

  python vsr_main.py \
    --viz-input ../../assets/game \
    --viz-output _demo/vsr_likee \
    --name $NAME \
    --device $DEVICE\
    --task viz \
    --model-path $MODEL_PATH \
    --model-generator $GENERATOR \
    --model-source tw \
    --model-type $TYPE

else
  echo "[FATAL] Unknown task <${TARGET}>"
fi
