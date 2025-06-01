import torch

class Chatbot:
    def __init__(self, model, tokenizer, device=None, max_length=128):
        self.model = model
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()

    def generate_response(self, input_text):
        # Tokenize input using tokenizer()
        encoded = self.tokenizer(
            input_text,
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=self.max_length
        )
        inputs = {k: v.to(self.device) for k, v in encoded.items()}

        with torch.no_grad():
            output_ids = self.model.generate(
                **inputs,
                max_length=self.max_length,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
                do_sample=True,
                top_k=50,
                top_p=0.95
            )

        response = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return response
