import torch
import numpy as np
import random


def seed(seed_nr=420):
    torch.manual_seed(seed_nr)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    np.random.seed(seed_nr)
    random.seed(seed_nr)
