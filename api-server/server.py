from flask import Flask, request
from flask_cors import CORS
from statement_finder import *
from web_crawler_Snopes import *
from web_crawler_Wikipedia import *


app = Flask(__name__)
CORS(app)

@app.route('/factcheck', methods=['POST'])
def factCheck():

    if request.method == 'POST':

        if request.json['data'] == 'fact':
            return '\nFACT!\n'
        else:
            return '\nFALSE\n'


## statement_finder.py instructions ##
# Input: inputText = text gathered from web
# Process: call atomic_find_statements(inputText)
# Output: array of strings (possibly empty) where each string is a statement from the input text
# Example: atomic_find_statements("Granny Smith apples are green. Do you like Granny Smith apples?") = ['granny smith apples are green']