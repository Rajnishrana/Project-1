import torch
from torch.utils.data import Dataset
from transformers import PreTrainedTokenizer  # For type hinting

class ChatDataset(Dataset):
    def __init__(
        self, 
        texts: list[str], 
        tokenizer: PreTrainedTokenizer, 
        max_length: int = 128
    ):
        self.texts = texts
        self.tokenizer = tokenizer
        self.max_length = max_length

        # Ensure pad_token and pad_token_id are set
        if self.tokenizer.pad_token_id is None:
            if self.tokenizer.eos_token_id is not None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
            else:
                raise ValueError("Tokenizer has no pad_token_id or eos_token_id defined.")

    def __len__(self) -> int:
        return len(self.texts)

    def __getitem__(self, idx: int) -> dict[str, torch.Tensor]:
        text = self.texts[idx]
        encoded = self.tokenizer(
            text,
            padding='max_length',
            truncation=True,
            max_length=self.max_length,
            return_tensors='pt'
        )
        input_ids = encoded['input_ids'].squeeze(0)          # Shape: (max_length,)
        attention_mask = encoded['attention_mask'].squeeze(0) # Shape: (max_length,)
        
        labels = input_ids.clone()
        # Mask padding tokens with -100 so loss ignores them
        labels[labels == self.tokenizer.pad_token_id] = -100

        return {
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'labels': labels,
        }
