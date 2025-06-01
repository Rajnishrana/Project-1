# Conversational Chatbot (Cornell Movie Dialog Corpus)

This is a simple chatbot built using PyTorch and HuggingFace Transformers.

---

## 📁 Project Structure

├── data/ # Raw and processed data
├── models/ # Trained model checkpoints
├── inference/ # Inference classes and CLI
├── scripts/ # Dataset download and preprocessing
├── utils/ # Configs, tokenizers, helpers
├── configs/ # YAML config files
├── main.py # Main entry point
├── requirements.txt # Python dependencies
└── README.md # Project overview


---

## 🚀 Quickstart

### 1. Install Requirements
```bash
pip install -r requirements.txt
python scripts/download_dataset.py
python scripts/preprocess_data.py
python main.py --mode train
python main.py --mode chat

Configuration
All training and model parameters are defined in YAML files inside configs/.