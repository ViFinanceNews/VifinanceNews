from flask import Flask, request, jsonify
from ViFinanceCrawLib.QualAna.ArticleFactCheckUtility import ArticleFactCheckUtility
from ViFinanceCrawLib.QuantAna import QuantAna
from dotenv import load_dotenv
import os
import json
import pprint
from urllib.parse import unquote, unquote_plus
app = Flask(__name__) # Create the Application
load_dotenv(dotenv_path=".devcontainer/devcontainer.env")
# Quantitive Analysis
@app.route('/about_us', methods=['GET']) # About Us Page


@app.route("/search_result/<string:user_query>", methods=['GET', 'POST']) # Search Result Page
def search_article_use_query(user_query): # Search the Article using the User Query - but not added to the Database yet
    user_query = unquote_plus(user_query)
    article_util = ArticleFactCheckUtility()
    search_result = article_util.search_web(user_query, num_results=10)
    result_json = json.dumps(search_result, indent=4, ensure_ascii=False)
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