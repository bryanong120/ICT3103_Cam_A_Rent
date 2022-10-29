from flask import Flask, jsonify, request, session, redirect, url_for
from passlib.hash import pbkdf2_sha256
import uuid
from db import db
from tokenize import String
# status code 200 = OK request fulfilled
# status code 400 = BAD request
# status code 401 = Unauthorized entry


class User:

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def signup(self):
        # create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "username": request.form.get('username'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }

        # encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        # check for existing email
        if db.User.find_one({"email": user['email']}):
            return jsonify({"error": "Email address already in use"}), 400

        # insert user if there is no existing email
        if db.User.insert_one(user):
            return self.start_session(user)

        # throw error
        return jsonify({"error:" "Signup failed"}), 400

    def signout(self):
        session.clear()
        return redirect(url_for("home"))

    def login(self):
        user = db.User.find_one({"email": request.form.get('email')})
        # check for user email in db and if password matches
        ## request.form.get('password') is un-encrypted
        ## user['password'] is encrypted

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)

        return jsonify({"error": "Invalid login credentials"}), 401

    def viewUserListing(self):
        if session['logged_in'] == True:
            user = session['user']
            user_product = db.Product.find({"uid": user['_id']})
            return user_product

    def delProduct(self, productID: String):
        return db.Product.delete_one({"_id": productID})
