#!/bin/bash

# single input green screen matting (SGSM)

TASK=$1
echo "[GSM::TASK] ${TASK}"

if [[ "$TASK" = "train" ]]; then

  python bgm.py \
    --name GSM.MobileNetv2.PhotoMatte85.Slim \
    --device cuda:3 \
    --task train \
    --multiprocess \
    --model-sgsm \
    --model-name mattingrefine \
    --model-path _checkpoints/green_screen_matting/pytorch_mobilenetv2.old.pth \
    --model-source bgm \
    --model-backbone mobilenetv2 \
    --train-batchsize 2 \
    --train-epoch 1000 \
    --dataset photomatte13k

elif [[ "$TASK" = "viz_img" ]]; then

  python bgm.py \
    --name GSM.PhotoMatte85 \
    --device cpu \
    --task viz \
    --model-sgsm \
    --model-name mattingrefine \
    --model-path _outputs/GSM.MobileNetv2.PhotoMatte85.Slim.210609195030/dp-gpu070.p0/model.epoch-187.step-84898.pth \
    --model-source tw \
    --model-backbone mobilenetv2 \
    --viz-input ../../assets/green_screen/ \
    --viz-output _demo/sgsm_8-8-4-4-4 \
    --viz-type image

  # --viz-target-bgr ../../assets/green_screen/bg_gauze.png \

elif [[ "$TASK" = "viz_vid" ]]; then

  python bgm.py \
    --name GSM.PhotoMatte85 \
    --device cuda:3 \
    --task viz \
    --model-sgsm \
    --model-name mattingrefine \
    --model-path _outputs/GSM.MobileNetv2.PhotoMatte85.Slim.210609195030/dp-gpu070.p0/model.epoch-187.step-84898.pth \
    --model-source tw \
    --model-backbone mobilenetv2 \
    --viz-input _datasets/matting/IMG_1270.mp4 \
    --viz-output _demo/new187_bg/ \
    --viz-type video

  # --viz-target-bgr /data/jk/backgrounds/虚拟背景效果图_part1/纱帘海边/纱帘背景.png \


elif [[ "$TASK" = "onnx" ]]; then

python bgm.py \
  --name GSM.Onnx \
  --task onnx \
  --model-sgsm \
  --model-name mattingrefine \
  --model-path _outputs/GSM.MobileNetv2.PhotoMatte85.Slim.210609195030/dp-gpu070.p0/model.epoch-187.step-84898.pth \
  --model-source tw \
  --model-backbone mobilenetv2

fi
