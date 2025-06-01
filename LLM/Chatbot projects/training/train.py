import time
import torch
from torch.optim import AdamW
from training.loss_functions import get_loss_function
from training.evaluate import evaluate_model


def train_model(model, train_loader, val_loader=None, test_loader=None, tokenizer=None, config=None):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    model = model.to(device)

    training_config = config.get('training', {})
    epochs = training_config.get('epochs', 5)
    learning_rate = training_config.get('learning_rate', 5e-5)
    loss_function_name = training_config.get('loss_type', 'cross_entropy')

    print(f"Training configuration: epochs={epochs}, learning_rate={learning_rate}, loss_function={loss_function_name}")

    optimizer = AdamW(model.parameters(), lr=learning_rate)
    loss_fn = get_loss_function(loss_function_name)

    for epoch in range(epochs):
        model.train()
        total_loss = 0
        start_time = time.time()

        for batch in train_loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)

            if hasattr(outputs, "loss") and outputs.loss is not None:
                loss = outputs.loss
            else:
                logits = outputs.logits if hasattr(outputs, "logits") else outputs[0]
                loss = loss_fn(logits, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        avg_train_loss = total_loss / len(train_loader)
        epoch_time = time.time() - start_time

        # Validation evaluation and metrics printing
        if val_loader is not None and tokenizer is not None:
            metrics = evaluate_model(model, val_loader, tokenizer, config, split_name="Validation")
            # Assuming evaluate_model returns a dict with these keys:
            val_loss = metrics.get('loss', float('nan'))
            val_ppl = metrics.get('perplexity', float('nan'))
            val_bleu = metrics.get('bleu', float('nan'))
            val_rouge1 = metrics.get('rouge-1', float('nan'))
            val_rouge2 = metrics.get('rouge-2', float('nan'))
            val_rougel = metrics.get('rouge-l', float('nan'))
            val_meteor = metrics.get('meteor', float('nan'))

            print(
                f"Epoch {epoch + 1}/{epochs} - "
                f"Train Loss: {avg_train_loss:.4f} | "
                f"Val Loss: {val_loss:.4f} | Val PPL: {val_ppl:.4f} | Val BLEU: {val_bleu:.4f} | "
                f"Val ROUGE-1: {val_rouge1:.4f} | Val ROUGE-2: {val_rouge2:.4f} | Val ROUGE-L: {val_rougel:.4f} | "
                f"Val METEOR: {val_meteor:.4f} | "
                f"Time: {epoch_time:.2f}s"
            )
        else:
            print(f"Epoch {epoch + 1}/{epochs} - Train Loss: {avg_train_loss:.4f} | Time: {epoch_time:.2f}s")

    # Final test evaluation
    if test_loader is not None and tokenizer is not None:
        print("\nStarting evaluation on Test set...")
        evaluate_model(model, test_loader, tokenizer, config, split_name="Test")


def train(config):
    from transformers import AutoModelForCausalLM
    from utils.tokenizer_utils import ChatTokenizer
    from data.data_loader import get_datasets_from_processed_file

    print("Training process started")

    # Initialize tokenizer
    tokenizer = ChatTokenizer(
        config['tokenizer']['model_name'],
        max_length=config['tokenizer'].get('max_length', 128)
    )
    print("Tokenizer initialized")

    # Load processed data
    processed_path = config['data'].get('processed_data_path')
    if not processed_path:
        raise ValueError("Config must include 'data.processed_data_path' to split and load the dataset.")
    print(f"Using processed data path: {processed_path}")

    train_loader, val_loader, test_loader = get_datasets_from_processed_file(processed_path, tokenizer, config)
    print(f"Data loaders ready. Train batches: {len(train_loader)}, Validation batches: {len(val_loader)}, Test batches: {len(test_loader)}")

    # Load model
    model_name = config['model']['name']
    print(f"Loading model: {model_name}")
    model = AutoModelForCausalLM.from_pretrained(model_name)
    print("Model loaded")

    # Train and evaluate
    train_model(model, train_loader, val_loader, test_loader, tokenizer, config)
    print("Training process completed")
