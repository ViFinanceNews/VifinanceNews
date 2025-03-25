from flask import Flask, request, jsonify
from ViFinanceCrawLib.QualAna.ArticleFactCheckUtility import ArticleFactCheckUtility
from ViFinanceCrawLib.QuantAna import QuantAna
from dotenv import load_dotenv
import os
import json
import pprint
from urllib.parse import unquote, unquote_plus
import redis
import hashlib

redis_client = redis.Redis(
  host='together-ray-37993.upstash.io',
  port=6379,
  password= os.getenv('REDIS_PASSWORD'),
  ssl=True
)


app = Flask(__name__) # Create the Application

def hash_query(query, salt="ViFinanceNews#123"):
    salted_query = query + salt
    return hashlib.sha256(salted_query.encode('utf-8')).hexdigest()

# Load environment variables from .env file
load_dotenv(dotenv_path=".devcontainer/devcontainer.env")
# Quantitive Analysis
@app.route('/about_us', methods=['GET']) # About Us Page

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

@app.route("/search_result/<string:user_query>", methods=['GET', 'POST']) # Search Result Page
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

def flag_save_article(): # Flag And Save the Article
    return



def get_the_synthesis_sum_of_article(): # get the synthesis & summarization of multiple articles
    return

@app.route('/article', methods=['GET', 'POST']) # Article Page (for one article)
def article_page(): # Article Page
    return "Welcome to the Article Page!"
def get_fact_checking_of_one_article(): # get the fact checking of one article
    return
def get_summarization_of_one_article(): # get the abstractive summarization of one article
    return
def get_qualitative_analysis(): # this would return the qualitative analysis result
    # include the bias - check
    # include the toxicity check
    # include the sentiment analysis
    return
def get_relationship_between_articles(): # get the inter-relationship between the articles
    return
def get_quantitative_analysis(): # this would return the quantiative analysis result 
    return
def check_tag_article(): # check the tag of the article
    return

# @app.route('/home_page', methods=['GET', 'POST']) # Homepage
# def home_page():
#     return "Welcome to the Home Page!" 

# @app.route('/sign_in', methods=['GET', 'POST']) # Sign-in Page

# @app.route('/sign_out', methods=['GET', 'POST']) # Sign-out Page

# @app.route('/user/<name>', methods=['GET', 'POST']) # User Page


# @app.route('/sign_up', methods=['GET', 'POST']) # Sign-up Page


# @app.route('/settings', methods=['GET', 'POST'])
# # Qualtivative Analysis

def home():
    return 


if __name__ == '__main__':
  app.run(debug=True) # Run the Application