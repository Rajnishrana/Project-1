from transformers import AutoTokenizer

class ChatTokenizer:
    def __init__(self, model_name="microsoft/DialoGPT-small", max_length=128):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Set pad_token if not set
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = "left"
        self.max_length = max_length

    def __call__(self, text, return_tensors=None, **kwargs):
        padding = kwargs.pop('padding', "max_length")
        truncation = kwargs.pop('truncation', True)
        max_length = kwargs.pop('max_length', self.max_length)

        return self.tokenizer(
            text,
            padding=padding,
            truncation=truncation,
            max_length=max_length,
            return_tensors=return_tensors,
            **kwargs
        )

    def encode(self, text, return_tensors="pt", **kwargs):
        return self.tokenizer(
            text,
            return_tensors=return_tensors,
            padding="max_length",
            truncation=True,
            max_length=self.max_length,
            **kwargs
        )

    def decode(self, token_ids, skip_special_tokens=True):
        return self.tokenizer.decode(token_ids, skip_special_tokens=skip_special_tokens)

    def save_pretrained(self, path):
        self.tokenizer.save_pretrained(path)
        
    def __getattr__(self, name):
        # Forward attribute access to the inner tokenizer
        return getattr(self.tokenizer, name)
