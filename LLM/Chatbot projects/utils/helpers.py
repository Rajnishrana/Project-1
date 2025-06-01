import random
import numpy as np
import torch
import logging
import os

def set_seed(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

def setup_logging(log_path=None, level=logging.INFO):
    log_format = "%(asctime)s — %(levelname)s — %(message)s"
    logging.basicConfig(
        filename=log_path if log_path else None,
        level=level,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
