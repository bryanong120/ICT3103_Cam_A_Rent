from flask import jsonify, request, session, redirect, url_for, flash
from passlib.hash import pbkdf2_sha256
import uuid
import re
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
    	#input validation
        #username validation
        username =  request.form.get('username')
        if len(username) < 3:
            return jsonify({"error": "Username must be at least 3 characters"}), 400 #username 3 characters and above
        if re.match("^[a-zA-Z0-9_.-]+$", username) == None:
            return jsonify({"error": "Username can only include letters, numbers and . , -, _ but not special characters"}), 400 #username only allows alphanumeric and -, ., _ symbols

        #email validation
        email = request.form.get('email')
        if re.match("^[a-zA-Z0-9@_.-]+$", email) == None:
            return jsonify({"error": "Please input valid email"}), 400
        
        #password validation
        password = request.form.get('password')
        if len(password) == 0:
            return jsonify({"error": "Password cannot be empty"}), 400

        if len(password) < 12:
            return jsonify({"error": "Password should be at least 12 characters long"}), 400

        if len(password) > 128:
            return jsonify({"error": "Password cannot be longer than 128 characters"}), 400

        if username in password:
            return jsonify({"error": "Password cannot contain your username"}), 400


            
        # create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "username": username,
            "email": email,
            "password": password,
            "failed_logins": 0
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
        return redirect(url_for("homePage"))

    def login(self):
        # check for user email in db and if password matches
        
        #login user validation
        login_email = request.form.get('email')
        if re.match("^[a-zA-Z0-9@_.-]+$", login_email) == None:
            return jsonify({"error": "Please input a valid email"}), 400
            
        user = db.User.find_one({"email": login_email})

        ## request.form.get('password') is un-encrypted
        ## user['password'] is encrypted
        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)

        elif user and not(pbkdf2_sha256.verify(request.form.get('password'), user['password'])):
            return jsonify({"error": "Testing"}), 401

        return jsonify({"error": "Invalid login credentials"}), 401

    def viewListing(self):
        if session['logged_in'] == True:
            user = session['user']
            user_product = db.Product.find({"uid": user['_id']})
            return user_product

    def delListing(self, productID: String):
        return db.Product.delete_one({"_id": productID})
