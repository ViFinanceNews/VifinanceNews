
import sys
import os

# Move up to 'src/main' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


from ViFinanceCrawLib.QualAna import ArticleFactCheckUtility
from ViFinanceCrawLib.QualAna import ArticleFactCheckUtility
from flask import Flask, request, jsonify
from ViFinanceCrawLib.QualAna import ArticleFactCheckUtility
import os
import json
from urllib.parse import unquote, unquote_plus
import redis
import hashlib



redis_client = redis.Redis(
    host= os.getenv('REDIS_HOST'),
    port = os.getenv('REDIS_PORT'),
    password = os.getenv('REDIS_PASSWORD'),
    ssl=True
)

def hash_query(query, salt="ViFinanceNews#123"): # for encode the data to enhance security
    salted_query = query + salt
    return hashlib.sha256(salted_query.encode('utf-8')).hexdigest()

app = Flask(__name__)

@app.route("/get_cached_result/<string:user_query>", methods=['GET'])
# to get the cached result for fast retrieving
def get_cached_result(user_query):
    user_query = unquote_plus(user_query)
    hashed_key = hash_query(user_query)
    
    cached_result = redis_client.get(hashed_key)
    if cached_result:
        print("✅ Cached result found.")
        return jsonify(json.loads(cached_result))
    else:
        print("❌ No cached result found.")
        return jsonify({"message": "No cached result found for this query."}), 404

@app.route("/search_result/<string:user_query>", methods=['POST']) # Search Result Page
def search_article_use_query(user_query): # Search the Article using the User Query - but not added to the Database yet
    user_query = unquote_plus(user_query)
    hashed_key = hash_query(user_query)
    # Optional: Check cache first if the query exist in the Redis
    cached_result = redis_client.get(hashed_key)
    if cached_result:
        print("✅ Returning cached result.")
        decoded_result = cached_result.decode('utf-8')  # Convert bytes -> string
        result_json = json.dumps(decoded_result, indent=4, ensure_ascii=False)
        return jsonify(result_json)
    
    article_util = ArticleFactCheckUtility()
    search_result = article_util.search_web_fast(user_query, num_results=10)
    article_list = [article["main_text"] for article in search_result]
    batch_size = article_util.choose_the_batch_size(article_list)
    tag_list = article_util.process_articles_in_batches(article_list, batch_size = batch_size)
    for i, article in enumerate(search_result):
        article["tags"] = tag_list[i]      
    result_json = json.dumps(search_result, indent=4, ensure_ascii=False)
    # ✅ Store securely
    redis_client.set(hashed_key, result_json, ex=86400)  # TTL (expiration date) = 1 day
    return jsonify(result_json)

