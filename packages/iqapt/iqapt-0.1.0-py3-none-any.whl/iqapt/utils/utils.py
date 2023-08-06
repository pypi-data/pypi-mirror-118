import torch
import torch.nn as nn
import torch.nn.functional as F
import math
import iqapt.error as error
#from . import error as error


def check_img_size(img_a, img_b):
    if img_a.size() != img_b.size():
        return None
    else:
        return img_a.size()


def get_tensor_device(tensor):
    return tensor.device


def gaussian(window_size, sigma):
    gauss = torch.Tensor([
        math.exp(-(x - window_size // 2)**2 / float(2 * sigma**2))
        for x in range(window_size)
    ])
    return gauss / gauss.sum()


def gaussian_kernel(window_size, sigma):
    one_D_window = gaussian(window_size, sigma).unsqueeze(1)
    two_D_window = one_D_window.mm(one_D_window.t()).float()
    return two_D_window


def unfold_img(img, window_size):
    if len(img.size()) == 2:
        img = img.unsqueeze(0).unsqueeze(0)
    elif len(img.size()) == 3:
        img = img.unsqueeze(0)
    elif len(img.size()) == 4:
        img = img
    else:
        raise error.InputError('placeholder')

    N, C, H, W = img.size()
    unfold = torch.nn.Unfold(window_size)
    unfold_img = unfold(img)
    unfold_img = unfold_img.permute(0, 2, 1)
    unfold_img = unfold_img.reshape(N, -1, C, window_size, window_size)
    return unfold_img


def normalize_tensor(input_tensor, eps=0.1**10):
    tensor_dims = len(input_tensor.size())

    if tensor_dims == 4:
        start_dim = 1
    elif tensor_dims == 3 or tensor_dims == 2:
        start_dim = 0
    else:
        raise error.InputError(
            'the size of input_tensor should be N,C,H,W or C,H,W or H,W.')

    norm_factor = torch.sqrt(
        torch.sum(input_tensor**2,
                  dim=list(range(start_dim, tensor_dims)),
                  keepdim=True))
    return input_tensor / norm_factor


def spatial_average(input_tensor, keepdim=True):
    tensor_dims = len(input_tensor.size())

    if tensor_dims == 4:
        start_dim = 2
    elif tensor_dims == 3:
        start_dim = 1
    elif tensor_dims == 2:
        start_dim = 0
    else:
        raise error.InputError(
            'the size of input_tensor should be N,C,H,W or C,H,W or H,W.')

    return torch.mean(input_tensor,
                      dim=list(range(start_dim, tensor_dims)),
                      keepdim=keepdim)


def upsample(input_tensor, out_size, mode='bilinear'):
    tensor_dims = len(input_tensor.size())

    if tensor_dims == 2:
        input_tensor = torch.unsqueeze(input_tensor, 0)
    elif tensor_dims < 2:
        raise error.InputError(
            'the size of input_tensor should be N,C,H,W or C,H,W or H,W.')

    return F.upsample(input_tensor,
                      size=out_size,
                      mode=mode,
                      align_corners=False)
