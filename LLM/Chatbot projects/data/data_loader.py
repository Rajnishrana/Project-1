import random
from torch.utils.data import DataLoader
from .chat_dataset import ChatDataset

def get_dataloader(texts, tokenizer, batch_size=32, max_length=128, shuffle=True):
    dataset = ChatDataset(texts, tokenizer, max_length=max_length)
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)

def split_dataset(texts, train_ratio=0.8, val_ratio=0.1, seed=42):
    random.seed(seed)
    random.shuffle(texts)
    total = len(texts)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)
    train_texts = texts[:train_end]
    val_texts = texts[train_end:val_end]
    test_texts = texts[val_end:]
    return train_texts, val_texts, test_texts

def get_datasets_from_processed_file(processed_path, tokenizer, config):
    with open(processed_path, 'r', encoding='utf-8') as f:
        texts = [line.strip() for line in f if line.strip()]  # Remove empty lines

    data_config = config["data"]
    max_samples = data_config.get("max_samples")
    if max_samples is not None:
        texts = texts[:max_samples]

    train_ratio = data_config.get("train_split", 0.8)
    val_ratio = data_config.get("val_split", 0.1)
    seed = config.get("logging", {}).get("seed", 42)
    batch_size = config["training"].get("batch_size", 32)
    max_length = data_config.get("max_length", 128)

    train_texts, val_texts, test_texts = split_dataset(texts, train_ratio, val_ratio, seed)

    train_loader = get_dataloader(train_texts, tokenizer, batch_size, max_length, shuffle=True)
    val_loader = get_dataloader(val_texts, tokenizer, batch_size, max_length, shuffle=False)
    test_loader = get_dataloader(test_texts, tokenizer, batch_size, max_length, shuffle=False)

    return train_loader, val_loader, test_loader

print("data_loader.py loaded successfully")
