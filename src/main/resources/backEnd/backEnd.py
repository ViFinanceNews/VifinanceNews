from flask import Flask, request, jsonify
from ViFinanceCrawLib.QualAna.ArticleFactCheckUtility import ArticleFactCheckUtility
from ViFinanceCrawLib.QuantAna import QuantAna

from dotenv import load_dotenv
import os
import json

app = Flask(__name__) # Create the Application
load_dotenv(dotenv_path=".devcontainer/devcontainer.env")
# Quantitive Analysis
@app.route('/about_us', methods=['GET']) # About Us Page


@app.route("/search_result/<string:user_query>", methods=['GET', 'POST']) # Search Result Page
def search_article_use_query(user_query): # Search the Article using the  User Query
    article_util = ArticleFactCheckUtility()
    search_result = article_util.search_web(user_query, num_results=1)
    result_json = json.dumps(search_result, indent=4, ensure_ascii=False)
    return jsonify(result_json)

# @app.route('/article', methods=['GET', 'POST']) # Article Page (for one article)


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