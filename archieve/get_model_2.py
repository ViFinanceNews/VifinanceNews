import os
from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModel, pipeline
import torch

app = Flask(__name__)

# Define the root folder where the models are located
root_model_dir = "/app/models/hub"

# Function to search for a folder containing a model based on folder name
def find_model_folder(model_name):
    for root, dirs, files in os.walk(root_model_dir):
        # Check if 'config.json' exists (which indicates a valid Hugging Face model folder)
        if "config.json" in files and model_name in root:
            return root
    return None

# Search for the model folder (for example, 'multilingual-albert-base-cased-32k')
model_folder = find_model_folder("models--cservan--multilingual-albert-base-cased-32k")
sentiment_model_folder = find_model_folder("models--tabularisai--multilingual-sentiment-analysis")

if model_folder is None or sentiment_model_folder is None:
    raise Exception("Model folder(s) not found!")

# Load multilingual ALBERT model for embeddings from the found folder
albert_tokenizer = AutoTokenizer.from_pretrained(model_folder)
albert_model = AutoModel.from_pretrained(model_folder)

# Load sentiment analysis model from the found folder
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model=sentiment_model_folder,
    tokenizer=sentiment_model_folder,
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