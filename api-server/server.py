from flask import Flask, request, jsonify
from flask_cors import CORS
from statement_finder import *
from web_crawler_Snopes import *
from web_crawler_Wikipedia import *


app = Flask(__name__)
CORS(app)

@app.route('/factcheck', methods=['POST'])
def factCheck():

    if request.method == 'POST':

        foundOnSnopes = False

        statementArray = atomic_find_statements(request.json['data'])


        # If a full statement cannot be parsed return immediately
        if len(statementArray) == 0:
            return jsonify(
                statementsParsed = 0
            )

        else:

            wikiCrawl = Crawler()
            snopesCrawl = Search_n_Scraper()

            for x in statementArray:
                wikiSite = wikiCrawl.wiki_search(x)
                wikiCrawl.crawl(wikiSite)
 
                snopesSites = snopesCrawl.snopes_search(x)

            if len(snopesSites) > 0:
                foundOnSnopes = True

            return jsonify(
                foundOnSnopes = foundOnSnopes,
                snopes = snopesSites[0].url,
                rating = snopesSites[0].rating,
                true = snopesSites[0].rating_whatsTrue,
                false = snopesSites[0].rating_whatsFalse,
                wiki = wikiCrawl.visited[0]
            )



## statement_finder.py instructions ##
# Input: inputText = text gathered from web
# Process: call atomic_find_statements(inputText)
# Output: array of strings (possibly empty) where each string is a statement from the input text
# Example: atomic_find_statements("Granny Smith apples are green. Do you like Granny Smith apples?") = ['granny smith apples are green']