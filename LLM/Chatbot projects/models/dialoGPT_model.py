import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from .base_model import BaseChatbotModel

class DialoGPTModel(BaseChatbotModel):
    def __init__(self, config):
        super(DialoGPTModel, self).__init__()
        model_name = config['model']['name']
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

    def forward(self, input_ids, attention_mask=None):
        return self.model(input_ids=input_ids, attention_mask=attention_mask)

    def generate_response(self, input_text, max_length=100, device=None):
        device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(device)
        encoded = self.tokenizer(
            input_text + self.tokenizer.eos_token,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=max_length
        )
        inputs = {k: v.to(device) for k, v in encoded.items()}
        with torch.no_grad():
            output_ids = self.model.generate(
                **inputs,
                max_length=max_length,
                pad_token_id=self.tokenizer.eos_token_id
            )
        return self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
