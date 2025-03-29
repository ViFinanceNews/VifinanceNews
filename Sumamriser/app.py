import sys
import os
import requests
import flask
from ViFinanceCrawLib.Summarizer.Summarizer import Summarizer
from flask import request, jsonify

BASE_URL  = "http://127.0.0.1.5001"
summarizer = Summarizer()

app = flask.Flask(__name__)

@app.route("/summarize", methods=['POST'])
def summarize_article():
    data = request.get_json()
    if not isinstance(data, list) or not all(isinstance(item, dict) and "main_text" in item for item in data):
        return jsonify({"error": "Invalid input: Expected a list of dicts with 'text' key"}), 400
    
    return

@app.route("/synthesis", methods=['POST'])
def synthesis_articles():
    data = request.get_json()
    if not isinstance(data, list) or not all(
        isinstance(item, dict) and 
        all(key in item for key in ["title", "main_text", "url", "authors", "date_publish"]) for item in data
        ):
        return jsonify({"error": "Invalid input: Expected a list of dicts with keys: 'title', 'main_text', 'url', 'authors', 'date_publish'"}), 400
    return
