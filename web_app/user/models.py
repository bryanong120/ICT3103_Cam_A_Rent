from datetime import datetime
from flask import jsonify, request, session, redirect, url_for, flash
from passlib.hash import pbkdf2_sha256
import uuid
from db import db
from tokenize import String
from datetime import datetime
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
            "password": request.form.get('password'),
            "virtualCredit": 1000
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
        user = db.User.find_one({"email": request.form.get('email')})

        ## request.form.get('password') is un-encrypted
        ## user['password'] is encrypted
        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)

        return jsonify({"error": "Invalid login credentials"}), 401

    def viewListing(self):
        if session['logged_in'] :
            user = session['user']
            user_product = db.Product.find({"uid": user['_id']})
            return user_product

    def delListing(self, productID: str):
        return db.Product.delete_one({"_id": productID})

    def findUserDetails(self, userID: str):
        if session['logged_in'] :
            uID = session['user']['_id']
            userDetails = db.User.find_one({'_id': uID})
            return userDetails

    def deductDeposit(self, productObj):
        error = ""
        if session['logged_in'] :
            uID = session['user']['_id']
            userObj = User().findUserDetails(uID)

            try:
                dValue = int(productObj['initialDeposit'])
            except:
                error = "deposit value is not an int"
                return flash(error)

            if userObj['virtualCredit'] <  dValue :
                error = "insufficient credit!"
                return flash(error)

            #Deduct credits from user
            db.User.update_one(
                {'_id': uID}, 
                {'$inc': 
                    {'virtualCredit': -dValue}
                    })
            successMsg = "Successfully deducted ${} from {}".format(dValue, session['user']['username'])
            flash(successMsg)

            #Insert deposit logs 
            deposit = {
                'pid' : productObj['_id'],
                'amount': dValue,
                'owner': productObj['uid'],
                'rentee': uID,
                'date' : datetime.utcnow(),
            }
            db.Deposit.insert_one(deposit)
            
