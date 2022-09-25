from flask import Flask, jsonify
import pymongo
from pymongo import MongoClient

app = Flask(__name__)


def get_db():
    client = MongoClient(host='test_mongodb',
                         port=27017,
                         user='root',
                         password='pass',
                         authSource='admin')

    db = client["camera_db"]
    return db


@app.route('/')
def ping_server():
    return "Welcome to Cam-A-Rent"


@app.route('/cameras')
def fetch_cameras():
    db = get_db()
    _cameras = db.camera_tb.find()
    cameras = [{"userid": camera["id"], "name": camera["name"]}
               for camera in _cameras]
    return jsonify({"cameras": cameras})


if __name__ == 'main':
    app.run(host='0.0.0.0', port=5000)
