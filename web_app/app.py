from flask import Flask, jsonify, render_template, request, url_for, session, redirect
import os
from pymongo import MongoClient
import db

app = Flask(__name__)

# Connection to mongo database


@app.route('/test', methods=['POST', 'GET'])
def MongoDB():
    db.db.User.insert_one({"email": "jon@gmail.com"})
    return "I am connected to db!"


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('index.html')


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
