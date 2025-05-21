from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load model once when the module is imported
model_name = "csebuetnlp/mT5_multilingual_XLSum"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def summarize_text(text):
    if not text.strip():
        return "Input text is empty."

    # Tokenize input
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=1024)
    
    # Generate summary
    summary_ids = model.generate(
        inputs.input_ids,
        max_length=150,
        min_length=40,
        num_beams=4,
        length_penalty=2.0,
        early_stopping=True
    )

    # Decode
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)
