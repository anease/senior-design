from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/factcheck', methods=['POST'])
def factCheck():

    if request.method == 'POST':

        if request.json['data'] == 'fact':
            return '\nFACT!\n'
        else:
            return '\nFALSE\n'
