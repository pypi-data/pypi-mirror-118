#!/bin/bash

TASK=$1
ENCODER=VNIMA.MobileNet
MODEL_PATH=_checkpoints/likee_vqa/vqa_yuv_epoch-32.pth
DEVICE=cuda:0
COLORSPACE=YUV
NAME=$ENCODER-$COLORSPACE-$TASK

echo "[LikeeVsr::TASK]          ${TASK}"
echo "[LikeeVsr::DEVICE]        ${DEVICE}"
echo "[LikeeVsr::ENCODER]       ${ENCODER}"
echo "[LikeeVsr::NAME]          ${NAME}"
echo "[LikeeVsr::MODEL_PATH]    ${MODEL_PATH}"
echo "[LikeeVsr::COLORSPACE]    ${COLORSPACE}"

if [[ "$TASK" = "train" ]]; then

python likee_vqa.py \
    --name $NAME \
    --device $DEVICE \
    --task train \
    --train-lr 0.0001 \
    --train-batchsize 4 \
    --dataset-train _datasets/BigoliveGameSRNew/mtd_train.txt \
    --dataset-val _datasets/BigoliveGameSR/OneDrive/val.protocal.mtd.mini.txt \
    --dataset-test _datasets/BigoliveGameSRNewTest/combine \
    --model-encoder $ENCODER \
    --model-source tw \
    --input-colorspace $COLORSPACE \
    --input-interval 3 \
    --input-length 30 \
    --train-epoch 1000 \
    --train-optimizer adam

elif [[ "$TASK" = "val" ]]; then

  python likee_vqa.py \
    --input-colorspace $COLORSPACE \
    --input-interval 3 \
    --input-length 30 \
    --val-batchsize 4 \
    --name $NAME \
    --device $DEVICE \
    --model-path $MODEL_PATH \
    --model-encoder $ENCODER \
    --model-discriminator $DISCRIMINATOR \
    --model-encoder $ENCODER \
    --model-source thea-v1 \
    --task val \
    --model-source thea-v1 \
    --dataset-val /data4/jk/tw/_datasets/VNIMA/val.txt

elif [[ "$TASK" = "test" ]]; then

  python likee_vqa.py \
    --name $NAME \
    --device $DEVICE \
    --task test \
    --model-encoder $ENCODER \
    --model-path $MODEL_PATH \
    --model-source tw \
    --dataset-test _datasets/BigoliveGameSRNewTest/combine

elif [[ "$TASK" = "onnx" ]]; then

  python likee_vqa.py \
    --name $NAME \
    --device $DEVICE \
    --task onnx \
    --model-encoder $ENCODER \
    --model-source tw

elif [[ "$TASK" = "trt" ]]; then

  python likee_vqa.py \
    --name $NAME \
    --device $DEVICE \
    --task trt \
    --model-encoder $ENCODER \
    --model-path $MODEL_PATH \
    --model-source tw

elif [[ "$TASK" = "viz" ]]; then

  python likee_vqa.py \
    --viz-input ../../assets/mp4 \
    --viz-output _demo/assets \
    --input-colorspace $COLORSPACE \
    --input-interval 3 \
    --input-length 30 \
    --name $NAME \
    --device $DEVICE \
    --task viz \
    --model-path $MODEL_PATH \
    --model-encoder $ENCODER \
    --model-discriminator $DISCRIMINATOR \
    --model-encoder $ENCODER \
    --model-source thea-v1 \
    --model-type $TYPE

else
  echo "[FATAL] Unknown task <${TARGET}>"
fi
