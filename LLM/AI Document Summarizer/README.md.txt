# AI Document Summarizer

## Overview

This project is a full-stack AI application designed to automate the analysis of text documents by extracting key insights and generating summaries. Users can upload or paste UTF-8 encoded text documents and interact with the system using natural language queries. The backend runs a transformer-based large language model wrapped in a Flask API, while the frontend is built using React.js.

The system supports chat history, clear error handling, and does not require environment variables or config files for API keys, as keys can be input via the UI if necessary.

---

## Features

- Upload or paste UTF-8 encoded text documents  
- Interact with the system via natural language queries, e.g.,  
  "Can you summarize what dropout is and how it is used in deep learning?"  
- View chat history of user prompts and AI-generated responses  
- Clear UI error notifications without crashing  
- API key input via UI (no environment variables or config files required)  

---

## Models Used

- Default model: distilgpt2 (a lightweight, CPU-friendly transformer model from Hugging Face)  
  - Suitable for CPU or low-spec GPUs  
  - Limited capabilities but efficient for this prototype  
- Optional model (not included in this submission): meta-llama/Llama-3-8B-Instruct  
  - Requires a GPU with at least 16GB VRAM and multiple CPU cores  
  - More powerful but resource intensive  

---

## Technology Stack

- Frontend: React.js (built with Vite, served as static files by Flask)  
- Backend: Flask API wrapping transformer models  
- Machine Learning / NLP:  
  - Transformers library (Hugging Face)  
  - PyTorch  
  - Huggingface Hub for model management  
- Containerization: Docker for environment consistency and easy deployment  
- Testing: pytest for unit and integration tests  
- Package Management: pip for Python dependencies, npm/yarn for JavaScript dependencies  
- API Design: RESTful API architecture  

---

## Hardware / Performance Notes

- Default setup uses distilgpt2 to meet constraints of CPU and memory resources.  
- p95 latency target for query response: 3 seconds from user query to first word of response.  
- p99 hardware specs for optional models: 16 GB RAM, 16 GB VRAM, 4 CPU cores.  
- The application notifies users clearly if internet connection is unavailable, as some model downloads may require connectivity.  

---

## Running the Application

To build and run the application using Docker:














