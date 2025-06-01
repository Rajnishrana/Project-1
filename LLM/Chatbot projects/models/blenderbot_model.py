import torch
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
from base_chatbot_model import BaseChatbotModel

class BlenderBotModel(BaseChatbotModel):
    def __init__(self, model_name="facebook/blenderbot-400M-distill"):
        super(BlenderBotModel, self).__init__()
        self.tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
        self.model = BlenderbotForConditionalGeneration.from_pretrained(model_name)

    def forward(self, input_ids, attention_mask=None, labels=None):
        return self.model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)

    def generate_response(self, input_text, max_length=100, device=None):
        device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(device)
        inputs = self.tokenizer([input_text], return_tensors="pt", padding=True, truncation=True).to(device)
        with torch.no_grad():
            reply_ids = self.model.generate(**inputs, max_length=max_length)
        return self.tokenizer.decode(reply_ids[0], skip_special_tokens=True)
