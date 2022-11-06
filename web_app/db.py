from flask_pymongo import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

DB_URI = os.getenv('DB_URI')
client = pymongo.MongoClient(DB_URI, tls=True)
db = client.get_database('Cam-A-Rent')