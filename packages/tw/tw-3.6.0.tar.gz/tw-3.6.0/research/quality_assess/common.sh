#!/bin/bash

set -e

INPUT_HEIGHT=224
INPUT_WIDTH=224

if [[ "$DATASET" = "PIPAL" ]];then
DATASET_TRAIN=_datasets/quality_assess/PIPAL
DATASET_VAL=_datasets/quality_assess/PIPAL
DATASET_TEST=_datasets/quality_assess/PIPAL
elif [[ "$DATASET" = "TID2013" ]];then
DATASET_TRAIN=_datasets/quality_assess/TID2013/mos_with_names.txt
DATASET_VAL=_datasets/quality_assess/TID2013/mos_with_names.txt
DATASET_TEST=_datasets/quality_assess/TID2013/mos_with_names.txt
elif [[ "$DATASET" = "KonIQ10k" ]]; then
DATASET_TRAIN=_datasets/quality_assess/koniq10k/koniq10k_scores_and_distributions.csv
DATASET_VAL=_datasets/quality_assess/koniq10k/koniq10k_scores_and_distributions.csv
DATASET_TEST=_datasets/quality_assess/koniq10k/koniq10k_scores_and_distributions.csv
INPUT_HEIGHT=384
INPUT_WIDTH=512
elif [[ "$DATASET" = "LIVE2005" ]]; then
DATASET_TRAIN=_datasets/quality_assess/LIVE2005
DATASET_VAL=_datasets/quality_assess/LIVE2005
DATASET_TEST=_datasets/quality_assess/LIVE2005
elif [[ "$DATASET" = "LIVEC" ]]; then
DATASET_TRAIN=_datasets/quality_assess/LIVEC
DATASET_VAL=_datasets/quality_assess/LIVEC
DATASET_TEST=_datasets/quality_assess/LIVEC
elif [[ "$DATASET" = "LIVEMD" ]]; then
DATASET_TRAIN=_datasets/quality_assess/LIVEMD
DATASET_VAL=_datasets/quality_assess/LIVEMD
DATASET_TEST=_datasets/quality_assess/LIVEMD
elif [[ "$DATASET" = "CSIQ" ]]; then
DATASET_TRAIN=_datasets/quality_assess/CSIQ/csiq.txt
DATASET_VAL=_datasets/quality_assess/CSIQ/csiq.txt
DATASET_TEST=_datasets/quality_assess/CSIQ/csiq.txt
elif [[ "$DATASET" = "FLIVE" ]]; then
DATASET_TRAIN=_datasets/quality_assess/FLIVE/all_patches.csv
DATASET_VAL=_datasets/quality_assess/FLIVE/all_patches.csv
DATASET_TEST=_datasets/quality_assess/FLIVE/all_patches.csv
INPUT_HEIGHT=640
INPUT_WIDTH=640
fi