# from flask import Flask
# app = Flask(__name__)
#
# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'

from app import app
import os

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)