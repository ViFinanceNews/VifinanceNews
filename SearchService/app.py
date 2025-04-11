import sys
import os
import requests
import json
import flask
import urllib.parse
from ViFinanceCrawLib.article_database.ScrapeAndTagArticles import ScrapeAndTagArticles
from flask import request, jsonify
from urllib.parse import unquote, unquote_plus
import hashlib

app = flask.Flask(__name__)

scrapped_url = []


@app.route("/get_cached_result/<string:user_query>", methods=['GET'])
def get_articles(user_query):
    user_query = unquote_plus(user_query)
    if not user_query:
        return jsonify({"error": "Invalid input"}), 400

    processor = ScrapeAndTagArticles()
    
    try:
        scraped_data = processor.search_and_scrape(user_query)
        if not scraped_data:
            return jsonify({"error": "No results found"}), 404  # Return 404 if no data found
        
        # print("Scraped URLs:", scraped_data)  # Debugging info
        processor.move_query(1, hashlib.md5(user_query.encode()).hexdigest())
        return jsonify({"message": "success", "data": scraped_data}), 200
    
    except Exception as e:
        print(f"Error: {e}")  # Debugging
        return jsonify({"error": "Internal Server Error"}), 500

# If user favorites the article, move it from Redis to the database using its URL as key

@app.route('/save', methods=['POST'])
def move_to_database():
    data = request.get_json()
    
    # ✅ Validate input
    if not data or "url" not in data:
        return jsonify({"error": "Invalid input, 'url' is required"}), 400

    urls = data["url"]
    
    # ✅ Ensure 'urls' is always a list
    if isinstance(urls, str):
        urls = [urls]  # Convert single string to list

    processor = ScrapeAndTagArticles()
    
    for url in urls:
        processor.move_to_database(url)  # ✅ Corrected usage

    return jsonify({"message": "success"}), 200


if __name__ == "__main__":
    print("Starting Flask app on port 5001...")
    app.run(debug=True, host="127.0.0.1", port=5001)  
