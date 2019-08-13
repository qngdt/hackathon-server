from flask import Flask, request, flash, redirect
from flask_cors import CORS, cross_origin
from werkzeug.datastructures import ImmutableMultiDict
import os
import json
import sys
import time
sys.path.append(os.getcwd())
if not os.path.exists('tmp'):
    os.makedirs('tmp')
app = Flask(__name__)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
CORS(app)


@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/data')
def data():
    return 'data'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8000')