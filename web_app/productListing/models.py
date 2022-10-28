from tokenize import String
from flask import Flask, jsonify, request, session, redirect, url_for
from passlib.hash import pbkdf2_sha256
import uuid
from db import db
from bson.objectid import ObjectId

class ProductListing:
    def showAllProduct(self):
        return db.Product.find()

    def homePageProduct(self):
        return db.Product.find(limit=9)

    def viewProduct(self, productID: String):
        # oid = ObjectId(productID)
        return db.Product.find_one({"_id" : productID})