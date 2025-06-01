from sklearn.metrics import accuracy_score, f1_score
from nltk.translate.bleu_score import sentence_bleu

def compute_metrics(predictions, references):
    bleu_scores = [sentence_bleu([ref.split()], pred.split()) for pred, ref in zip(predictions, references)]
    avg_bleu = sum(bleu_scores) / len(bleu_scores) if bleu_scores else 0

    # Note: accuracy/f1 are only valid for classification, not generation
    return {
        "BLEU": round(avg_bleu, 4),
    }
