import torch
from piq import ssim, SSIMLoss

x = torch.rand(4, 3, 256, 256, requires_grad=True)
y = torch.rand(4, 3, 256, 256)

loss = SSIMLoss(data_range=1.)(x, y)
print(loss)
