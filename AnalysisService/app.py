import sys
import os
import requests
import flask
import redis
from ViFinanceCrawLib.QualAna.QualAna import QualAnaIns
from ViFinanceCrawLib.QuantAna.QuantAna_albert import QuantAnaInsAlbert
from VifinanceNews.LoggingService.app import log_event
from flask import request, jsonify
import urllib.parse # for decoding
import os
import json
from flask_cors import CORS

service_name = "AnalysisService"

app = flask.Flask(__name__)
quant_analyzer = QuantAnaInsAlbert()
qual_analyzer = QualAnaIns()
redis_cache = redis.Redis(
    host = os.getenv("REDIS_HOST"),
    port = os.getenv("REDIS_PORT"),
    password = os.getenv("REDIS_PASSWORD"),
    ssl =True
)

CORS(app, supports_credentials=True, origins=["*"])
print("Analysis Started")

@app.route('/api/factcheck/', methods=['POST'])
@log_event(service_name, event_base="FactCheck")
def fact_check():
    try:
        data = request.get_json(silent=True)  # Receive JSON payload
        if not isinstance(data, dict) or "url" not in data:
            return jsonify({'error': 'Invalid request format. Expected JSON with a "url" key.'}), 400

        url = data["url"]  # Extract URL
        redis_article = redis_cache.get(url)

        if redis_article:
            redis_article = json.loads(redis_article)  # Convert from JSON string to dict
            fact_check = qual_analyzer.fact_check(redis_article)
            print("check fact-check in app.py")
            decoded_str = fact_check.strip().strip('"')
            json_data = json.loads(decoded_str)
            return jsonify({"fact-check":json_data})
        else:
            return jsonify({'error': 'Article not found in cache'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return proper error message
    
@app.route('/api/biascheck/', methods=['POST'])
@log_event(service_name, event_base="BiasCheck")
def bias_check():
    try:
        data = request.get_json(silent=True)  # Receive JSON payload
        if not isinstance(data, dict) or "url" not in data:
            return jsonify({'error': 'Invalid request format. Expected JSON with a "url" key.'}), 400

        url = data["url"]  # Extract URL
        redis_article = redis_cache.get(url)
        
        if redis_article:
            redis_article = json.loads(redis_article)  # Convert from JSON string to dict
            bias_analysis = qual_analyzer.bias_analysis(str({"title": redis_article["title"], "main_text": redis_article["main_text"]}))
            print("Check bias in app.py")
            decoded_str = bias_analysis.strip().strip('"')
            json_data = json.loads(decoded_str)
        
            return jsonify({"bias-check":json_data})
        else:
            return jsonify({'error': 'Article not found in cache'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return proper error message

@app.route('/api/sentiment_analysis/', methods=['POST'])
@log_event(service_name, event_base="SentimentAnalysis")
def sentiment_analysis():
    try:
        data = request.get_json(silent=True)  # Receive JSON payload
        if not isinstance(data, dict) or "url" not in data:
            return jsonify({'error': 'Invalid request format. Expected JSON with a "url" key.'}), 400

        url = data["url"]  # Extract URL
        redis_article = redis_cache.get(url)
        
        if redis_article:
            redis_article = json.loads(redis_article)  # Convert from JSON string to dict
            shorten_text = quant_analyzer.generative_extractive(redis_article["main_text"])
            sentiment_analysis = quant_analyzer.sentiment_analysis(shorten_text)
            print("Check sentiment in app.py")
            print(type(sentiment_analysis))
            return jsonify({"sentiment_analysis":sentiment_analysis})
        else:
            return jsonify({'error': 'Article not found in cache'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return proper error message

@app.route('/api/toxicity_analysis/',  methods=['POST'])
@log_event(service_name, event_base="ToxicityAnalysis")
def toxicity_analysis():
    try:
        data = request.get_json(silent=True)  # Receive JSON payload
        if not isinstance(data, dict) or "url" not in data:
            return jsonify({'error': 'Invalid request format. Expected JSON with a "url" key.'}), 400

        url = data["url"]  # Extract URL
        redis_article = redis_cache.get(url)
        
        if redis_article:
            redis_article = json.loads(redis_article)  # Convert from JSON string to dict
            shorten_text = quant_analyzer.generative_extractive(redis_article["main_text"])
            toxicity_analysis_analysis = quant_analyzer.detect_toxicity(shorten_text)
        
            return jsonify({"toxicity_analysis":toxicity_analysis_analysis})
        else:
            return jsonify({'error': 'Article not found in cache'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Return proper error message
