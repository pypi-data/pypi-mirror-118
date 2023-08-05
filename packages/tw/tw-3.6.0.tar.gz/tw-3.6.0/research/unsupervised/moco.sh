#!/bin/bash

TASK=$1
ENCODER=simple
NAME=MOCOv2-$ENCODER
MODEL_PATH=_outputs/Moco-simple.210512211342/model.epoch-67.step-1857240.pth

echo "[MOCO::TASK]    ${TASK}"
echo "[MOCO::ENCODER] ${ENCODER}"
echo "[MOCO::NAME]    ${NAME}"
echo "[MOCO::PATH]    ${MODEL_PATH}"

if [[ "$TASK" = "train" ]]; then

  python moco.py \
    --name $NAME \
    --device cuda:0 \
    --task train \
    --train-lr 0.0001 \
    --train-batchsize 32 \
    --dataset-train _datasets/BigoliveGameSR/PAPER.protocal.lr.txt \
    --dataset-val _datasets/BigoliveGameSR/PAPER.protocal.hr.txt \
    --model-encoder $ENCODER \
    --train-epoch 1000 \
    --train-optimizer adam

elif [[ "$TASK" = "viz" ]]; then

  python moco.py \
    --viz-input _datasets/BigoliveGameSRNewTest/LOL_clip2 \
    --viz-output _demo/$NAME-LOL.CLIP2 \
    --name $NAME \
    --device cuda:1 \
    --task viz \
    --model-path $MODEL_PATH \
    --model-source tw \
    --model-type $TYPE \
    --model-encoder $ENCODER

  python moco.py \
    --viz-input _datasets/BigoliveGameSRNewTest/SVID_20210427_105627_1/mtd_SVID_20210427_105627_1_0_640x312.mp4.fold \
    --viz-output _demo/$NAME-SVID_20210427_105627_1 \
    --name $NAME \
    --device cuda:1 \
    --task viz \
    --model-path $MODEL_PATH \
    --model-source tw \
    --model-type $TYPE \
    --model-encoder $ENCODER

  python moco.py \
    --viz-input _datasets/BigoliveGameSRNewTest/SVID_20210427_110917_1/mtd_SVID_20210427_110917_1_0_640x312.mp4.fold \
    --viz-output _demo/$NAME-SVID_20210427_110917_1 \
    --name $NAME \
    --device cuda:1 \
    --task viz \
    --model-path $MODEL_PATH \
    --model-source tw \
    --model-type $TYPE \
    --model-encoder $ENCODER

  python moco.py \
    --viz-input _datasets/BigoliveGameSRNewTest/Screen_Recording_Part2/SVID_20210506_151543_1/demo_SVID_20210506_151543_1_0__312.0x640.0.mp4.fold \
    --viz-output _demo/$NAME-SVID_20210506_151543_1 \
    --name $NAME \
    --device cuda:1 \
    --task viz \
    --model-path $MODEL_PATH \
    --model-source tw \
    --model-type $TYPE \
    --model-encoder $ENCODER

  python moco.py \
    --viz-input _datasets/BigoliveGameSRNewTest/Screen_Recording_Part2/SVID_20210506_154544_1/demo_SVID_20210506_154544_1_0__640.0x312.0.mp4.fold \
    --viz-output _demo/$NAME-SVID_20210506_154544_1 \
    --name $NAME \
    --device cuda:1 \
    --task viz \
    --model-path $MODEL_PATH \
    --model-source tw \
    --model-type $TYPE \
    --model-encoder $ENCODER

  python moco.py \
    --viz-input _datasets/BigoliveGameSRNewTest/Screen_Recording_Part2/SVID_20210506_155555_1/demo_SVID_20210506_155555_1_0__640.0x312.0.mp4.fold \
    --viz-output _demo/$NAME-SVID_20210506_155555_1 \
    --name $NAME \
    --device cuda:1 \
    --task viz \
    --model-path $MODEL_PATH \
    --model-source tw \
    --model-type $TYPE \
    --model-encoder $ENCODER
    
else
  echo "[FATAL] Unknown task <${TARGET}>"

fi