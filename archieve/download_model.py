from transformers import (
    AutoTokenizer, AutoModel,
    AutoModelForSequenceClassification, pipeline
)
import os

def download_model(model_path, model_name, model_type="default"):
    """Download and save a Hugging Face model and tokenizer"""
    os.makedirs(model_path, exist_ok=True)

    # Ensure HF cache goes to the right folder
    os.environ["HF_HOME"] = os.environ.get("HF_HOME", "/app/hf_cache")

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Check if it's a sequence classification model or a pipeline-only model
    if model_type == "sequence_classification":
        try:
            # Try loading the model as AutoModelForSequenceClassification
            model = AutoModelForSequenceClassification.from_pretrained(model_name)
        except OSError:
            # If model is not available as a PyTorch model, handle it for pipeline (e.g., sentiment-analysis)
            print(f"Model {model_name} is not available for direct classification, using pipeline.")
            model = None  # Don't load the model explicitly, let the pipeline handle it
    else:
        model = AutoModel.from_pretrained(model_name)

    # Save tokenizer and model if it's a valid model (for non-pipeline models)
    if model:
        tokenizer.save_pretrained(model_path)
        model.save_pretrained(model_path)
    else:
        # For pipeline models, we just need to save the tokenizer since the model is handled by pipeline.
        tokenizer.save_pretrained(model_path)

# Download both models
download_model("models/albert", "cservan/multilingual-albert-base-cased-32k")
download_model("models/sentiment", "tabularisai/multilingual-sentiment-analysis", model_type="sequence_classification")