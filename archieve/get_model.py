from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModel, pipeline
import torch
import os

app = Flask(__name__)

# Set the Hugging Face cache directory to the mounted volume path
# This will tell Hugging Face to use the volume for caching
os.environ["HF_HOME"] = "/app/models"  # The volume mounted at /app/models

# Load multilingual ALBERT model for embeddings from the cached volume
albert_tokenizer = AutoTokenizer.from_pretrained("cservan/multilingual-albert-base-cased-32k")
albert_model = AutoModel.from_pretrained("cservan/multilingual-albert-base-cased-32k")

# Load sentiment analysis model from the cached volume
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="tabularisai/multilingual-sentiment-analysis",
    tokenizer="tabularisai/multilingual-sentiment-analysis",
    device=0 if torch.cuda.is_available() else -1
)

@app.route('/analyze-sentiment', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = sentiment_pipeline(text)
    return jsonify({"result": result})

@app.route('/get-embedding', methods=['POST'])
def get_embedding():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    inputs = albert_tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        outputs = albert_model(**inputs)
        # Get the last hidden state for CLS token
        cls_embedding = outputs.last_hidden_state[:, 0, :].squeeze().tolist()

    return jsonify({"embedding": cls_embedding})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6000, debug=True)