from flask import Flask, jsonify, render_template, request, url_for, session, redirect
import os
from pymongo import MongoClient

app = Flask(__name__)

# Connection to mongo database


def MongoDB():


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('index.html')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
