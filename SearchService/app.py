import sys
import os

# Get absolute path to project root (1 level above SearchService)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add it to Python's module search path
if project_root not in sys.path:
    sys.path.insert(0, project_root)
import requests
import json
import flask
import urllib.parse
from ViFinanceCrawLib.article_database.ScrapeAndTagArticles import ScrapeAndTagArticles
from ViFinanceCrawLib.QuantAna.QuantAna_albert import QuantAnaInsAlbert
from ViFinanceCrawLib.article_database.ArticleQueryDatabase import AQD
from flask import request, jsonify
from urllib.parse import unquote, unquote_plus
import hashlib
from flask_cors import CORS

UP_VOTE=1
DOWN_VOTE=-1

app = flask.Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:6999"])

quant_analyser = QuantAnaInsAlbert()
scrapped_url = []
processor = ScrapeAndTagArticles()
aqd_object = AQD()


@app.route("/api/get_cached_result", methods=['POST'])
def get_articles():
    data = request.get_json()

    user_query = data.get("query", "").strip() if data else ""
    if not user_query or quant_analyser.obsence_check(query=user_query):
        return jsonify({"error": "Yêu cầu tìm kiếm của bạn vi phạm về điều khoản tìm kiếm nội dung an toàn của chúng tôi"}), 400

    try:
        scraped_data = processor.search_and_scrape(user_query)
        print("Scraped Data:", scraped_data)
        if not scraped_data:
            return jsonify({"error": "No results found"}), 404

        return jsonify({"message": "success", "data": scraped_data}), 200

    except Exception as e:
        print(f"❌ Server Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# If user favorites the article, move it from Redis to the database using its URL as key

@app.route('/api/save', methods=['POST'])
def move_to_database():
    try:
        aqd_object.db.connect()
        data = request.get_json()

        # ✅ Validate input
        if not data or "url" not in data:
            return jsonify({"error": "Invalid input, 'url' is required"}), 400

        urls = data["url"]

        # ✅ Ensure 'urls' is always a list
        if isinstance(urls, str):
            urls = [urls]  # Convert single string to list
            
        # ✅ Extract session ID from cookie
        session_id = request.cookies.get("SESSION_ID")
        print(f"Session ID: {session_id}")
        if not session_id:
            return jsonify({"error": "Unauthorized – No session cookie found"}), 401

        # ✅ Get userId from Redis session
        session_key = f"session:{session_id}"  
        session_data_raw = aqd_object.redis_client.get(session_key)
        print(f"Redis Key: {session_key}")
        print(f"Raw session data: {session_data_raw}")

        if not session_data_raw:
            return jsonify({"error": "Session expired or invalid"}), 401

        try:
            session_data = json.loads(session_data_raw.decode("utf-8"))
            user_id = session_data.get("userId")
        except Exception as e:
            print(f"Session JSON decode error: {e}")
            return jsonify({"error": "Invalid session format"}), 500

        if not user_id:
            return jsonify({"error": "Unauthorized – No userId in session"}), 401

        for url in urls:
            aqd_object.move_to_database(url, user_id)  # ✅ Corrected usage

        return jsonify({"message": "success"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/get_up_vote', methods=['POST'])
def get_up_vote():
    data = request.get_json()
    url = data.get('url')
    try:
        # Get vote type from Redis cache
        redis_key = url
        raw_data = aqd_object.redis_client.get(redis_key) # JSON String
        json_string = raw_data.decode("utf-8")
        article_data = json.loads(json_string)
        vote_type = article_data.get("vote_type")
        if vote_type==0:
            aqd_object.redis_client.hincrby(redis_key, 'up_vote', 1)
            aqd_object.redis_client.hset(redis_key, vote_type, 1)
        if vote_type == UP_VOTE:
            aqd_object.redis_client.hincrby(redis_key, 'up_vote', -1)
            aqd_object.redis_client.hset(redis_key, vote_type, 0)
        elif vote_type == DOWN_VOTE:
            aqd_object.redis_client.hincrby(redis_key, 'up_vote', -2)
            aqd_object.redis_client.hset(redis_key, vote_type, -1)
        
        return flask.jsonify({'vote_type': vote_type})
    except Exception as e:
        return flask.jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/get_down_vote', methods=['POST'])
def get_down_vote():
    data = request.get_json()
    url = data.get('url')
    try:
        # Get vote type from Redis cache
        redis_key = url
        raw_data = aqd_object.redis_client.get(redis_key) # JSON String
        json_string = raw_data.decode("utf-8")
        article_data = json.loads(json_string)
        vote_type = article_data.get("vote_type")
        if vote_type==0:
            aqd_object.redis_client.hincrby(redis_key, 'up_vote', -1)
            aqd_object.redis_client.hset(redis_key, vote_type, -1)
        if vote_type == UP_VOTE:
            aqd_object.redis_client.hincrby(redis_key, 'up_vote', 2)
            aqd_object.redis_client.hset(redis_key, vote_type, 1)
        elif vote_type == DOWN_VOTE:
            aqd_object.redis_client.hincrby(redis_key, 'up_vote', 1)
            aqd_object.redis_client.hset(redis_key, vote_type, 0)
        
        return flask.jsonify({'vote_type': vote_type})
    except Exception as e:
        return flask.jsonify({'status': 'error', 'message': str(e)})


if __name__ == "__main__":
    print("Starting Flask app on port 7001...")
    app.run(debug=True, host="0.0.0.0", port=7001)  