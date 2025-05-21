from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

class LLMWrapper:
    def __init__(self, model_name="distilgpt2"):
        print("Loading model...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.pipe = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)

    def generate_response(self, prompt, max_tokens=100):
        result = self.pipe(prompt, max_new_tokens=max_tokens, do_sample=True, temperature=0.7)
        generated_text = result[0]['generated_text']

        # Post-processing to clean repeated 'Answer:' or extra text
        if "Answer:" in generated_text:
            answer = generated_text.split("Answer:")[1].strip()
        else:
            answer = generated_text.strip()

        # Optionally stop at first newline to avoid long repeated text
        answer = answer.split('\n')[0]

        return answer
