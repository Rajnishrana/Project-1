from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from backend.model import LLMWrapper
import os

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')
CORS(app)

llm = LLMWrapper()

@app.route('/api/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json(force=True)  # force=True ensures JSON parsing
    except Exception:
        return jsonify({'error': 'Invalid JSON format'}), 400

    context = data.get('context', '')
    question = data.get('question', '')

    if not question.strip():
        return jsonify({'error': 'Missing or empty question'}), 400

    prompt = f"{context}\n\nQuestion: {question}\nAnswer:"

    try:
        answer = llm.generate_response(prompt)
    except Exception as e:
        # Log the error on the backend if you have logging (optional)
        return jsonify({'error': f"Model error: {str(e)}"}), 500

    if not answer:
        return jsonify({'error': 'Model returned empty response'}), 500

    return jsonify({'answer': answer})

@app.route('/')
def index():
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except Exception:
        return "Index page not found.", 404

@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory(app.static_folder, path)
    except Exception:
        return "Resource not found.", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
