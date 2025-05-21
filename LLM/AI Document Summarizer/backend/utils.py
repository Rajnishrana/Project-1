from flask import Flask, request, jsonify
from summarizer import summarize_text  # this works if summarizer.py is in same folder

app = Flask(__name__)

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    input_text = data.get("text", "")

    if not input_text.strip():
        return jsonify({"error": "Text is required"}), 400

    summary = summarize_text(input_text)
    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(debug=True)
