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
"""Bigolive face detector based on RetinaFace

    1. use Y-channel as input
    2. use short-side 256 resize as inferencing

"""
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
from torch.nn import functional as F
import tw
from tw import logger
from tw import transform as T

import detector


def transform_train(metas):
  T.random_zoom_in_crop(metas)
  T.random_photometric_distortion(metas)
  T.pad_to_square(metas)

  # NOTE: flip image but keep organs keypoints fixed.
  # NOTE: exchange eys and mouth landmarks.
  if random.random() > 0.5:
    T.hflip(metas)
    kps = metas[2].keypoints.reshape(-1, 5, 2)
    kps[..., 0, :], kps[..., 1, :] = kps[..., 1, :].copy(), kps[..., 0, :].copy()
    kps[..., 3, :], kps[..., 4, :] = kps[..., 4, :].copy(), kps[..., 3, :].copy()
    metas[2].keypoints = kps.reshape(-1, 2)

  T.resize(metas, 320, 320)
  T.to_tensor(metas, mean=[104.0, 117.0, 123.0])

  metas[0].bin = T.change_colorspace(metas[0].bin, src=T.COLORSPACE.BGR, dst=T.COLORSPACE.BT709_FULLRANGE)
  return metas


def transform_test(metas):
  T.to_tensor(metas, mean=[104.0, 117.0, 123.0])
  metas[0].bin = T.change_colorspace(metas[0].bin, src=T.COLORSPACE.BGR, dst=T.COLORSPACE.BT709_FULLRANGE)
  return metas

