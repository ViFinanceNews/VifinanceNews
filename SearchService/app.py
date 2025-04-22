import sys
import os
import requests
import json
import flask
import urllib.parse
from ViFinanceCrawLib.article_database.ScrapeAndTagArticles import ScrapeAndTagArticles
from ViFinanceCrawLib.QuantAna.QuantAna_albert import QuantAnaInsAlbert
from flask import request, jsonify
from urllib.parse import unquote, unquote_plus
import hashlib


UP_VOTE=1
DOWN_VOTE=-1

app = flask.Flask(__name__)

scrapped_url = []


@app.route("/get_cached_result/<string:user_query>", methods=['GET'])
def get_articles(user_query):
    user_query = unquote_plus(user_query)
    if not user_query or QuantAnaInsAlbert.obsence_check(user_query):
        return jsonify({"error": "Invalid input"}), 400

    processor = ScrapeAndTagArticles()
    
    try:
        scraped_data = processor.search_and_scrape(user_query)
        if not scraped_data:
            return jsonify({"error": "No results found"}), 404  # Return 404 if no data found
        
        # print("Scraped URLs:", scraped_data)  # Debugging info
        id=get_user_id()
        if id is not None:
            processor.move_query(id, hashlib.sha256(user_query.encode()).hexdigest())
            
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

def get_user_id():
    BASE_URL = "http://localhost:7000"

    session = requests.Session()
    
    """Retrieve the user_id from the /api/auth-status endpoint."""
    auth_status_url = f"{BASE_URL}/api/auth-status"
    
    response = session.get(auth_status_url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("loggedIn"):
            user_id = data.get("userId")
            print(f"User ID: {user_id}")
            return user_id
        else:
            print("User is not logged in.")
            return None
    else:
        print("Failed to check auth status:", response.json())
        return None


@app.route('/vote', methods=['POST'])
def upvote():
    data = flask.request.get_json()
    url = data.get('url')
    vote_type = data.get('vote_type')

    processor = ScrapeAndTagArticles()
    
    try:
        # Update Redis cache
        redis_key = f"article:{url}"
        current_vote_type = processor.redis_client.hget(redis_key, "vote_type")
        current_vote_type = int(current_vote_type) if current_vote_type else 0  # Default to 0 if not set

        if vote_type == UP_VOTE:
            if current_vote_type == 1:
                # Undo upvote
                processor.redis_client.hincrby(redis_key, "upvote", -1)
                processor.redis_client.hset(redis_key, "vote_type", 0)
            elif current_vote_type == -1:
                # Change downvote to upvote
                processor.redis_client.hincrby(redis_key, "upvote", 2)
                processor.redis_client.hset(redis_key, "vote_type", 1)
            else:
                # Add upvote
                processor.redis_client.hincrby(redis_key, "upvote", 1)
                processor.redis_client.hset(redis_key, "vote_type", 1)

        elif vote_type == DOWN_VOTE:
            if current_vote_type == -1:
                # Undo downvote
                processor.redis_client.hincrby(redis_key, "upvote", 1)
                processor.redis_client.hset(redis_key, "vote_type", 0)
            elif current_vote_type == 1:
                # Change upvote to downvote
                processor.redis_client.hincrby(redis_key, "upvote", -2)
                processor.redis_client.hset(redis_key, "vote_type", -1)
            else:
                # Add downvote
                processor.redis_client.hincrby(redis_key, "upvote", -1)
                processor.redis_client.hset(redis_key, "vote_type", -1)

        return flask.jsonify({'status': 'success'})
    except Exception as e:
        return flask.jsonify({'status': 'error', 'message': str(e)})

    



if __name__ == "__main__":
    print("Starting Flask app on port 5001...")
    app.run(debug=True, host="127.0.0.1", port=5001)  
