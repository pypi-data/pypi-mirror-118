#!/bin/bash


DATASET_TRAIN=_datasets/BigoliveGameSRNew/mtd_train.refine.txt
DATASET=`echo $DATASET_TRAIN | cut -d"/" -f3 | cut -d"." -f2`

TASK=$1
ENCODER=FENetWithMoco
GENERATOR=FENetWithWarp.B422.C32
DISCRIMINATOR=VGGStyleDiscriminator
TYPE=blind_vsr
DEVICE=cuda:2
MODEL_PATH=_checkpoints/bigolive_game_vsr/blind_vsr-FENetWithMoco-FENetWithWarp.B422.C32-YUV-778.pth
COLORSPACE=YUV
NAME=$TYPE-$ENCODER-$GENERATOR-$COLORSPACE-$TASK-$DATASET

echo "[GAN::TASK]          ${TASK}"
echo "[GAN::GENERATOR]     ${GENERATOR}"
echo "[GAN::DISCRIMINATOR] ${DISCRIMINATOR}"
echo "[GAN::NAME]          ${NAME}"
echo "[GAN::MODEL_PATH]    ${MODEL_PATH}"
echo "[GAN::DEVICE]        ${DEVICE}"

if [[ "$TASK" = "train" ]]; then

python vsr_main.py \
    --name $NAME \
    --device $DEVICE \
    --task train \
    --train-lr 0.0001 \
    --train-batchsize 4 \
    --dataset-train $DATASET_TRAIN \
    --dataset-val _datasets/BigoliveGameSR/OneDrive/val.protocal.mtd.mini.txt \
    --dataset-test _datasets/BigoliveGameSRNewTest/combine \
    --model-type $TYPE \
    --model-generator $GENERATOR \
    --model-discriminator $DISCRIMINATOR \
    --model-encoder $ENCODER \
    --model-path $MODEL_PATH \
    --model-source vanilla \
    --input-colorspace $COLORSPACE \
    --train-epoch 2000 \
    --train-optimizer adam

elif [[ "$TASK" = "val" ]]; then

  python vsr_main.py \
    --name $NAME \
    --device $DEVICE \
    --task val \
    --model-type $TYPE \
    --model-generator $GENERATOR \
    --model-discriminator $DISCRIMINATOR \
    --model-path $MODEL_PATH \
    --input-colorspace $COLORSPACE \
    --model-source tw \
    --dataset-val _datasets/BigoliveGameSR/OneDrive/val.protocal.mtd.mini.txt

elif [[ "$TASK" = "test" ]]; then

  python vsr_main.py \
    --name $NAME \
    --device $DEVICE \
    --task test \
    --model-type $TYPE \
    --model-generator $GENERATOR \
    --model-discriminator $DISCRIMINATOR \
    --model-path $MODEL_PATH \
    --input-colorspace $COLORSPACE \
    --model-source tw \
    --dataset-test _datasets/BigoliveGameSRNewTest/combine

elif [[ "$TASK" = "onnx" ]]; then

  python vsr_main.py \
    --name $NAME \
    --device $DEVICE \
    --task onnx \
    --model-type $TYPE \
    --model-generator $GENERATOR \
    --model-discriminator $DISCRIMINATOR \
    --model-path $MODEL_PATH \
    --input-colorspace $COLORSPACE \
    --model-source tw

elif [[ "$TASK" = "trt" ]]; then

  python vsr_main.py \
    --name $NAME \
    --device $DEVICE \
    --task trt \
    --model-type $TYPE \
    --model-generator $GENERATOR \
    --model-discriminator $DISCRIMINATOR \
    --model-path $MODEL_PATH \
    --input-colorspace $COLORSPACE \
    --model-source tw

elif [[ "$TASK" = "viz" ]]; then

  python vsr_main.py \
    --viz-input ../../assets/game \
    --viz-output _demo/vsr_blind \
    --name $NAME \
    --device $DEVICE\
    --task viz \
    --model-path $MODEL_PATH \
    --input-colorspace $COLORSPACE \
    --model-generator $GENERATOR \
    --model-discriminator $DISCRIMINATOR \
    --model-encoder $ENCODER \
    --model-source tw \
    --model-type $TYPE

else
  echo "[FATAL] Unknown task <${TARGET}>"
fi
