import sys
import os
import requests
import json
import urllib.parse
# Get absolute path to project root (1 level above SearchService)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add it to Python's module search path
if project_root not in sys.path:
    sys.path.insert(0, project_root)
import flask
from ViFinanceCrawLib.article_database.ScrapeAndTagArticles import ScrapeAndTagArticles
from ViFinanceCrawLib.QuantAna.QuantAna_albert import QuantAnaInsAlbert
from ViFinanceCrawLib.article_database.ArticleQueryDatabase import AQD
from flask import request, jsonify, request
from urllib.parse import unquote, unquote_plus
import hashlib
from flask_cors import CORS
from LoggingService.app import log_event
import time


UP_VOTE=1
DOWN_VOTE=-1
NEUTRAL_VOTE=0
BACKEND_SERVICE_NAME = "SearchService"


app = flask.Flask(__name__)
# CORS(app, supports_credentials=True, origins=["http://localhost:6999"])

CORS(app, supports_credentials=True, origins=["*"])
quant_analyser = QuantAnaInsAlbert()
scrapped_url = []
processor = ScrapeAndTagArticles()
aqd_object = AQD()
print("Search Started")


@app.route("/api/get_cached_result", methods=['POST'])
@log_event(service_name=BACKEND_SERVICE_NAME, event_base="GetCachedResult")
def get_articles():
    data = request.get_json()
    
    user_query = data.get("query", "").strip() if data else ""
    if not user_query or quant_analyser.obsence_check(query=user_query):
        return jsonify({"error": "Yêu cầu tìm kiếm của bạn vi phạm về điều khoản tìm kiếm nội dung an toàn của chúng tôi"}), 400

    
    try:
        scraped_data = processor.search_and_scrape(user_query)
        print("Scrape sucesss")
        if not scraped_data:
            return jsonify({"error": "No results found"}), 404
        
        session_id = request.cookies.get('SESSION_ID')
        user_id = aqd_object.get_userID_from_session(SESSION_ID=session_id)
        
        if user_id is not None: # Save the user search-history
            aqd_object.move_query_to_history(user_id, user_query.encode())

        current_query_key = f"session:{session_id}:current_query"
        aqd_object.redis_usr.set(current_query_key, user_query)
        return jsonify({"message": "success", "data": scraped_data}), 200

    except Exception as e:
        print(f"❌ Server Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500



@app.route('/api/save', methods=['POST'])
@log_event(service_name=BACKEND_SERVICE_NAME, event_base="SaveArticle")
def save():
    try:
        aqd_object.db.connect()
        data = request.get_json()
        session_id = request.cookies.get('SESSION_ID')

        if not session_id:
            return jsonify({"error": "Session not found or expired."}), 401


        user_id = aqd_object.get_userID_from_session(SESSION_ID=session_id)
        if user_id is None:
            return jsonify({"error": "Unauthorized - No userId in session"}), 401
        
        # ✅ Validate input
        if not data or "url" not in data:
            return jsonify({"error": "Invalid input, 'url' is required"}), 400

        urls = data["url"]

        # ✅ Ensure 'urls' is always a list
        if isinstance(urls, str):
            urls = [urls]  # Convert single string to list

        for url in urls:
            aqd_object.move_article_to_database(url, user_id)  # ✅ Corrected usage

        return jsonify({"message": "success"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        

@app.before_request
@log_event(service_name=BACKEND_SERVICE_NAME, event_base="BeforeRequest")
def handle_session_and_query():
    session_id = request.cookies.get('SESSION_ID')
    user_id = aqd_object.get_userID_from_session(session_id)
    if session_id:
        print(f"🔒 session_id: {session_id}")
        
        # Step 1: Check if the session_id is still valid (exists in Redis)
        session_exists = aqd_object.redis_usr.exists(f"session:{session_id}")
        if not session_exists:
            # Session has expired → clean up the query key
            aqd_object.redis_usr.delete(f"session:{session_id}:current_query")
            print(f"🗑️ Session expired. Deleted current_query for session: {session_id}")
            return  # session expired, no further processing

        # Step 2: Check if the user submitted a new query
        data = request.get_json(silent=True)
        if data and "query" in data:
            user_query = data.get("query", "").strip() if data else None

            # Don't delete the query key before reading it!
            previous_query_bytes = aqd_object.redis_usr.get(f"session:{session_id}:current_query")
            previous_query = previous_query_bytes.decode("utf-8") if previous_query_bytes else None


            if user_query and user_query != previous_query:
                print(f"🔄 Query changed from '{previous_query}' to '{user_query}'. Triggering upsert.")
                aqd_object.upsert_articles_from_user_hash(session_id=session_id, user_id=user_id)
                aqd_object.redis_usr.set(f"session:{session_id}:current_query", user_query) # save the current_query
            
        

@app.route('/api/get_up_vote', methods=['POST'])
@log_event(service_name=BACKEND_SERVICE_NAME, event_base="GetUpVote")
def get_up_vote():
    data = request.get_json()
    url = data.get('url')
    try:

        session_id = request.cookies.get('SESSION_ID')

        if not session_id:
            return jsonify({"error": "Please log in to continue"}), 401
        
   
        user_id=aqd_object.get_userID_from_session(SESSION_ID=session_id)
        
   
        if user_id is None:
            return jsonify({"error" : "Missing user_id"}), 401

        user_votes_key = f"user:{user_id}:personal_vote"
        vote_type = aqd_object.redis_usr.hget(user_votes_key, url) 
        if vote_type is None:
            print("[INFO] No vote stored for this user and URL — default to NEUTRAL_VOTE")
            vote_type = NEUTRAL_VOTE

        if isinstance(vote_type, bytes):
            vote_type= int(vote_type)

        
        redis_data = aqd_object.redis_client.get(url) # get the article from cache

        if redis_data is None:
            article_data = {"upvotes": NEUTRAL_VOTE}
        else:
            # Parse the JSON string into a Python dictionary
            article_data = json.loads(redis_data.decode("utf-8"))


        #neutral vote to upvote +1
        if vote_type==NEUTRAL_VOTE:
            print("neutral vote to upvote +1")
            try:
                article_data["upvotes"] += 1
                aqd_object.redis_usr.hset(user_votes_key, url, UP_VOTE)
                vote_type = UP_VOTE
            except Exception as e:
                print(e)
                return jsonify({'status': 'Unable to change neutral vote to upvote', 'message': str(e)}), 500
        #upvote to neutral vote -1
        elif vote_type == UP_VOTE:
            print("upvote to neutral vote -1")
            try:
                # aqd_object.redis_client.hincrby(url, 'up_vote', -1)
                article_data["upvotes"] += -1
                aqd_object.redis_usr.hset(user_votes_key, url, NEUTRAL_VOTE)
                vote_type = NEUTRAL_VOTE
            except Exception as e:
                print(e)
                return jsonify({'status': 'Unable to change upvote to neutral vote', 'message': str(e)}), 500
        #downvote to upvote +2
        elif vote_type == DOWN_VOTE:
            print("downvote to upvote +2")
            try:
                article_data["upvotes"] += 2
                aqd_object.redis_usr.hset(user_votes_key, url, UP_VOTE)
                vote_type = UP_VOTE
            except Exception as e:
                print(e)
                return jsonify({'status': 'Unable to change downvote to upvote', 'message': str(e)}), 500
            
        aqd_object.redis_client.set(url, json.dumps(article_data))
        return jsonify({'vote_type': vote_type}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/get_down_vote', methods=['POST'])
@log_event(service_name=BACKEND_SERVICE_NAME, event_base="GetDownVote")
def get_down_vote():
    data = request.get_json()
    url = data.get('url')
    try:

        session_id = request.cookies.get('SESSION_ID')

        if not session_id:
            return jsonify({"error": "Guest cannot vote on the article. Please log in to continue"}), 401
        

        user_id=aqd_object.get_userID_from_session(SESSION_ID=request.cookies.get('SESSION_ID'))
        if user_id is None:
            return jsonify({"error": "Missing the user_id"}), 401

        user_votes_key = f"user:{user_id}:personal_vote"
        vote_type = aqd_object.redis_usr.hget(user_votes_key, url)
        if vote_type is None:
            print("[INFO] No vote stored for this user and URL — default to NEUTRAL_VOTE")
            vote_type = NEUTRAL_VOTE
        
        if isinstance(vote_type, bytes):
            vote_type= int(vote_type)

        redis_data = aqd_object.redis_client.get(url)

        if redis_data is None:
            article_data = {"upvotes": NEUTRAL_VOTE}
        else:
            # Parse the JSON string into a Python dictionary
            article_data = json.loads(redis_data.decode("utf-8"))

       
        #neutral vote to downvote -1
        if vote_type==NEUTRAL_VOTE:
            print("neutral vote to downvote -1")
            try:
                article_data["upvotes"] += -1
                aqd_object.redis_usr.hset(user_votes_key, url, DOWN_VOTE)
                vote_type = DOWN_VOTE
            except Exception as e:
                print(e)
                return jsonify({'status': 'Unable to change neutral vote to downvote', 'message': str(e)}), 500
        #downvote to neutral vote +1
        elif vote_type == DOWN_VOTE:
            print("downvote to neutral vote +1")
            try:
                article_data["upvotes"] += 1
                aqd_object.redis_usr.hset(user_votes_key, url, NEUTRAL_VOTE)
                vote_type = NEUTRAL_VOTE
            except Exception as e:
                print(e)
                return jsonify({'status': 'Unable to change downvote to neutral vote', 'message': str(e)}), 500
        #upvote to downvote -2
        elif vote_type == UP_VOTE:
            print("upvote to downvote -2")
            try:
                article_data["upvotes"] += -2
                aqd_object.redis_usr.hset(user_votes_key, url, DOWN_VOTE)
                vote_type = DOWN_VOTE
            except Exception as e:
                print(e)
                return jsonify({'status': 'Unable to change upvote to downvote', 'message': str(e)}), 500
            
        aqd_object.redis_client.set(url, json.dumps(article_data))
        return jsonify({'vote_type': vote_type}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
@app.route('/api/get_user_vote', methods=['POST'])
@log_event(service_name=BACKEND_SERVICE_NAME, event_base="GetUserVote")    
def get_user_vote():
    data = request.get_json()
    url = data.get('url')
    try:
        session_id = request.cookies.get('SESSION_ID')

        if not session_id:
            return jsonify({"error": "Missing Session ID - Login Again"}), 401
        
        user_id=aqd_object.get_userID_from_session(SESSION_ID=request.cookies.get('SESSION_ID'))
        if user_id is None:
            return jsonify({"error": "Missing User ID - Login Again"}), 401

        user_votes_key = f"user:{user_id}:personal_vote"
        vote_type = aqd_object.redis_usr.hget(user_votes_key, url) 
        if vote_type is None :
            return jsonify({'status': 'error', 'message': 'Unable to get the vote'}), 500
        vote_type= int(vote_type)

        return jsonify({'usr_vote': vote_type}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/api/get_total_upvotes', methods=['POST'])
@log_event(service_name=BACKEND_SERVICE_NAME, event_base="GetTotalUpVotes") 
def get_total_upvotes():
    data = request.get_json()
    url = data.get('url')

    try:
        redis_data = aqd_object.redis_client.get(url) # get the article from cache

        if redis_data is None:
            return jsonify({'status': 'error', 'message': "Unable to get the articles data"}), 501
        
        article_data = json.loads(redis_data.decode("utf-8"))

        upvotes_data = article_data["upvotes"]
        # print(f"The upvotes: {upvotes_data}")
        if upvotes_data is None:
            return jsonify({'status': 'error', 'message': "upvotes data is not exist"}), 502
        
        return jsonify({'upvotes': upvotes_data}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# if __name__ == "__main__":
#     print("Starting Flask app on port 7001...")
#     app.run(debug=False, host="0.0.0.0", port=7001)  
