

import torch
from torch.utils.data import DataLoader

import tw


class Dataset(torch.utils.data.Dataset):

  def __init__(self):
    super(Dataset, self).__init__()
    self.targets = [0, 0, 0, 0]

  def __len__(self):
    return len(self.targets)
  
  def batch(self):
    for i in range(4):
      self.targets[i] += 1

  def __getitem__(self, idx):
    self.targets[idx] += 1
    print('in getitem', self.targets[idx], self.targets)
    return self.targets[idx]


if __name__ == "__main__":
  
  """pay attention num_wokers will result dataset copy.
  """
  dataset = Dataset()
  print('before', dataset.targets)
  
  loader = DataLoader(dataset,
                      batch_size=1,
                      shuffle=False,
                      sampler=None,
                      num_workers=1)
  
  for i in range(3):
    for sample in loader:
      # print(sample)
      pass
    dataset.batch()
    print('after', i, dataset.targets)
