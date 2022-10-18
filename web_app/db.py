from flask import Flask
from flask_pymongo import pymongo

CONNECTION_STRING = "mongodb+srv://nikoswee:apple1234@rent-a-cam.tf5um47.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('Cam-A-Rent')
user_collection = pymongo.collection.Collection(db, 'User')

