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
"""Bigolive game vsr
"""
import os
import abc
import tqdm
import functools

import cv2

import torch
from torch import nn
from torch.utils import tensorboard

import tw
from tw import logger
from tw import transform as T

import vsr_models


class VsrModelWrapper(nn.Module):

  r"""Compose model module for different training type.
  """

  def __init__(self, net_g: nn.Module, net_d: nn.Module = None, net_e: nn.Module = None):
    super(VsrModelWrapper, self).__init__()
    self.netG = net_g
    self.netD = net_d
    self.netE = net_e


class VsrBase(metaclass=abc.ABCMeta):

  def __init__(self, config):
    """vsr base
    """
    self.Config = config

    # overwrite when dist
    if self.Config.dist_size > 1:
      self.Config.device = 'cuda:{}'.format(self.Config.dist_rank)
    self.Master = True if self.Config.dist_rank == 0 else False

    # evaluation and tensorboard
    self.Evaluator = tw.evaluator.ImageSimilarityEvaluator(use_psnr=True, use_ssim=True, use_lpips=True)
    self.Evaluator.to(self.Config.device)
    self.Writer = tensorboard.SummaryWriter(log_dir=self.Config.root)

    # scalar
    self.Epoch = 0
    self.Step = 0

    # models
    self.Model = self._build_model()

    # build optim
    if self.Config.task == 'train':
      self.Optim = self._build_optim(self.Model)
    else:
      self.Optim = None

    # load model and possible optimizer
    if self.Config.model_path is not None:
      self._load()

    # extend to distributed
    if self.Config.dist_size > 1:
      model = torch.nn.SyncBatchNorm.convert_sync_batchnorm(model)
      model = torch.nn.parallel.DistributedDataParallel(model, device_ids=[self.Config.dist_rank])

  def transform_yuv_train(self, metas):
    """transform"""
    if self.Config.input_colorspace in ['YUV', 'Y']:
      T.change_colorspace(metas, T.COLORSPACE.BGR, T.COLORSPACE.BT709_FULLRANGE)
    elif self.Config.input_colorspace in ['RGB']:
      T.change_colorspace(metas, T.COLORSPACE.BGR, T.COLORSPACE.RGB)
    else:
      raise NotImplementedError(self.Config.model_colorpsace)

    T.to_tensor(metas, scale=255.0)
    return metas

  def transform_yuv_val(self, metas):
    """transform"""
    if self.Config.input_colorspace in ['YUV', 'Y']:
      T.change_colorspace(metas, T.COLORSPACE.BGR, T.COLORSPACE.BT709_FULLRANGE)
    elif self.Config.input_colorspace in ['RGB']:
      T.change_colorspace(metas, T.COLORSPACE.BGR, T.COLORSPACE.RGB)
    else:
      raise NotImplementedError(self.Config.model_colorpsace)

    T.to_tensor(metas, scale=255.0)
    return metas

  def _build_dataset(self, phase: tw.phase):
    """build train/val datasets
    """
    cfg = self.Config

    # build target dataset
    if phase == tw.phase.train:
      if cfg.model_type in ['frvsr']:
        assert self.segment > 0
        return tw.datasets.VideoFolderEnhance(path=cfg.dataset_train,
                                              transform=self.transform_yuv_train,
                                              segment=self.segment)
      else:
        return tw.datasets.ImageFolderEnhance(path=cfg.dataset_train, transform=self.transform_yuv_train)

    elif phase == tw.phase.val and self.Master:
      return tw.datasets.ImageEnhance(path=cfg.dataset_val, transform=self.transform_yuv_val)

    raise NotImplementedError

  def _build_model(self):
    """build model
    """
    cfg = self.Config

    # different input format
    if self.Config.input_colorspace in ['Y']:
      in_channels, out_channels = 1, 1
    elif self.Config.input_colorspace in ['RGB', 'YUV']:
      in_channels, out_channels = 3, 3
    else:
      raise NotImplementedError

    # build generator
    if cfg.model_generator == 'MSRResNet':
      netG = vsr_models.MSRResNet(in_nc=in_channels, out_nc=out_channels, nf=64, nb=23, upscale=2)

    elif cfg.model_generator.startswith('RRDBNet'):
      setting = cfg.model_generator.split('.')
      if len(setting) > 1:
        nf, nb = int(setting[1]), int(setting[2])
      else:
        nf, nb = 64, 23
      netG = vsr_models.RRDBNet(in_nc=in_channels, out_nc=out_channels, nf=nf, nb=nb)

    elif cfg.model_generator.startswith('FENetWithWarp'):

      if cfg.model_encoder is None:
        warp_channels = in_channels  # output as input
        warp_scale = 2  # 2x super-resolution
      elif cfg.model_encoder == 'FENetWithMoco':
        warp_channels = 2  # warp channels is 2
        warp_scale = 1  # warp input h and w is identical with inputs
      else:
        raise NotImplementedError(cfg.model_encoder)

      setting = cfg.model_generator.split('.')
      blocks = [int(setting[1][1]), int(setting[1][2]), int(setting[1][3])]
      channels = int(setting[2].split('C')[1])
      netG = vsr_models.FENetWithWarp(in_channels=in_channels,
                                      out_channels=out_channels,
                                      channels=channels,
                                      num_blocks=blocks,
                                      block_type='residual',
                                      warp_scale=warp_scale,
                                      warp_channels=warp_channels)

    elif cfg.model_generator.startswith('FENet'):
      setting = cfg.model_generator.split('.')
      blocks = [int(setting[1][1]), int(setting[1][2]), int(setting[1][3])]
      channels = int(setting[2].split('C')[1])
      netG = vsr_models.FENetWithBranch(in_channels=in_channels,
                                        out_channels=out_channels,
                                        channels=channels,
                                        num_blocks=blocks,
                                        block_type='residual')

    elif cfg.model_generator == 'DASR':
      netG = vsr_models.DASR(in_channels=in_channels, out_channels=out_channels)

    else:
      raise NotImplementedError(cfg.model_generator)

    # build discriminator
    if cfg.model_discriminator == 'NLayerDiscriminator':
      netD = vsr_models.NLayerDiscriminator(in_nc=in_channels, nf=64, n_layers=3)
    elif cfg.model_discriminator == 'VGGStyleDiscriminator':
      netD = vsr_models.VGGStyleDiscriminator(num_in_ch=in_channels, num_feat=64, input_size=256)
    else:
      netD = None

    # build encoder
    if cfg.model_encoder == 'FENetWithMoco':
      channels = 32
      encoder = functools.partial(vsr_models.FENetEncoder, in_channels=in_channels, out_channels=channels)
      netE = vsr_models.FENetWithMoco(encoder=encoder, channels=channels)
    else:
      netE = None

    model = VsrModelWrapper(net_g=netG, net_d=netD, net_e=netE)
    model.to(cfg.device)

    return model

  def _build_optim(self, model: nn.Module):
    """build optimizer"""
    cfg = self.Config
    optim = {}

    if cfg.train_optimizer == 'adam':
      optim['G'] = torch.optim.Adam([{'params': model.netG.parameters(), 'lr': cfg.train_lr}])
      if model.netD is not None:
        optim['D'] = torch.optim.Adam([{'params': model.netD.parameters(), 'lr': cfg.train_lr}])
      if model.netE is not None:
        optim['E'] = torch.optim.Adam([{'params': model.netE.parameters(), 'lr': cfg.train_lr}])

    elif cfg.train_optimizer == 'sgd':
      optim['G'] = torch.optim.SGD([{'params': model.netG.parameters(), 'lr': cfg.train_lr, 'momentum': 0.9}])
      if model.netD is not None:
        optim['D'] = torch.optim.SGD([{'params': model.netD.parameters(), 'lr': cfg.train_lr, 'momentum': 0.9}])
      if model.netE is not None:
        optim['E'] = torch.optim.SGD([{'params': model.netE.parameters(), 'lr': cfg.train_lr, 'momentum': 0.9}])

    else:
      raise NotImplementedError(cfg.train_optimizer)

    return optim

  def _dump(self):
    """dump current checkpoint
    """
    cfg = self.Config
    path = f'{cfg.root}/model.epoch-{self.Epoch}.step-{self.Step}.pth'

    torch.save({
        'state_dict': self.Model.state_dict(),
        'global_step': self.Step,
        'global_epoch': self.Epoch,
        'optimizer': {k: v.state_dict() for k, v in self.Optim.items()}
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

      if cfg.task == 'train':
        for k in self.Optim:
          self.Optim[k].load_state_dict(ckpt['optimizer'][k])

      if 'global_step' in ckpt:
        self.Step = ckpt['global_step']

      if 'global_epoch' in ckpt:
        self.Epoch = ckpt['global_epoch']

    elif cfg.model_source == 'vanilla':
      tw.checkpoint.load_matched_state_dict(self.Model, ckpt['state_dict'])

    else:
      raise NotImplementedError(cfg.model_source)

  def _build_dataloader(self, phase: tw.phase, dataset):
    """ build data loader
    """
    cfg = self.Config

    if phase == tw.phase.train:
      return torch.utils.data.DataLoader(
          dataset=dataset,
          batch_size=cfg.train_batchsize,
          shuffle=True,
          num_workers=8,
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

    raise NotImplementedError

  @classmethod
  def tensor_fullrange_yuv_to_rgb(self, tensor, rgb_out=True):
    """require input tensor is [0, 1] and output [0, 1] rgb tensor
    """
    assert tensor.ndim in [3, 4], "require tensor with dim [n, c, h, w] or [c, h, w]"
    device = tensor.device
    t = tensor * 255.0 - torch.tensor([0, 128, 128]).view(1, 3, 1, 1).to(device)
    if t.ndim == 4:
      y, u, v = t[:, 0], t[:, 1], t[:, 2]
    elif t.ndim == 3:
      y, u, v = t[0], t[1], t[2]
    else:
      raise NotImplementedError
    r = y + 1.570 * v
    g = y - 0.187 * u - 0.467 * v
    b = y + 1.856 * u
    if rgb_out:
      return torch.stack([r, g, b], dim=1) / 255.0
    else:
      return torch.stack([b, g, r], dim=1) / 255.0

  @classmethod
  def resize(self, tensor, scale=0.5, mode='bilinear', align_corners=None):
    """resize wrapper for 3/5-d tensor
    """
    fn = functools.partial(torch.nn.functional.interpolate,
                           scale_factor=scale,
                           mode=mode,
                           align_corners=align_corners)

    assert isinstance(tensor, torch.Tensor)

    if scale == 1:
      return tensor

    if tensor.dim() == 5:
      # bs, c, f, h, w
      new_tensor = []
      for s in range(tensor.size(2)):
        new_tensor.append(fn(tensor[:, :, s, :, :]))
      new_tensor = torch.stack(new_tensor, dim=2)
      return new_tensor

    elif tensor.dim() == 4:
      # bs, c, h, w
      return fn(tensor)

    elif tensor.dim() == 3:
      # f, h, w
      return fn(tensor)

    else:
      raise NotImplementedError(tensor.dim())

  def _onnx(self, **kwargs):
    """export model to onnx
    """
    cfg = self.Config

    if cfg.input_colorspace in ['Y']:
      in_channels = 1
    else:
      in_channels = 3

    inputs = torch.rand(1, in_channels, 640, 360).to(cfg.device)
    tw.flops.register(self.Model.netG)
    with torch.no_grad():
      self.Model.netG(inputs)
    print(tw.flops.accumulate(self.Model.netG))
    tw.flops.unregister(self.Model.netG)

    tw.export.torch_to_onnx(self.Model.netG.eval(),
                            torch.rand(1, in_channels, 640, 360).to(cfg.device),
                            cfg.model_generator + '.onnx',
                            input_names=['input', ],
                            output_names=['output', ],
                            dynamic_axes={'input': {0: 'batch', 2: 'height', 3: 'width'}})

  def _tensorrt(self, **kwargs):
    """export to tensorrt models
    """
    cfg = self.Config

    if cfg.input_colorspace in ['Y']:
      in_channels = 1
    else:
      in_channels = 3

    tw.export.onnx_to_trt(
        cfg.model_generator + '.onnx',
        cfg.model_generator + '.engine',
        shapes={'input': {'min': (1, in_channels, 32, 32),
                          'best': (1, in_channels, 640, 360),
                          'max': (1, in_channels, 1024, 1024)}},
        verbose=True)

  def _inference(self, img_lr, **kwargs):
    img_hr = self.Model.netG(img_lr)
    img_hr = img_hr + self.resize(img_lr, scale=2.0)
    return img_hr

  def _test(self, **kwargs):
    """ test """
    cfg = self.Config
    # create folder for every epoch
    root = tw.fs.mkdirs(f'{cfg.root}/test/epoch_{self.Epoch}_step_{self.Step}/')
    # visualize
    self._viz(viz_output=root, viz_input=cfg.dataset_test)

  def _viz(self, **kwargs):
    """ visualize """
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

    # mkdir
    images, _ = tw.media.collect(viz_input)
    if not os.path.exists(viz_output):
      os.makedirs(viz_output)

    # set state
    self.Model.eval()

    # process images
    for filepath in tqdm.tqdm(sorted(images)):

      # convert image to tensor
      raw = cv2.imread(filepath)  # .astype('float')

      if cfg.input_colorspace == 'Y':

        # inference super resolution
        img = T.change_colorspace(raw, src=T.COLORSPACE.BGR, dst=T.COLORSPACE.BT709_VIDEORANGE)
        img = torch.from_numpy(img).float().to(device) / 255.0
        img = img.permute(2, 0, 1)  # [0, 1]
        img_lr = img[0].unsqueeze(0).unsqueeze(0)  # select Y channel

        # inference
        with torch.no_grad():
          img_hr = self._inference(img_lr)

        # fill-up YUV
        img_up = self.resize(img[None], scale=2.0)[0]
        img_up[0] = img_hr

        # to cpu
        img_up = img_up.permute(1, 2, 0).cpu().numpy()
        img_up = T.change_colorspace(img_up * 255.0, src=T.COLORSPACE.BT709_VIDEORANGE, dst=T.COLORSPACE.BGR)

      elif cfg.input_colorspace == 'YUV':

        # inference super resolution
        img = T.change_colorspace(raw, src=T.COLORSPACE.BGR, dst=T.COLORSPACE.BT709_VIDEORANGE)
        img = torch.from_numpy(img).float().to(device) / 255.0
        img = img.permute(2, 0, 1)  # [0, 1]
        img_lr = img.unsqueeze(0)
        img_420 = self.resize(self.resize(img_lr, scale=0.5, mode='nearest'), scale=2.0, mode='bilinear')
        img_lr[:, 1:] = img_lr[:, 1:]

        # inference
        with torch.no_grad():
          img_hr = self._inference(img_lr)[0]

        # to cpu
        img_up = img_hr.permute(1, 2, 0).cpu().numpy()
        img_up = T.change_colorspace(img_up * 255.0, src=T.COLORSPACE.BT709_VIDEORANGE, dst=T.COLORSPACE.BGR)

      elif cfg.model_colorpsace == 'RGB':

        img = cv2.cvtColor(raw, cv2.COLOR_BGR2RGB)
        img = torch.from_numpy(img).float().to(device) / 255.0
        img = img.permute(2, 0, 1)  # [0, 1]
        img_lr = img.unsqueeze(0)

        # inference
        with torch.no_grad():
          img_hr = self._inference(img_lr)[0]

        # to cpu
        img_hr = img_hr.permute(1, 2, 0).cpu().numpy()
        img_up = cv2.cvtColor(img_hr, cv2.COLOR_RGB2BGR)

      else:

        raise NotImplementedError(cfg.input_colorspace)

      render = img_up

      # save to file
      if os.path.isdir(viz_output):
        dst = os.path.join(viz_output, os.path.basename(filepath) + '.sr.png')
        cv2.imwrite(dst, render)
      else:
        cv2.imwrite(viz_output, render)

  def _val(self, **kwargs):
    """ validate after epoch
    """
    cfg = self.Config
    device = self.Config.device
    start_time = tw.timer.tic()
    total = 0

    # reset
    self.Model.eval()
    self.Evaluator.reset()

    # build dataloader
    if 'loader' in kwargs and kwargs['loader'] is not None:
      val_loader = kwargs['loader']
    else:
      val_loader = self._build_dataloader(tw.phase.val, self._build_dataset(tw.phase.val))

    # create folder for every epoch
    root = tw.fs.mkdirs(f'{cfg.root}/val/epoch_{self.Epoch}_step_{self.Step}/')

    # start
    with torch.no_grad():
      for samples in tqdm.tqdm(val_loader):
        total += len(samples)

        # convert data into tensor
        lr, hr, paths = [], [], []
        for sample in samples:
          if cfg.input_colorspace in ['RGB', 'YUV']:
            lr.append(sample[0].bin.float().to(device))
            hr.append(sample[1].bin.float().to(device))
          elif cfg.input_colorspace in ['Y']:
            lr.append(sample[0].bin[0][None].float().to(device))
            hr.append(sample[1].bin[0][None].float().to(device))
          else:
            raise NotImplementedError(cfg.input_colorspace)
          paths.append(sample[0].path[0])

        lr = torch.stack(lr, dim=0).float().to(device)
        hr = torch.stack(hr, dim=0).float().to(device)

        # inference
        hr_pred = self._inference(lr)

        # eval
        metrics = self.Evaluator.compute(hr_pred, hr, path=paths)
        self.Evaluator.append(metrics)

    # stat
    reports = self.Evaluator.accumulate()
    elapsed = tw.timer.duration(start_time, tw.timer.tic())
    throughput = tw.timer.throughput(elapsed, total)
    keys = list(reports.keys()) + ['time', 'throughtput']
    vals = list(reports.values()) + [elapsed, throughput]
    tw.runner.log(keys=keys, values=vals, step=self.Step, epoch=self.Epoch, tag='val', writer=self.Writer)

  @abc.abstractclassmethod
  def _train(self, **kwargs):
    raise NotImplementedError

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
        self._viz()

    elif cfg.task == 'onnx':
      with torch.no_grad():
        self._onnx()

    elif cfg.task == 'trt':
      with torch.no_grad():
        self._tensorrt()

    else:
      raise NotImplementedError(cfg.task)
