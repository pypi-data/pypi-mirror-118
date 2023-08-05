#!/bin/bash

#!<---------------------------------------------------------------
#!< BGM
#!<---------------------------------------------------------------

# python bgm.py \
#   --name BGM \
#   --device cuda:0 \
#   --task viz \
#   --model-name mattingrefine \
#   --model-path _checkpoints/GreenScreenMatting/pytorch_mobilenetv2.old.pth \
#   --model-backbone mobilenetv2 \
#   --viz-input _datasets/matting/bigo/testset/IMG_1270/00000920.png \
#   --viz-bgr _datasets/matting/bigo/testset/IMG_1270/00000000.png \
#   --viz-output _outputs/IMG_1270/pytorch_mobilenetv2/

# python bgm.py \
#   --name BGM \
#   --device cuda:0 \
#   --task val \
#   --model-name mattingrefine \
#   --model-path _checkpoints/GreenScreenMatting/pytorch_mobilenetv2.old.pth \
#   --model-backbone mobilenetv2 \
#   --dataset photomatte13k

#!<---------------------------------------------------------------
#!< GSM
#!<---------------------------------------------------------------

# visualize gsm for image
# python bgm.py \
#   --name BGM \
#   --device cuda:0 \
#   --task viz \
#   --model-gsm \
#   --model-name mattingrefine \
#   --model-path _checkpoints/GreenScreenMatting/gsm_resnet50_59999.old.pth \
#   --model-backbone resnet50 \
#   --viz-input _datasets/matting/bigo/testset/IMG_1270/00000920.png \
#   --viz-output _outputs/IMG_1270/gsm_resnet50_59999/

# python bgm.py \
#   --name BGM \
#   --device cuda:0 \
#   --task viz \
#   --model-gsm \
#   --model-name mattingrefine \
#   --model-path _outputs/GSM.MobileNet.PhotoMatte85.210414201307/bigo.p0/model.epoch-2.step-912.pth \
#   --model-source tw \
#   --model-backbone mobilenetv2 \
#   --viz-input _datasets/matting/bigo/testset/IMG_1270/00000920.png \
#   --viz-output _outputs/IMG_1270/GSM.mobilenetv2.PhotoMatte85.2/

#-------

#!< 不要动，这个是用GSM模型生成groundtruth的指令
# visualize gsm for video
python bgm.py \
  --name BGM \
  --device cuda:3 \
  --task viz \
  --model-gsm \
  --model-name mattingrefine \
  --model-path _checkpoints/GreenScreenMatting/gsm_resnet50_59999.old.pth \
  --model-backbone resnet50 \
  --viz-input _datasets/matting/bigo/bigo_80k_videos \
  --viz-output _datasets/matting/bigo/gsm_resnet50_bigo_80k_videos \
  --viz-type image

# export to onnx
# python bgm.py \
#   --name BGM \
#   --device cuda:0 \
#   --task onnx \
#   --model-gsm \
#   --model-name mattingrefine \
#   --model-path _checkpoints/GreenScreenMatting/gsm_resnet50_59999.old.pth \
#   --model-backbone resnet50

# validation
# python bgm.py \
#   --name BGM \
#   --device cuda:0 \
#   --task val \
#   --model-gsm \
#   --model-name mattingrefine \
#   --model-path _checkpoints/GreenScreenMatting/gsm_resnet50_59999.old.pth \
#   --model-backbone resnet50 \
#   --dataset photomatte13k

# train - resnet50
# python bgm.py \
#   --name GSM.ResNet50.PhotoMatte85 \
#   --device cuda:0 \
#   --task train \
#   --multiprocess \
#   --model-gsm \
#   --model-name mattingrefine \
#   --model-path _checkpoints/GreenScreenMatting/pytorch_resnet50.old.pth \
#   --model-backbone resnet50 \
#   --train-batchsize 2 \
#   --dataset photomatte13k

# python bgm.py \
#   --name GSM.MobileNet.PhotoMatte85 \
#   --device cuda:0 \
#   --task train \
#   --multiprocess \
#   --model-gsm \
#   --model-name mattingrefine \
#   --model-path _checkpoints/GreenScreenMatting/pytorch_mobilenetv2.old.pth \
#   --model-backbone mobilenetv2 \
#   --train-batchsize 2 \
#   --dataset photomatte13k