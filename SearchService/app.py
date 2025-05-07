import sys
import os
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
CORS(app)

quant_analyser = QuantAnaInsAlbert()
scrapped_url = []
processor = ScrapeAndTagArticles()
aqd_object = AQD()


@app.route("api/get_cached_result", methods=['POST'])
def get_articles():
    data = request.get_json()

    user_query = data.get("query", "").strip() if data else ""
    if not user_query or quant_analyser.obsence_check(query=user_query):
        return jsonify({"error": "Yêu cầu tìm kiếm của bạn vi phạm về điều khoản tìm kiếm nội dung an toàn của chúng tôi"}), 400

    try:
        scraped_data = processor.search_and_scrape(user_query)
        print("Scrape sucesss")
        print(scraped_data)
        if not scraped_data:
            return jsonify({"error": "No results found"}), 404
        
        # user_id = get_user_id()  # Replace with dynamic user ID logic
        # # print(f"Get User_id {user_id}")
        # if user_id is not None:
        #     hashed_query = hashlib.sha256(user_query.encode()).hexdigest()
        #     # print(f"user hash-query {hashed_query}")
        #     # print(f"user id {user_id}")
        #     aqd_object.move_query(user_id, hashed_query)

        return jsonify({"message": "success", "data": scraped_data}), 200

    except Exception as e:
        print(f"❌ Server Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# If user favorites the article, move it from Redis to the database using its URL as key

@app.route('api/save', methods=['POST'])
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

        for url in urls:
            aqd_object.move_to_database(url)  # ✅ Corrected usage

        return jsonify({"message": "success"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# DEPRECATED NOT IN USE
# def get_user_id():
#     BASE_URL = "http://localhost:8000"

#     session = requests.Session()
    
#     """Retrieve the user_id from the /api/auth-status endpoint."""
#     auth_status_url = f"{BASE_URL}/auth-status"
    
#     response = session.get(auth_status_url)
    
#     if response.status_code == 200:
#         data = response.json()
#         if data.get("loggedIn"):
#             user_id = data.get("userId")
#             print(f"User ID: {user_id}")
#             return user_id
#         else:
#             print("User is not logged in.")
#             return None
#     else:
#         print("Failed to check auth status:", response.json())
#         return None


@app.route('/vote', methods=['POST'])
def upvote():
    data = request.get_json()
    url = data.get('url')
    vote_type = data.get('vote_type')
    try:
        # Update Redis cache
        redis_key = url
        raw_data = aqd_object.redis_client.get(redis_key) # JSON String
        json_string = raw_data.decode("utf-8")
        article_data = json.loads(json_string)
        article_data["vote_type"] = vote_type
        aqd_object.redis_client.set(redis_key, json.dumps(article_data), ex=3600)
        return flask.jsonify({'status': 'success'})
    except Exception as e:
        return flask.jsonify({'status': 'error', 'message': str(e)})


# if __name__ == "__main__":
#     print("Starting Flask app on port 7001...")
#     app.run(debug=False, host="0.0.0.0", port=7001)  
