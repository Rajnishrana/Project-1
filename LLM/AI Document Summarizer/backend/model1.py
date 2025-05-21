# backend/model.py

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

class LLMWrapper:
    def __init__(self, model_name="meta-llama/Llama-3-8B-Instruct"):
        print("Loading model...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype="auto")
        self.pipe = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)

    def generate_response(self, prompt, max_tokens=300):
        result = self.pipe(prompt, max_new_tokens=max_tokens, do_sample=True, temperature=0.7)
        return result[0]['generated_text']
