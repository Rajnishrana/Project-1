import torch
from tqdm import tqdm
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.translate.meteor_score import meteor_score
from rouge_score import rouge_scorer
import math
import nltk

nltk.download('wordnet')
nltk.download('punkt')

def perplexity(loss):
    """Convert cross-entropy loss to perplexity."""
    return math.exp(loss) if loss < 100 else float('inf')  # Avoid overflow

def evaluate_model(model, val_loader, tokenizer, config, split_name="Validation", show_progress=True):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.eval()

    # print(f"Starting evaluation on {split_name} set...")

    loss_fn = torch.nn.CrossEntropyLoss(ignore_index=tokenizer.pad_token_id)
    total_loss = 0.0
    total_samples = 0

    total_bleu = 0.0
    total_rouge_1 = 0.0
    total_rouge_2 = 0.0
    total_rouge_l = 0.0
    total_meteor = 0.0

    rouge = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    smoothing = SmoothingFunction().method1

    gen_kwargs = {
        "num_beams": config.get('generation', {}).get('num_beams', 1),
        "no_repeat_ngram_size": config.get('generation', {}).get('no_repeat_ngram_size', 2),
        "pad_token_id": tokenizer.pad_token_id,
    }
    # Use max_new_tokens if available, else max_length
    if 'max_new_tokens' in config.get('generation', {}):
        gen_kwargs["max_new_tokens"] = config['generation']['max_new_tokens']
    else:
        gen_kwargs["max_length"] = config.get('generation', {}).get('max_length', 50)

    with torch.no_grad():
        iterator = tqdm(val_loader, desc=f"Evaluating {split_name}") if show_progress else val_loader
        for batch in iterator:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            batch_size = input_ids.size(0)

            total_loss += loss.item() * batch_size  # accumulate total loss weighted by batch size
            total_samples += batch_size

            generated_ids = model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                **gen_kwargs
            )

            preds = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)

            # Fix labels for decoding: replace -100 with pad_token_id
            labels_cpu = labels.detach().cpu().clone().numpy()
            labels_cpu[labels_cpu == -100] = tokenizer.pad_token_id
            refs = tokenizer.batch_decode(labels_cpu, skip_special_tokens=True)

            for pred, ref in zip(preds, refs):
                pred_tokens = pred.split()
                ref_tokens = [ref.split()]

                # Compute BLEU with smoothing
                bleu = sentence_bleu(ref_tokens, pred_tokens, smoothing_function=smoothing)
                total_bleu += bleu

                rouge_scores = rouge.score(ref, pred)
                total_rouge_1 += rouge_scores['rouge1'].fmeasure
                total_rouge_2 += rouge_scores['rouge2'].fmeasure
                total_rouge_l += rouge_scores['rougeL'].fmeasure

                meteor = meteor_score([ref_tokens[0]], pred_tokens)
                total_meteor += meteor

    if total_samples == 0:
        print(f"No samples found in {split_name} set!")
        return None

    avg_loss = total_loss / total_samples
    avg_perplexity = perplexity(avg_loss)

    avg_bleu = total_bleu / total_samples
    avg_rouge_1 = total_rouge_1 / total_samples
    avg_rouge_2 = total_rouge_2 / total_samples
    avg_rouge_l = total_rouge_l / total_samples
    avg_meteor = total_meteor / total_samples

    print(
        f"{split_name} Loss: {avg_loss:.4f} | "
        f"{split_name} Perplexity: {avg_perplexity:.4f} | "
        f"{split_name} BLEU: {avg_bleu:.4f} | "
        f"{split_name} ROUGE-1: {avg_rouge_1:.4f} | "
        f"{split_name} ROUGE-2: {avg_rouge_2:.4f} | "
        f"{split_name} ROUGE-L: {avg_rouge_l:.4f} | "
        f"{split_name} METEOR: {avg_meteor:.4f}"
    )

    return {
        "loss": avg_loss,
        "perplexity": avg_perplexity,
        "bleu": avg_bleu,
        "rouge1": avg_rouge_1,
        "rouge2": avg_rouge_2,
        "rougeL": avg_rouge_l,
        "meteor": avg_meteor
    }
