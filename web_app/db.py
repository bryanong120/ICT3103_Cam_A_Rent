from flask_pymongo import pymongo

DB_URI = "mongodb+srv://nikoswee:296JsRtDcmhJMD4a@rent-a-cam.tf5um47.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(DB_URI, tls=True)
db = client.get_database('Cam-A-Rent')