class BigoLiveFaceDetector():

  def __init__(self, config):
    self.Config = config

    # overwrite when dist
    if self.Config.dist_size > 1:
      self.Config.device = 'cuda:{}'.format(self.Config.dist_rank)
    self.Master = True if self.Config.dist_rank == 0 else False

    # evaluation and tensorboard
    self.Writer = tensorboard.SummaryWriter(log_dir=self.Config.root)

    # scalar
    self.Epoch = 0
    self.Step = 0

    # coder for bbox and points
    self.BoxCoder = tw.nn.GeneralBoxCoder(
        means=[0, 0, 0, 0],
        variances=[0.1, 0.1, 0.2, 0.2])
    self.PtsCoder = tw.nn.BboxPtsCoder(
        means=[0, 0],
        variances=[0.1, 0.1])

    # postprocessing
    self.NMS = tw.nn.NonMaxSuppression()

    # models
    self.Anchor, self.Model = self._build_model()

    # build optim
    if self.Config.task == 'train':
      self.Matcher = tw.nn.AnchorMatcher(pos_iou_thr=0.35, neg_iou_thr=0.35, min_pos_iou=0.20)
      self.Optim = torch.optim.SGD([{'params': self.Model.parameters(),
                                     'lr': self.Config.train_lr,
                                     'momentum': 0.9}], weight_decay=5e-4)
    else:
      self.Optim = None

    # load model and possible optimizer
    if self.Config.model_path is not None:
      self._load()

    # extend to distributed
    if self.Config.dist_size > 1:
      self.Model = torch.nn.SyncBatchNorm.convert_sync_batchnorm(self.Model)
      self.Model = torch.nn.parallel.DistributedDataParallel(self.Model, device_ids=[self.Config.dist_rank])

  def _build_model(self):
    """build model
    """
    cfg = self.Config

    # different input format
    if self.Config.input_colorspace in ['Y']:
      in_channels = 1
    elif self.Config.input_colorspace in ['RGB', 'YUV']:
      in_channels = 3
    else:
      raise NotImplementedError

    # 640 x 640 Input
    # anchor_sizes=[[16, 32], [64, 128], [256, 512]]
    # anchor_strides=[8, 16, 32]
    # anchor_ratios=[1.0, ]

    # 320 x 320 Input
    anchor_sizes = [[8, 16], [32, 64], [128, 256]]
    anchor_strides = [8, 16, 32]
    anchor_ratios = [1.0, ]

    # build anchor
    anchor = tw.nn.RetinaFaceAnchorGenerator(
        anchor_sizes=anchor_sizes,
        anchor_strides=anchor_strides,
        anchor_ratios=anchor_ratios)
    anchor_nums = [len(sizes) * len(anchor_ratios) for sizes in anchor_sizes]

    # select different backbone
    if cfg.model_backbone == 'mobilenet':
      model = detector.BigoliveFaceNet(
          arch='mobilenet',
          in_channels=in_channels,
          fpn_in_channels=32,
          fpn_out_channels=64,
          anchor_num=anchor_nums)
    else:
      raise NotImplementedError(cfg.model_backbone)

    anchor.to(cfg.device)
    model.to(cfg.device)
    return anchor, model

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
      content = tw.checkpoint.replace_prefix(ckpt['state_dict'], 'module.', '')
      tw.checkpoint.load_matched_state_dict(self.Model, content)

    elif cfg.model_source == 'retinaface':
      tw.checkpoint.load_matched_state_dict(self.Model, ckpt)

    else:
      raise NotImplementedError(cfg.model_source)

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
      ih, iw, _ = frame.shape

      resized = cv2.resize(frame, (192, 320))
      h, w, _ = resized.shape
      rh = ih / h
      rw = iw / w

      # preprocessing
      inputs = T.to_tensor(resized, mean=[104, 117, 123])
      if cfg.input_colorspace in ['Y', 'YUV']:
        inputs = T.change_colorspace(inputs, src=T.COLORSPACE.BGR, dst=T.COLORSPACE.BT709_FULLRANGE)
      if cfg.input_colorspace in ['Y']:
        inputs = inputs[0][None]
      inputs = inputs.to(device).unsqueeze(0)

      # inference
      # -> [1, 34688, 4], [1, 34688, 2], [1, 34688, 10], [1, 34688, 1]
      loc, conf, landmarks, iou = self.Model(inputs)

      # to single image
      loc, conf, landmarks, iou = loc[0], conf[0], landmarks[0], iou[0]

      # score to conf
      # alpha = 0.5
      # conf = conf.pow(alpha) * iou.pow(1 - alpha)

      # postprocessing
      priorbox = self.Anchor.forward(
          [[h // 8, w // 8], [h // 16, w // 16], [h // 32, w // 32]],
          img_h=h, img_w=w)
      priorbox = torch.cat(priorbox, dim=0)
      boxes = self.BoxCoder.decode(loc, priorbox)

      # conf[:, 0] is non-face
      select = conf[:, 1] > cfg.pre_conf_thresh
      boxes = torch.cat([boxes, conf[:, 1].unsqueeze(1)], dim=1)[select]

      # to cpu
      nms_boxes, nms_inds = self.NMS(boxes.cpu(), thresh=cfg.nms_thresh, max_proposals=100)
      nms_boxes = nms_boxes.cpu().numpy()
      post_select = nms_boxes[:, -1] > cfg.post_conf_thresh
      nms_boxes = nms_boxes[post_select]
      dets = nms_boxes * np.array([rw, rh, rw, rh, 1.0])

      # render
      image = tw.drawer.boundingbox(frame, dets, labels=[1] * dets.shape[0])

      # preprocessing landmarks [N, 5, 2]
      landmarks = self.PtsCoder.decode(landmarks, priorbox)
      landmarks = landmarks[select][nms_inds][post_select].cpu().reshape(-1, 2).numpy() * np.array([rw, rh])
      image = tw.drawer.keypoints(image, landmarks, radius=2)

      cv2.imwrite(dst, image)

  def _build_dataset(self, phase: tw.phase):
    """build train/val datasets
    """
    cfg = self.Config

    # build target dataset
    if phase == tw.phase.train:
      dataset = tw.datasets.WiderFace(path=cfg.dataset_train, transform=transform_train)

    elif phase == tw.phase.test and self.Master:
      dataset = tw.datasets.WiderFaceTest(path=cfg.dataset_test, transform=transform_test)

    else:
      raise NotImplementedError

    if phase == tw.phase.train:
      return torch.utils.data.DataLoader(
          dataset=dataset,
          batch_size=cfg.train_batchsize,
          shuffle=True,
          num_workers=16,
          collate_fn=tw.datasets.SampleCollator(),
          pin_memory=True,
          drop_last=True)

    elif phase == tw.phase.test:
      return torch.utils.data.DataLoader(
          dataset=dataset,
          batch_size=1,
          shuffle=False,
          num_workers=4,
          collate_fn=tw.datasets.SampleCollator(),
          pin_memory=False,
          drop_last=False)

    else:
      raise NotImplementedError

  def _optimize(self, samples, anchors, prediction, **kwargs):
    """calculate retinaface losses (multibox losses)

    Args:
        samples (list[SampleMeta]): [bs, ]
        anchors ([torch.Tensor]): [n, 4]
        prediction (tuple):
          bbox_pred ([torch.Tensor]): [bs, n, 4]
          cls_pred ([torch.Tensor]): [bs, n, 2]
          pts_pred ([torch.Tensor]): [bs, n, 10]

    """
    cfg = self.Config
    device = cfg.device
    losses = {'loss_cls': 0, 'loss_bbox_pos': 0, 'loss_pts_pos': 0, 'loss_iou_aware': 0, 'loss_iou': 0}

    # decoupled outputs
    bbox_pred, cls_pred, pts_pred, iou_pred = prediction

    # compute losses for each sample
    total_pos_bbox = 0
    total_pts = 0
    for img_id, sample in enumerate(samples):

      # -1: without-pts, 1: with-pts, 0: bg
      gt_bbox = torch.tensor(sample[1].bboxes).float().to(device)
      gt_label = torch.tensor(sample[1].label).long().to(device)
      gt_pts = torch.tensor(sample[2].keypoints).float().to(device)  # [K * 5, 2]
      gt_pts = torch.reshape(gt_pts, [gt_bbox.size(0), -1])

      # no groundtruth
      if gt_bbox.size(0) == 0:
        continue

      # finding the relationship anchors and gt_bbox
      # [N, 4], [K, 4], [K, ] -> [N, ], [N, ]
      gt_inds, gt_labels = self.Matcher(anchors, gt_bbox, gt_label)

      # collect keypoints number: gt_labels == 1 as bounding box with pts
      pos_pts_inds = torch.nonzero(gt_labels > 0, as_tuple=False).squeeze(-1).unique()
      num_pts = pos_pts_inds.numel()

      # encoding keypoints with anchor offset into targets.
      if num_pts > 0:

        # total points samples
        total_pts += num_pts

        # finding corresponding groundtruth index
        pos_gt_pts_inds = gt_inds[pos_pts_inds] - 1

        # encoding positive pts part
        pos_pts_targets = self.PtsCoder.encode(gt_pts[pos_gt_pts_inds, :], anchors[pos_pts_inds])

        # prediction
        pos_pts_pred = pts_pred[img_id][pos_pts_inds]
        losses['loss_pts_pos'] += self.loss_pts_loc(pos_pts_pred, pos_pts_targets).sum()

      # compute bounding box cls
      pos_bbox_inds = torch.nonzero(gt_inds > 0, as_tuple=False).squeeze(-1).unique()  # fg
      neg_bbox_inds = torch.nonzero(gt_inds == 0, as_tuple=False).squeeze(-1).unique()  # bg
      num_pos_bbox = pos_bbox_inds.numel()

      if num_pos_bbox > 0:

        # accumulate
        total_pos_bbox += num_pos_bbox
        # index offset from 1~K to 0~K-1
        pos_gt_bbox_inds = gt_inds[pos_bbox_inds] - 1

        # compute bbox classification loss
        gt_label[gt_label == -1] = 1

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

        # compute iou losses
        decode_bbox_target = self.BoxCoder.decode(pos_bbox_targets, anchors[pos_bbox_inds])
        decode_bbox_pred = self.BoxCoder.decode(bbox_pred[img_id][pos_bbox_inds], anchors[pos_bbox_inds])
        losses['loss_iou'] += self.loss_iou_loc(decode_bbox_pred, decode_bbox_target).sum()

        # compute iou-aware losses
        iou = T.bbox.aligned_iou(decode_bbox_pred, decode_bbox_target).unsqueeze(dim=-1)
        losses['loss_iou_aware'] += self.loss_iou_reg(iou_pred[img_id][pos_bbox_inds], iou).sum()

    if total_pos_bbox > 0:
      losses['loss_cls'] /= total_pos_bbox
      losses['loss_bbox_pos'] /= total_pos_bbox
      losses['loss_bbox_pos'] *= 2.0
      losses['loss_iou_aware'] /= total_pos_bbox
      losses['loss_iou'] /= total_pos_bbox

    if total_pts > 0:
      losses['loss_pts_pos'] /= total_pts

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
    total_step = len(train_loader) * cfg.train_epoch

    # print trainable parameters
    tw.checkpoint.print_trainable_variables(self.Model)

    # build optimizer
    lr_steps = [190 * len(train_loader), 220 * len(train_loader)]
    # lr_scheduler = tw.optim.WarmupMultiStepLR(self.Optim, lr_steps, warmup_iters=500)
    lr_scheduler = torch.optim.lr_scheduler.MultiStepLR(self.Optim, lr_steps, gamma=0.1)

    # since the network use fixed size to training, we generate priorbox first
    h, w = cfg.train_height, cfg.train_width
    priorbox = self.Anchor.forward([[h // 8, w // 8], [h // 16, w // 16], [h // 32, w // 32]], img_h=h, img_w=w)
    priorbox = torch.cat(priorbox, dim=0).to(device)

    # prepare losses
    self.loss_bbox_cls = nn.CrossEntropyLoss(reduction='none')
    self.loss_bbox_loc = tw.nn.SmoothL1Loss(beta=1.0, reduction=None)
    self.loss_pts_loc = tw.nn.SmoothL1Loss(beta=1.0, reduction=None)
    self.loss_iou_reg = nn.BCEWithLogitsLoss(reduction='none')
    self.loss_iou_loc = tw.nn.GIoULoss()

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

        # [bs, n, 4], [bs, n, 2], [bs, n, 10]
        predictions = self.Model(images)

        # compute losses
        losses = self._optimize(samples, priorbox, predictions)

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

      # if tw.runner.reach(self.Epoch, cfg.log_val) and self.Master:
      #   self._val(loader=val_loader)

      if tw.runner.reach(self.Epoch, cfg.log_test) and self.Master:
        with torch.no_grad():
          self._test()

  def _test(self, **kwargs):
    """Test on widerface datasets

    Raises:
        NotImplementedError: [description]
    """

    cfg = self.Config
    device = self.Config.device
    start_time = tw.timer.tic()
    total = 0

    # reset
    self.Model.eval()

    # create folder for every epoch
    root = tw.fs.mkdirs(f'{cfg.root}/test/epoch_{self.Epoch}_step_{self.Step}/')
    dataset_dir = os.path.dirname(os.path.abspath(cfg.dataset_test))
    
    test_loader = self._build_dataset(tw.phase.test)

    # mkdir folder first
    # files = []
    # with open(cfg.dataset_test) as fp:
    #   for line in tqdm.tqdm(fp):
    #     name = line[1:].replace('\n', '')
    #     dstpath = os.path.join(root, name)[:-3] + 'txt'
    #     if not os.path.exists(os.path.dirname(dstpath)):
    #       os.makedirs(os.path.dirname(dstpath))

    # processing
    for samples in tqdm.tqdm(test_loader):

      images = []
      for sample in samples:
        if cfg.input_colorspace in ['RGB', 'YUV']:
          images.append(sample[0].bin.float().to(device))
        elif cfg.input_colorspace in ['Y']:
          images.append(sample[0].bin[0][None].float().to(device))
        else:
          raise NotImplementedError(cfg.input_colorspace)
      images = torch.stack(images, dim=0).float().to(device)
      n, c, ih, iw = images.shape

      # resize to short side 256 to inference
      if True:
        if ih > iw:
          w = 256
          h = int(ih * 256.0 / iw)
        else:
          h = 256
          w = int(iw * 256.0 / ih)
        images = nn.functional.interpolate(images, [h, w], mode='bilinear')
        rh = ih / h
        rw = iw / w
      else:
        rh = 1.0
        rw = 1.0
        h = ih
        w = iw
        
      # inference
      # -> [1, 34688, 4], [1, 34688, 2], [1, 34688, 10], [1, 34688, 1]
      loc, conf, landmarks, iou = self.Model(images)

      # to single image
      loc, conf, landmarks, iou = loc[0], conf[0], landmarks[0], iou[0]

      # score to conf
      alpha = 0.5
      conf = conf.pow(alpha) * iou.pow(1 - alpha)

      # postprocessing
      priorbox = self.Anchor.forward(
          [[math.ceil(h / 8), math.ceil(w / 8)],
           [math.ceil(h / 16), math.ceil(w / 16)],
           [math.ceil(h / 32), math.ceil(w / 32)]],
          img_h=h, img_w=w)
      priorbox = torch.cat(priorbox, dim=0)
      boxes = self.BoxCoder.decode(loc, priorbox)
      
      # conf[:, 0] is non-face
      select = conf[:, 1] > 0.02
      boxes = torch.cat([boxes, conf[:, 1].unsqueeze(1)], dim=1)[select]
      conf = conf[select, 1]

      # nms
      boxes, inds = self.NMS(boxes.cpu(), thresh=0.4, max_proposals=-1)

      # sort from large to small in terms of conf
      sorted_conf, inds = torch.sort(conf[inds], descending=True)
      sorted_boxes = boxes[inds].numpy()

      # write to string
      name = samples[0][0].caption
      line = name.split('/')[-1][:-4] + '\n' + str(len(sorted_boxes)) + '\n'
      for (x1, y1, x2, y2, conf) in sorted_boxes:
        x1, x2, y1, y2 = x1 * rw, x2 * rw, y1 * rh, y2 * rh
        line += '%d %d %d %d %.7f\n' % (int(x1), int(y1), int(x2 - x1 + 1), int(y2 - y1 + 1), conf)
      
      # save to file
      dstpath = os.path.join(root, name)[:-3] + 'txt'
      if not os.path.exists(os.path.dirname(dstpath)):
        os.makedirs(os.path.dirname(dstpath))
      with open(dstpath, 'w') as fw:
        fw.write(line)

    # compute AP
    aps = tw.evaluator.WiderfaceEvaluator(gt_root=cfg.dataset_test_gt).accumulate(root)

    # stat
    reports = {'easy@AP': aps[0], 'medium@AP': aps[1], 'hard@AP': aps[2]}
    elapsed = tw.timer.duration(start_time, tw.timer.tic())
    throughput = tw.timer.throughput(elapsed, total)
    keys = list(reports.keys()) + ['time', 'throughtput']
    vals = list(reports.values()) + [elapsed, throughput]
    tw.runner.log(keys=keys, values=vals, step=self.Step, epoch=self.Epoch, tag='test', writer=self.Writer)


  def _tensorrt(self, **kwargs):
    """export to tensorrt models
    """
    cfg = self.Config
    tw.export.onnx_to_trt(
        f'retinaface.{cfg.model_backbone}.onnx',
        f'retinaface.{cfg.model_backbone}.engine',
        shapes={'input': {'min': (1, 1, 256, 256), 'best': (1, 1, 384, 256), 'max': (1, 1, 384, 384)}},
        verbose=True)

  def _onnx(self, **kwargs):
    """export model to onnx
    """
    cfg = self.Config

    inputs = torch.rand(1, 1, 320, 192).to(cfg.device)
    tw.flops.register(self.Model)
    with torch.no_grad():
      self.Model(inputs)
    print(tw.flops.accumulate(self.Model))
    tw.flops.unregister(self.Model)
    # NOTE: tensorrt 7.0 support only opset_version=10 for interpolation op.
    tw.export.torch_to_onnx(self.Model.eval(),
                            torch.rand(1, 1, 320, 192).to(cfg.device),
                            f'retinaface.{cfg.model_backbone}.onnx',
                            input_names=['input', ],
                            output_names=['loc', 'conf'],
                            dynamic_axes={'input': {0: 'batch', 2: 'height', 3: 'width'}},
                            opset_version=10)
    
  def __call__(self):
    """prepare basic
    """
    cfg = self.Config

    if cfg.task == 'train':
      self._train()

    elif cfg.task == 'val':
      with torch.no_grad():
        self._val()

    elif cfg.task == 'test':
      with torch.no_grad():
        self._test()

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
  parser.add_argument('--dataset-train', type=str, default='_datasets/widerface/train/label.txt')
  parser.add_argument('--dataset-test', type=str, default='_datasets/widerface/val/wider_val.txt')
  parser.add_argument('--dataset-test-gt', type=str, default='_checkpoints/detection/widerface_ground_truth')

  # ---------------------------------------------
  #  USED BY LOGGER
  # ---------------------------------------------
  parser.add_argument('--log', type=int, default=10, help="display interval step.")
  parser.add_argument('--log-val', type=int, default=1, help="running validation in terms of step.")
  parser.add_argument('--log-test', type=int, default=10, help="running test in terms of step.")
  parser.add_argument('--log-save', type=int, default=1, help="saveing checkpoint with interval.")

  # ---------------------------------------------
  #  USED BY MODEL-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--model-backbone', type=str, choices=['mobilenet', 'resnet50'])
  parser.add_argument('--model-path', type=str, default=None, help="loadding pretrain/last-checkpoint model.")
  parser.add_argument('--model-source', type=str, default=None)

  # ---------------------------------------------
  #  USED BY INPUT-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--input-colorspace', type=str, default='RGB', choices=['Y', 'RGB', 'YUV'])
  parser.add_argument('--nms-thresh', type=float, default=0.4, help="nms merging score.")
  parser.add_argument('--pre-conf-thresh', type=float, default=0.5, help="pre-nms to filter background.")
  parser.add_argument('--post-conf-thresh', type=float, default=0.9, help="post-nms to filter low bounding box.")
  parser.add_argument('--neg-pos-ratio', type=float, default=7.0, help="number of negative anchors to postives.")

  # ---------------------------------------------
  #  USED BY TRAIN-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--train-lr', type=float, default=0.001, help="total learning rate across devices.")
  parser.add_argument('--train-batchsize', type=int, default=32, help="total batch size across devices.")
  parser.add_argument('--train-epoch', type=int, default=250, help="total training epochs.")
  parser.add_argument('--train-optimizer', type=str, default='sgd', choices=['sgd', 'adam'], help="training optimizer.")
  parser.add_argument('--train-height', type=int, default=320, help="fixed size to training.")
  parser.add_argument('--train-width', type=int, default=192, help="fixed size to training.")

  # ---------------------------------------------
  #  USED BY VAL-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--val-batchsize', type=int, default=1, help="total batch size across devices.")

  # ---------------------------------------------
  #  USED BY VIZ-SPECIFIC
  # ---------------------------------------------
  parser.add_argument('--viz-input', type=str, help='input path could be a folder/filepath.')
  parser.add_argument('--viz-output', type=str, help='output path should be a folder path.')

  # generate config
  args, _ = parser.parse_known_args()

  # runner
  tw.runner.launch(parser, BigoLiveFaceDetector)
