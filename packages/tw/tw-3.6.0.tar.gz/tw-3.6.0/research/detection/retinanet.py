# Copyright 2021 The KaiJIN Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""RetinaNet
"""
from ast import parse
import functools
import os
import math
import random
import argparse
import tqdm
import cv2
import numpy as np
import torch
from torch import nn
from torch.utils import tensorboard
import tw
from tw import logger
from tw import transform as T

import detector


def transform_train(metas, h, w):
  shape = metas[0].bin.shape
  if len(shape) == 2 or shape[2] == 1:
    T.change_colorspace(metas, src=T.COLORSPACE.GRAY, dst=T.COLORSPACE.BGR)
  T.change_colorspace(metas, src=T.COLORSPACE.BGR, dst=T.COLORSPACE.RGB)

  T.random_photometric_distortion(metas)
  if random.random() > 0.5:
    T.random_expand(metas, ratio_range=(1, 4), mean=(0, 0, 0))

  T.minimum_iou_random_crop(metas, min_ious=(0.1, 0.3, 0.5, 0.7, 0.9, 1.0), min_crop_size=0.3)
  T.random_hflip(metas)
  T.resize(metas, h, w)
  T.to_tensor(metas, mean=[123.675, 116.28, 103.53])
  return metas


def transform_val(metas, h, w):
  shape = metas[0].bin.shape
  if len(shape) == 2 or shape[2] == 1:
    T.change_colorspace(metas, src=T.COLORSPACE.GRAY, dst=T.COLORSPACE.BGR)
  T.change_colorspace(metas, src=T.COLORSPACE.BGR, dst=T.COLORSPACE.RGB)
  T.resize(metas, h, w)
  T.to_tensor(metas, mean=[123.675, 116.28, 103.53])
  return metas


class RetinaNetWrapper(nn.Module):

  def __init__(self, backbone: nn.Module, neck: nn.Module, bbox_head: nn.Module):
    super(RetinaNetWrapper, self).__init__()
    self.backbone = backbone
    self.neck = neck
    self.bbox_head = bbox_head

  def forward(self, inputs):
    # inputs = torch.rand(1, 3, 512, 512)
    _, c3, c4, c5 = self.backbone(inputs)
    necks = self.neck((c3, c4, c5))
    bbox_cls, bbox_loc = self.bbox_head(necks)
    # for _cls, _loc in zip(bbox_cls, bbox_loc):
    #   print(_cls.shape, _loc.shape)
    torch.save(
        {
            'c3': c3,
            'c4': c4,
            'c5': c5,
            'inputs': inputs,
            'necks': necks,
            'bbox_cls': bbox_cls,
            'bbox_loc': bbox_loc,
        },
        'data.pth'
    )
    return bbox_cls, bbox_loc


class RetinaNetDetector():

  def __init__(self, config):
    self.Config = config

    # overwrite when dist
    if self.Config.dist_size > 1:
      self.Config.device = 'cuda:{}'.format(self.Config.dist_rank)
    self.Master = True if self.Config.dist_rank == 0 else False

    # evaluator
    self.Evaluator = None

    # evaluation and tensorboard
    self.Writer = tensorboard.SummaryWriter(log_dir=self.Config.root)

    # scalar
    self.Epoch = 0
    self.Step = 0

    #!<-------------------------------------------------------------------------
    #!< BUILD BACKBONE
    #!<-------------------------------------------------------------------------

    # different input format
    if self.Config.input_colorspace in ['Y']:
      in_channels = 1
    elif self.Config.input_colorspace in ['RGB', 'YUV']:
      in_channels = 3
    else:
      raise NotImplementedError

    # select different backbone
    if self.Config.model_backbone == 'resnet50':
      backbone = tw.models.resnet.resnet50(output_backbone=True)
      # backbone = detector.ssd.MobilenetV1()
      neck = tw.nn.FpnRetinaNet(
          in_channels=[512, 1024, 2048],
          hidden_channels=[256, 256, 256],
          out_channels=[256, 256, 256, 256, 256])
      head = tw.nn.RoIBoxHeadRetinaNet(
          num_classes=80,
          in_channels=256,
          out_channels=256,
          num_anchors=9,
          num_convs=4)
      anchor = tw.nn.RetinaNetAnchorGenerator(
          anchor_sizes=[32, 64, 128, 256, 512],
          anchor_strides=[8, 16, 32, 64, 128],
          anchor_ratios=[0.5, 1.0, 2.0],
          straddle_thresh=0.0,
          octave=4.0,
          scales_per_octave=3)

    else:
      raise NotImplementedError(self.Config.model_backbone)

    # coder
    self.Model = RetinaNetWrapper(backbone=backbone, neck=neck, bbox_head=head)
    self.Model.to(self.Config.device)
    self.Anchor = anchor
    self.Anchor.to(self.Config.device)
    self.BoxCoder = tw.nn.GeneralBoxCoder(means=[0, 0, 0, 0], variances=[0.1, 0.1, 0.1, 0.1])
    # postprocessing
    self.NMS = tw.nn.MulticlassNMS('nms', background_offset=0)

    # build optim
    if self.Config.task == 'train':
      self.Matcher = tw.nn.AnchorMatcher(pos_iou_thr=0.50, neg_iou_thr=0.50, min_pos_iou=0.0)
      self.Optim = torch.optim.SGD([{'params': self.Model.parameters(),
                                     'lr': self.Config.train_lr,
                                     'momentum': 0.9}], weight_decay=1e-5)
    else:
      self.Optim = None

    # setting backbone to disable training
    # for m in self.Model.backbone.modules():
    #   if isinstance(m, nn.BatchNorm2d):
    #     for p in m.parameters():
    #       p.requires_grad_(False)

    # load model and possible optimizer
    if self.Config.model_path is not None:
      self._load()

    # extend to distributed
    if self.Config.dist_size > 1:
      self.Model = torch.nn.SyncBatchNorm.convert_sync_batchnorm(self.Model)
      self.Model = torch.nn.parallel.DistributedDataParallel(self.Model, device_ids=[self.Config.dist_rank])

  def _dump(self):
    """dump current checkpoint
    """
    cfg = self.Config
    path = f'{cfg.root}/model.epoch-{self.Epoch}.step-{self.Step}.pth'

    torch.save({
        'state_dict': self.Model.state_dict(),
        'global_step': self.Step,
        'global_epoch': self.Epoch,
        'optimizer': self.Optim
    }, path)

    logger.info(f'Model has saved in {path}')

  def _load(self):
    """Loading mode
    """
    cfg = self.Config

    logger.net('Loading model source: {}'.format(cfg.model_source))
    ckpt = tw.checkpoint.load(cfg.model_path)

    if cfg.model_source is None:
      tw.checkpoint.load_matched_state_dict(self.Model, ckpt)

    elif cfg.model_source == 'tw':
      content = tw.checkpoint.replace_prefix(ckpt['state_dict'], 'module.', '')
      tw.checkpoint.load_matched_state_dict(self.Model, content)

      if 'optimizer' in ckpt and self.Optim is not None:
        self.Optim.load_state_dict(ckpt['optimizer'])

      if 'global_step' in ckpt:
        self.Step = ckpt['global_step']

      if 'global_epoch' in ckpt:
        self.Epoch = ckpt['global_epoch']

    elif cfg.model_source == 'vanilla':
      tw.checkpoint.load_matched_state_dict(self.Model, ckpt['state_dict'])

    elif cfg.model_source == 'torchvision':
      tw.checkpoint.load_matched_state_dict(self.Model.backbone, ckpt)

    elif cfg.model_source == 'mmdet':
      tw.checkpoint.load_matched_state_dict(self.Model, ckpt['state_dict'])

    else:
      raise NotImplementedError(cfg.model_source)

  def _build_dataset(self, phase: tw.phase):
    """build train/val datasets
    """
    cfg = self.Config
    train_trans = functools.partial(transform_train, h=cfg.input_height, w=cfg.input_width)
    val_trans = functools.partial(transform_val, h=cfg.input_height, w=cfg.input_width)

    # build target dataset
    if phase == tw.phase.train:
      dataset = tw.datasets.CocoDetection(root='_datasets/coco2017/train2017',
                                          annotation='_datasets/coco2017/annotations/instances_train2017.json',
                                          transform=train_trans,
                                          phase=tw.phase.train,
                                          with_bbox=True,
                                          with_segm=False,
                                          with_kps=False,
                                          background_offset=1,
                                          num_classes=81)
    elif phase == tw.phase.val:
      dataset = tw.datasets.CocoDetection(root='_datasets/coco2017/val2017',
                                          annotation='_datasets/coco2017/annotations/instances_val2017.json',
                                          transform=val_trans,
                                          phase=tw.phase.val,
                                          with_bbox=True,
                                          with_segm=False,
                                          with_kps=False,
                                          background_offset=1,
                                          num_classes=81)
    else:
      raise NotImplementedError

    if phase == tw.phase.train:
      return torch.utils.data.DataLoader(
          dataset=dataset,
          batch_size=cfg.train_batchsize,
          shuffle=True,
          num_workers=4,
          collate_fn=tw.datasets.SampleCollator(),
          pin_memory=True,
          drop_last=True)

    elif phase == tw.phase.val:
      return torch.utils.data.DataLoader(
          dataset=dataset,
          batch_size=cfg.val_batchsize,
          shuffle=False,
          num_workers=4,
          collate_fn=tw.datasets.SampleCollator(),
          pin_memory=False,
          drop_last=False)

    else:
      raise NotImplementedError

  def _viz(self, **kwargs):
    """visualize"""
    cfg = self.Config
    device = cfg.device

    # visualize during training
    if 'viz_output' in kwargs:
      viz_output = kwargs['viz_output']
    else:
      viz_output = cfg.viz_output

    if 'viz_input' in kwargs:
      viz_input = kwargs['viz_input']
    else:
      viz_input = cfg.viz_input

    # collect inputs
    images, videos = tw.media.collect(viz_input)
    if not os.path.exists(viz_output):
      os.makedirs(viz_output)

    # process images
    for filepath in tqdm.tqdm(sorted(images)):

      dst = os.path.join(viz_output, os.path.basename(filepath))
      frame = cv2.imread(filepath).astype('float32')
      frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
      ih, iw, _ = frame.shape

      # preprocessing
      inputs = T.to_tensor(frame, mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375])
      inputs = inputs.to(device).unsqueeze(0)

      # resize to short side 800 to inference
      if True:
        if ih > iw:
          w = 800
          h = int(ih * 800.0 / iw)
        else:
          h = 800
          w = int(iw * 800.0 / ih)
        inputs = nn.functional.interpolate(inputs, [h, w], mode='bilinear')
        rh = ih / h
        rw = iw / w
      else:
        rh = 1.0
        rw = 1.0
        h = ih
        w = iw

      # padding to divisible for 32
      inputs = T.pad_to_size_divisible([inputs[0]], size_divisible=32)

      # inference
      cls_scores, bbox_regs = self.Model(inputs)
      
      # build anchor
      feature_shapes = [list(layer.shape[-2:]) for layer in bbox_regs]
      anchors = self.Anchor.forward(feature_shapes, img_h=h, img_w=w)
      
      # process for every layer
      bboxes, scores = [], []
      for cls_score, bbox_reg, anchor in zip(cls_scores, bbox_regs, anchors):
        # assume inference a single image
        cls_score, bbox_reg = cls_score[0], bbox_reg[0]
        # [c, h, w] -> [h, w, c]
        cls_score = cls_score.permute(1, 2, 0).reshape(-1, cfg.num_classes - 1)
        # [c, h, w] -> [h * w * anchors, 4]
        bbox_reg = bbox_reg.permute(1, 2, 0).reshape(-1, 4)
        # sigmoid
        cls_score = cls_score.sigmoid()
        # find max score
        max_score, _ = cls_score.max(-1)
        # filter out small scores
        pre_nms_num = min(cfg.pre_nms_num, bbox_reg.size(0))
        _, top_inds = max_score.topk(pre_nms_num)
        # select
        anchor = anchor[top_inds]
        cls_score = cls_score[top_inds]
        bbox_reg = bbox_reg[top_inds]
        # decode
        decode_bbox = self.BoxCoder.decode(bbox_reg, anchor)
        bboxes.append(decode_bbox)
        scores.append(cls_score)
      
      # [4630, 80], [4630, 4]
      scores = torch.cat(scores, dim=0)
      bboxes = torch.cat(bboxes, dim=0)

      # doing nms
      preds, logits = self.NMS(bboxes=bboxes.cpu(),
                               scores=scores.cpu(),
                               conf_thresh=cfg.conf_thresh,
                               nms_thresh=cfg.nms_thresh,
                               max_instances=-1)
      boxes = preds[..., :4]
      scores = preds[..., 4]

      inds = scores > cfg.post_conf_thresh
      boxes = boxes[inds]
      scores = scores[inds]

      # render
      boxes = boxes.cpu().numpy()
      dets = boxes * np.array([rw, rh, rw, rh])
      image = tw.drawer.boundingbox(frame, dets)
      cv2.imwrite(dst, image)

  def _optimize(self, samples, anchors, prediction, **kwargs):
    """calculate ssd losses (multibox losses)

    Args:
        samples (list[SampleMeta]): [bs, ]
        anchors ([torch.Tensor]): [n, 4]
        prediction (tuple):
          cls_pred ([torch.Tensor]): [bs, n, 81]
          bbox_pred ([torch.Tensor]): [bs, n, 4]

    """
    cfg = self.Config
    device = cfg.device
    losses = {'loss_cls': 0, 'loss_bbox_pos': 0}

    # decoupled outputs
    cls_pred, bbox_pred = prediction

    # compute losses for each sample
    total_pos_bbox = 0
    for img_id, sample in enumerate(samples):

      # -1: without-pts, 1: with-pts, 0: bg
      gt_bbox = torch.tensor(sample[1].bboxes).float().to(device)
      gt_label = torch.tensor(sample[1].label).long().to(device)

      # no groundtruth
      if gt_bbox.size(0) == 0:
        continue

      # finding the relationship anchors and gt_bbox
      # [N, 4], [K, 4], [K, ] -> [N, ], [N, ]
      gt_inds, gt_labels = self.Matcher(anchors, gt_bbox, gt_label)

      # compute bounding box cls
      pos_bbox_inds = torch.nonzero(gt_inds > 0, as_tuple=False).squeeze(-1).unique()  # fg
      neg_bbox_inds = torch.nonzero(gt_inds == 0, as_tuple=False).squeeze(-1).unique()  # bg
      num_pos_bbox = pos_bbox_inds.numel()

      if num_pos_bbox > 0:
        # accumulate
        total_pos_bbox += num_pos_bbox
        # index offset from 1~K to 0~K-1
        pos_gt_bbox_inds = gt_inds[pos_bbox_inds] - 1

        # placing positive encoded anchor into targets. # [pos, 4]
        labels = anchors.new_zeros(anchors.size(0), dtype=torch.long)
        labels[pos_bbox_inds] = gt_label[pos_gt_bbox_inds]  # [pos, ]

        # compute class loss over all bboxes. # [N, ], [N, ]
        loss_bbox_cls = self.loss_bbox_cls(cls_pred[img_id], labels)
        # hard-sample mining
        num_neg_bbox = min(neg_bbox_inds.numel(), int(cfg.neg_pos_ratio * num_pos_bbox))
        loss_bbox_cls_neg, _ = loss_bbox_cls[neg_bbox_inds].topk(num_neg_bbox)
        losses['loss_cls'] += loss_bbox_cls[pos_bbox_inds].sum() + loss_bbox_cls_neg.sum()

        # compute bbox localization loss: select positive bboxes
        pos_bbox_targets = self.BoxCoder.encode(gt_bbox[pos_gt_bbox_inds, :], anchors[pos_bbox_inds])
        loss_bbox_loc_loss = self.loss_bbox_loc(bbox_pred[img_id][pos_bbox_inds], pos_bbox_targets)
        losses['loss_bbox_pos'] += loss_bbox_loc_loss.sum()

    if total_pos_bbox > 0:
      losses['loss_cls'] /= total_pos_bbox
      losses['loss_bbox_pos'] /= total_pos_bbox

    return losses

  def _train(self, **kwargs):
    """train
    """
    cfg = self.Config
    device = self.Config.device
    init_step = self.Step
    stat = tw.stat.AverSet()
    start_time = tw.timer.tic()

    # build train dataset
    train_loader = self._build_dataset(tw.phase.train)
    val_loader = self._build_dataset(tw.phase.val)
    total_step = len(train_loader) * cfg.train_epoch

    # print trainable parameters
    tw.checkpoint.print_trainable_variables(self.Model)

    # build optimizer
    h, w = cfg.input_height, cfg.input_width

    if cfg.model_backbone == 'mobilenet_v2':
      lr_steps = [50 * len(train_loader), 70 * len(train_loader), 75 * len(train_loader)]
      lr_scheduler = tw.optim.WarmupMultiStepLR(self.Optim, lr_steps)
      sizes = [[20, 20], [10, 10], [5, 5], [3, 3], [2, 2], [1, 1]]
      priorbox = self.Anchor.forward(sizes, img_h=h, img_w=w)
      priorbox = torch.cat(priorbox, dim=0).to(device)
    else:
      raise NotImplementedError

    # prepare losses
    self.loss_bbox_cls = nn.CrossEntropyLoss(reduction='none')
    self.loss_bbox_loc = tw.nn.SmoothL1Loss(beta=1.0, reduction=None)

    # training
    while self.Epoch < cfg.train_epoch:

      self.Epoch += 1
      self.Model.train()

      for samples in train_loader:

        # prepare data
        self.Step += 1

        # convert data into tensor
        images = []
        for sample in samples:
          if cfg.input_colorspace in ['RGB', 'YUV']:
            images.append(sample[0].bin.float().to(device))
          elif cfg.input_colorspace in ['Y']:
            images.append(sample[0].bin[0][None].float().to(device))
          else:
            raise NotImplementedError(cfg.input_colorspace)
        images = torch.stack(images, dim=0).float().to(device)
        bs = images.size(0)

        # cls scores and bbox regression
        bbox_cls, bbox_reg = self.Model(images)
        bbox_cls = torch.cat([l.permute(0, 2, 3, 1).contiguous().view(bs, -1, cfg.num_classes)
                             for l in bbox_cls], dim=1)
        bbox_reg = torch.cat([c.permute(0, 2, 3, 1).contiguous().view(bs, -1, 4) for c in bbox_reg], dim=1)

        # compute losses
        losses = self._optimize(samples, priorbox, (bbox_cls, bbox_reg))

        # accumulate
        loss = sum(loss for loss in losses.values())
        self.Optim.zero_grad()
        loss.backward()
        self.Optim.step()
        lr_scheduler.step()

        # iter
        losses.update({
            'loss': sum(loss for loss in losses.values()),
            'time': logger.toc(),
        })
        stat.update(losses)
        logger.tic()

        # print
        if tw.runner.reach(self.Step, cfg.log):
          eta = tw.timer.remain_eta(self.Step, total_step, start_time, init_step)
          tw.runner.log(keys=['eta'] + stat.keys() + ['lr'],
                        values=[eta] + stat.values() + [self.Optim.param_groups[0]['lr']],
                        step=self.Step,
                        epoch=self.Epoch,
                        tag='train',
                        iters_per_epoch=len(train_loader),
                        writer=self.Writer)
          stat.reset()

      if tw.runner.reach(self.Epoch, cfg.log_save) and self.Master:
        self._dump()

      if tw.runner.reach(self.Epoch, cfg.log_val) and self.Master:
        self._val(loader=val_loader)

  def _tensorrt(self, **kwargs):
    """export to tensorrt models
    """
    cfg = self.Config
    tw.export.onnx_to_trt(
        f'ssd.{cfg.model_backbone}.onnx',
        f'ssd.{cfg.model_backbone}.engine',
        shapes={'input': {'min': (1, 3, 384, 384), 'best': (1, 3, 384, 384), 'max': (1, 3, 384, 384)}},
        verbose=True)

  def _onnx(self, **kwargs):
    """export model to onnx
    """
    cfg = self.Config

    inputs = torch.rand(1, 3, 256, 256).to(cfg.device)
    tw.flops.register(self.Model)
    with torch.no_grad():
      self.Model(inputs)
    print(tw.flops.accumulate(self.Model))
    tw.flops.unregister(self.Model)
    tw.export.torch_to_onnx(self.Model.eval(),
                            torch.rand(1, 3, 256, 256).to(cfg.device),
                            f'ssd.{cfg.model_backbone}.onnx',
                            input_names=['input', ],
                            output_names=['output', ],
                            dynamic_axes={'input': {0: 'batch', 2: 'height', 3: 'width'}})

  def _val(self, **kwargs):
    """validate after epoch
    """
    cfg = self.Config
    device = self.Config.device
    start_time = tw.timer.tic()
    total = 0

    # reset
    self.Model.eval()
    if self.Evaluator is None:
      self.Evaluator = tw.evaluator.CocoEvaluator(
          annotation='_datasets/coco2017/annotations/instances_val2017.json',
          with_bbox=True, with_segm=False, with_kps=False)
      self.Evaluator.to(cfg.device)
    self.Evaluator.reset()

    # build dataloader
    if 'loader' in kwargs and kwargs['loader'] is not None:
      val_loader = kwargs['loader']
    else:
      val_loader = self._build_dataset(tw.phase.val)

    # create folder for every epoch
    root = tw.fs.mkdirs(f'{cfg.root}/val/epoch_{self.Epoch}_step_{self.Step}/')

    # build anchor
    priorbox = None

    with torch.no_grad():
      for samples in tqdm.tqdm(val_loader):

        # convert data into tensor
        images = []
        for sample in samples:
          if cfg.input_colorspace in ['RGB', 'YUV']:
            images.append(sample[0].bin.float().to(device))
          elif cfg.input_colorspace in ['Y']:
            images.append(sample[0].bin[0][None].float().to(device))
          else:
            raise NotImplementedError(cfg.input_colorspace)
        images = torch.stack(images, dim=0).float().to(device)
        bs = images.size(0)

        # cls scores and bbox regression
        bbox_scores, bbox_regs = self.Model(images)
        feature_shapes = [list(l.shape[-2:]) for l in bbox_regs]

        # -> [bs, 8732, 4], [bs, 8732, 31]
        bbox_regs = torch.cat([l.permute(0, 2, 3, 1).contiguous().view(bs, -1, 4) for l in bbox_regs], dim=1)
        bbox_scores = torch.cat([c.permute(0, 2, 3, 1).contiguous().view(bs, -1, cfg.num_classes)
                                for c in bbox_scores], dim=1)
        bbox_scores = bbox_scores.softmax(dim=-1)

        # construct priorbox
        if priorbox is None:
          priorbox = self.Anchor.forward(feature_shapes, img_h=cfg.input_height, img_w=cfg.input_width)
          priorbox = torch.cat(priorbox, dim=0)

        # process every image
        results = []
        for img_id in range(bs):

          # rescale sample to original size
          sample = samples[img_id]
          sample[0].bin = None
          resize_op = sample[0].transform[0]
          assert resize_op[0] == 'resize'
          scale_h, scale_w = resize_op[1] / resize_op[2], resize_op[3] / resize_op[4]

          # postprocess
          scores = bbox_scores[img_id]
          regs = bbox_regs[img_id]
          boxes = self.BoxCoder.decode(regs, priorbox)
          preds, logits = self.NMS(bboxes=boxes.cpu(),
                                   scores=scores.cpu(),
                                   conf_thresh=cfg.conf_thresh,
                                   nms_thresh=cfg.nms_thresh,
                                   max_instances=-1)

          if len(preds) == 0:
            continue
          boxes = preds[..., :4] * torch.tensor([scale_w, scale_h, scale_w, scale_h])
          scores = preds[..., 4]

          # x1y1x2y2 to xywh
          boxes[..., 2] = boxes[..., 2] - boxes[..., 0] + 1
          boxes[..., 3] = boxes[..., 3] - boxes[..., 1] + 1
          results.append({
              'image_id': sample[0].id,
              'logits': logits.numpy(),  # [N, ]
              'bboxes': boxes.numpy(),  # [N, 4 (x1, y1, w, h)]
              'scores': scores.numpy()  # [N, ]
          })

        # eval
        self.Evaluator.append(results)

    # stat
    reports = self.Evaluator.accumulate()
    elapsed = tw.timer.duration(start_time, tw.timer.tic())
    throughput = tw.timer.throughput(elapsed, total)
    keys = list(reports.keys()) + ['time', 'throughtput']
    vals = list(reports.values()) + [elapsed, throughput]
    tw.runner.log(keys=keys, values=vals, step=self.Step, epoch=self.Epoch, tag='val', writer=self.Writer)

  def __call__(self):
    """prepare basic
    """
    cfg = self.Config

    if cfg.task == 'train':
      self._train()

    elif cfg.task == 'val':
      with torch.no_grad():
        self._val()

    elif cfg.task == 'viz':
      with torch.no_grad():
        self.Model.eval()
        self._viz()

    elif cfg.task == 'onnx':
      with torch.no_grad():
        self._onnx()

    elif cfg.task == 'trt':
      with torch.no_grad():
        self._tensorrt()

    else:
      raise NotImplementedError(cfg.task)


if __name__ == "__main__":

  parser = argparse.ArgumentParser()

  # ---------------------------------------------
  #  USED BY COMMON
  # ---------------------------------------------
  parser.add_argument('--task', type=str, default=None, choices=['train', 'val', 'test', 'viz', 'onnx', 'trt'])
  parser.add_argument('--dataset', type=str, default='coco2017', choices=['coco2017'])

  # ---------------------------------------------
  #  USED BY LOGGER
  # ---------------------------------------------
  parser.add_argument('--log', type=int, default=10, help="display interval step.")
  parser.add_argument('--log-val', type=int, default=1, help="running validation in terms of step.")
  parser.add_argument('--log-save', type=int, default=1, help="saveing checkpoint with interval.")

  # ---------------------------------------------
  #  USED BY MODEL-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--model-backbone', type=str, choices=['resnet50'])
  parser.add_argument('--model-path', type=str, default=None, help="loadding pretrain/last-checkpoint model.")
  parser.add_argument('--model-source', type=str, default=None)

  # ---------------------------------------------
  #  USED BY INPUT-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--input-colorspace', type=str, default='RGB', choices=['Y', 'RGB', 'YUV'])
  parser.add_argument('--input-height', type=int, default=800, help="fixed size to training.")
  parser.add_argument('--input-width', type=int, default=800, help="fixed size to training.")

  parser.add_argument('--pre-nms-num', type=int, default=1000, help="number of bbox filte.r")
  parser.add_argument('--post-nms-num', type=int, default=100, help="number of bbox filter.")
  parser.add_argument('--num_classes', type=int, default=81, help="num classes with background.")
  parser.add_argument('--nms-thresh', type=float, default=0.5, help="nms merging score.")
  parser.add_argument('--conf-thresh', type=float, default=0.05, help="pre-nms to filter low bounding box.")
  parser.add_argument('--post-conf-thresh', type=float, default=0.5, help="post-nms to filter low bounding box.")
  parser.add_argument('--neg-pos-ratio', type=float, default=3.0, help="number of negative anchors relative to postives.")  # nopep8

  # ---------------------------------------------
  #  USED BY TRAIN-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--train-lr', type=float, default=0.1, help="total learning rate across devices.")
  parser.add_argument('--train-batchsize', type=int, default=1, help="total batch size across devices.")
  parser.add_argument('--train-epoch', type=int, default=100, help="total training epochs.")
  parser.add_argument('--train-optimizer', type=str, default='sgd', choices=['sgd', 'adam'], help="training optimizer.")

  # ---------------------------------------------
  #  USED BY VAL-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--val-batchsize', type=int, default=16, help="total batch size across devices.")

  # ---------------------------------------------
  #  USED BY VIZ-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--viz-input', type=str, help='input path could be a folder/filepath.')
  parser.add_argument('--viz-output', type=str, help='output path should be a folder path.')

  # generate config
  args, _ = parser.parse_known_args()

  # runner
  tw.runner.launch(parser, RetinaNetDetector)
