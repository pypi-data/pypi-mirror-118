

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def compute_index(predictions, labels):
  srocc = np.abs(stats.spearmanr(predictions, labels)[0])
  plcc = np.abs(np.corrcoef(predictions, labels)[0, 1])
  fit_func = np.polyfit(predictions, labels, deg=3)
  fit_pred = np.polyval(fit_func, predictions)
  plcc_fit = np.abs(np.corrcoef(fit_pred, labels)[0, 1])
  mae = np.mean(np.abs(predictions - labels))
  rmse = np.sqrt(np.mean((predictions - labels) ** 2))
  return fit_func, {'mae': mae, 'rmse': rmse, 'srocc': srocc, 'plcc_fit': plcc_fit, 'plcc': plcc},


def draw(src, dst):
  labels, preds = [], []
  with open(src) as fp:
    for line in fp:
      ref, distort, label, pred = line.replace('\n', '').split()
      labels.append(float(label))
      preds.append(float(pred))

  preds, labels = np.array(preds), np.array(labels)
  fit_func, index = compute_index(preds, labels)

  fit_preds = np.polyval(fit_func, preds)
  # fit_preds = np.polyval(fit_func, np.arange())

  fig = plt.figure()

  plt.scatter(preds, labels, c='g', alpha=0.5, s=10)
  plt.scatter(preds, fit_preds, c='b', alpha=0.5, s=2)

  plt.ylabel('labels')
  plt.xlabel('prediction')
  plt.grid()

  fig.suptitle('mae:{:.4f}, rmse:{:.4f}, srocc:{:.4f}, plcc_fit:{:.4f}, plcc:{:.4f}'.format(
      index['mae'], index['rmse'], index['srocc'], index['plcc_fit'], index['plcc']
  ))
  plt.savefig(dst)
  
  index['name'] = dst.split('/')[-1][:-4]
  return index

indexs = []
indexs.append(draw('_outputs/FRIQA.psnr.TID2013.210703183111.txt', '_outputs/FRIQA.psnr.TID2013.png'))
indexs.append(draw('_outputs/FRIQA.lpips.TID2013.210703183553.txt', '_outputs/FRIQA.lpips.TID2013.png'))
indexs.append(draw('_outputs/FRIQA.vsi.TID2013.210703183212.txt', '_outputs/FRIQA.vsi.TID2013.png'))
indexs.append(draw('_outputs/FRIQA.vifs.TID2013.210703183446.txt', '_outputs/FRIQA.vifs.TID2013.png'))
indexs.append(draw('_outputs/FRIQA.ms_ssim.TID2013.210703183048.txt', '_outputs/FRIQA.ms_ssim.TID2013.png'))
indexs.append(draw('_outputs/FRIQA.ssim.TID2013.210703183039.txt', '_outputs/FRIQA.ssim.TID2013.png'))
indexs.append(draw('_outputs/FRIQA.dists.TID2013.210703183658.txt', '_outputs/FRIQA.dists.TID2013.png'))
indexs.append(draw('_outputs/FRIQA.gmsd.TID2013.210703183132.txt', '_outputs/FRIQA.gmsd.TID2013.png'))
indexs.append(draw('_outputs/FRIQA.nlpd.TID2013.210703183157.txt', '_outputs/FRIQA.nlpd.TID2013.png'))
indexs.append(draw('_outputs/FRIQA.fsim.TID2013.210703183206.txt', '_outputs/FRIQA.fsim.TID2013.png'))
indexs.append(draw('_outputs/FRIQA.vif.TID2013.210703183221.txt', '_outputs/FRIQA.vif.TID2013.png'))
indexs.append(draw('_outputs/FRIQA.mad.TID2013.210703183519.txt', '_outputs/FRIQA.mad.TID2013.png'))


indexs.sort(key=lambda x: x['plcc'])

print('{:^25s}{:^10s}{:^10s}{:^10s}{:^10s}{:^10s}'.format('method', 'mae', 'rmse', 'srocc', 'plcc_fit', 'plcc'))
for index in indexs:
  print('{:^25s}{:^10.4f}{:^10.4f}{:^10.4f}{:^10.4f}{:^10.4f}'.format(
      index['name'], index['mae'], index['rmse'], index['srocc'], index['plcc_fit'], index['plcc']
  ))