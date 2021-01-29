from flask import Flask, request
app = Flask(__name__)

@app.route('/factcheck', methods=['POST'])
def factCheck():

    if request.method == 'POST':

        if request.form['data'] == 'fact':
            return '\nFACT!\n'
        else:
            return '\nFALSE\n'
