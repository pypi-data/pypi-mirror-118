import torch
from abc import ABC, abstractclassmethod
from . import utils
from . import error


class Metric(ABC):
    def __init__(self) -> None:
        super().__init__()

    def __call__(self, input_a, input_b):
        input_size = utils.check_img_size(input_a, input_b)

        if input_size != None:
            if len(input_size) == 4:
                N, C, H, W = input_size
                results = [None] * N
                paired_img_set = [
                    (index, img_a, img_b)
                    for index, (img_a,
                                img_b) in enumerate(zip(input_a, input_b))
                ]

                # TODO: optimized by multithreads
                for n in range(N):
                    index, img_a, img_b = paired_img_set[n]
                    results[index] = self.calc(img_a, img_b)
            elif len(input_size) == 3:
                C, H, W = input_size
                results = [None]
                img_a, img_b = input_a, input_b
                results[0] = self.calc(img_a, img_b)
            elif len(input_size) == 2:
                H, W = input_size
                img_a, img_b = torch.unsqueeze(input_a,
                                               0), torch.unsqueeze(input_b, 0)
                results = [None]
                results[0] = self.calc(img_a, img_b)
            else:
                raise error.InputError(
                    'the size of input_a or input_b should be N,C,H,W or C,H,W or H,W.'
                )
        else:
            raise error.VaildError(
                'the size of input_a and input_b should be the same.')

        return torch.stack(results)

    @abstractclassmethod
    def calc(self, img_a: torch.Tensor, img_b: torch.Tensor):
        '''
        implemented by sub class
        '''
