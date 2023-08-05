
import torch
import tw
from torch import nn


class PSNR(nn.Module):

  def __init__(self):
    super().__init__()
    

  def forward(self, x, y, as_loss=True):
    """PSNR Index.
    
      PSNR = 10 * log10(MAX^2/MSE)

    Args:
        x ([type]): [torch.Tensor[N, C, H, W]]
        y ([type]): [torch.Tensor[N, C, H, W]]
        as_loss (bool, optional): Defaults to True.

    Returns:
        [torch.Tensor]: [N]
    """
    mse = ((x - y) ** 2).mean(dim=[1, 2, 3])
    return 10 * torch.log10(1.0 * 1.0 / mse)
