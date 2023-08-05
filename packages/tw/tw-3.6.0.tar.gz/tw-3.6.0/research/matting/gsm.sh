#!/bin/bash

TASK=$1
MODEL_PATH=_checkpoints/green_screen_matting/pytorch_mobilenetv2.old.pth

echo "[GSM::TASK] ${TASK}"

if [[ "$TASK" = "gt" ]]; then

#!< 不要动，这个是用GSM模型生成groundtruth的指令
python bgm.py \
  --name GSM \
  --device cuda:3 \
  --task viz \
  --model-gsm \
  --model-name mattingrefine \
  --model-path _checkpoints/GreenScreenMatting/gsm_resnet50_59999.old.pth \
  --model-source bgm \
  --model-backbone resnet50 \
  --viz-input _datasets/bigo_80k_videos \
  --viz-output _datasets/bigo_80k_videos_gsm_resnet50\
  --viz-type image

elif [[ "$TASK" = "train" ]]; then

#!< 采用GSM训练
python bgm.py \
  --name GSM.MobileNetv2.PhotoMatte85.Slim \
  --device cuda:0 \
  --task train \
  --multiprocess \
  --model-gsm \
  --model-name mattingrefine \
  --model-path _checkpoints/green_screen_matting/pytorch_mobilenetv2.old.pth \
  --model-source bgm \
  --model-backbone mobilenetv2 \
  --train-batchsize 2 \
  --train-epoch 1000 \
  --dataset photomatte13k

elif [[ "$TASK" = "viz_img" ]]; then

#!< 采用GSM推理图像并结合背景
python bgm.py \
  --name GSM.PhotoMatte85 \
  --device cpu \
  --task viz \
  --model-gsm \
  --model-name mattingrefine \
  --model-path $MODEL_PATH \
  --model-source tw \
  --model-backbone mobilenetv2 \
  --viz-input ../../assets/green_screen/ \
  --viz-target-bgr ../../assets/green_screen/bg_gauze.png \
  --viz-output _demo/gsm_8-8-4-4-4 \
  --viz-type image

elif [[ "$TASK" = "viz_vid" ]]; then

#!< 采用GSM推理视频并结合背景
python bgm.py \
  --name GSM.PhotoMatte85 \
  --device cuda:3 \
  --task viz \
  --model-gsm \
  --model-name mattingrefine \
  --model-path $MODEL_PATH \
  --model-source tw \
  --model-backbone mobilenetv2 \
  --viz-input _datasets/matting/bigo/testset/IMG_1270.mp4 \
  --viz-target-bgr /data/jk/backgrounds/虚拟背景效果图_part1/纱帘海边/纱帘背景.png \
  --viz-output _demo/new173_bg/ \
  --viz-type video

elif [[ "$TASK" = "onnx" ]]; then

python bgm.py \
  --name GSM.Onnx \
  --task onnx \
  --model-gsm \
  --model-name mattingrefine \
  --model-path $MODEL_PATH \
  --model-source bgm \
  --model-backbone mobilenetv2

elif [[ "$TASK" = "trt" ]]; then

python bgm.py \
  --name GSM.TensorRT \
  --task trt \
  --model-gsm \
  --model-name mattingrefine \
  --model-path $MODEL_PATH \
  --model-source tw \
  --model-backbone mobilenetv2

fi
