import sys
import os
import requests
import json
import urllib.parse

# Move up to 'src/main' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import flask
from ViFinanceCrawLib.article_database.ScrapeAndTagArticles import ScrapeAndTagArticles
from flask import request, jsonify
from urllib.parse import unquote, unquote_plus
app = flask.Flask(__name__)
scrapped_url = []

BASE_URL = "http://127.0.0.1:5001"

@app.route("/get_cached_result/<string:user_query>", methods=['GET'])
def get_articles(user_query):
    user_query = unquote_plus(user_query)
    print("query ", user_query)
    if not user_query :
        return jsonify({"error": "Invalid input"}), 400

    processor = ScrapeAndTagArticles()

    scrapped_url.append(processor.search_and_scrape(user_query))
    print("Sucess")
    return jsonify({"message": "success"}), 200

# If user favorites the article, move it from Redis to the database using its URL as key
@app.route('/save', methods=['POST'])
def move_to_database():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Invalid input, 'url' is required"}), 400

    processor = ScrapeAndTagArticles()
    for url in scrapped_url:
        if scrapped_url==url:
            processor.move_to_database(url)

    return jsonify({"message": "success"}), 200


if __name__ == "__main__":
    print("Starting Flask app on port 5001...")
    app.run(debug=True, host="127.0.0.1", port=5001)  # ✅ Ensure Flask starts
