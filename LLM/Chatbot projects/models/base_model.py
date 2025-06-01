import torch.nn as nn
from abc import ABC, abstractmethod

class BaseChatbotModel(nn.Module, ABC):
    def __init__(self):
        super(BaseChatbotModel, self).__init__()

    @abstractmethod
    def forward(self, *inputs):
        pass

    @abstractmethod
    def generate_response(self, input_text, max_length=100, device=None):
        pass
