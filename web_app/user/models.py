from datetime import datetime
from flask import jsonify, request, session, redirect, url_for, flash, escape
from passlib.hash import pbkdf2_sha256
import uuid
import re
from db import db
from tokenize import String
from datetime import datetime
# status code 200 = OK request fulfilled
# status code 400 = BAD request
# status code 401 = Unauthorized entry


class User:

    def start_session(self, user, verified):
        del user['password']
        session['user'] = user
        
        if verified:
            session['logged_in'] = True
            return jsonify(user), 200
        else:
            session['logged_in'] = False
            
    def requestOTP(self):
        user = session['user']
        phonenumber = user['phonenumber']
        #if user['verifed'] == 0:
        email = user['email']
            #requestPhoneOTP(phonenumber])
            #requestEmailOTP(email])
        return redirect(url_for("verifyOTPPage"))
        #else:
            #requestPhoneOTP(phonenumber)
        return redirect(url_for("loginOTPPage"))
        
    def verifyOTP(self):
        phoneotp = escape(request.form.get('phoneotp'))
        if re.match("^\+[\d]+$", phoneotp) == None:
            return jsonify({"error": "Please input valid phone OTP"}), 400
        
        emailotp = escape(request.form.get('emailotp'))
        if re.match("^\+[\d]+$", emailotp) == None:
            return jsonify({"error": "Please input valid email OTP"}), 400
            
        user = session['user']
        phonenumber = user['phonenumber']
        email = user['email']
        if checkPhoneOTP(phonenumber, phoneotp) && checkEmailOTP(email, emailotp):
            return self.start_session(user, True)
        
        return jsonify({"error": "Incorrect code submitted"}), 400
        
    def loginOTP(self):
        phoneotp = escape(request.form.get('phoneotp'))
        if re.match("^\+[\d]+$", phoneotp) == None:
            return jsonify({"error": "Please input valid phone OTP"}), 400
        
        user = session['user']
        phonenumber = user['phonenumber']
        if checkPhoneOTP(phonenumber, phoneotp):
            return self.start_session(user, True)
        
        return jsonify({"error": "Incorrect code submitted"}), 400
        
    def signup(self):
        username = escape(request.form.get('username'))
        if len(username) < 3:   # username 3 characters and above
            return jsonify({"error": "Username must be at least 3 characters"}), 400
        if re.match("^[a-zA-Z0-9_.-]+$", username) == None:  # username only allows alphanumeric and -, ., _ symbols
            return jsonify({"error": "Username can only include letters, numbers and . , -, _ but not special characters"}), 400
        if db.User.find_one({"username": username}): #check for exsting username
            return jsonify({"error": "Username already in use"}), 400

        # email validation
        email = escape(request.form.get('email'))
        if re.match("^[a-zA-Z0-9@_.-]+$", email) == None:
            return jsonify({"error": "Please input valid email"}), 400
        # check for existing email
        if db.User.find_one({"email": email}):
            return jsonify({"error": "Email address already in use"}), 400

        # phone number validation
        phonenumber = escape(request.form.get('phonenumber'))
        phonenumber = phonenumber.replace(' ','')
        if re.match("^\+[\d]+$", phonenumber) == None:
            return jsonify({"error": "Please input valid phone number"}), 400

        # password validation
        password = escape(request.form.get('password'))
        if len(password) == 0:
            return jsonify({"error": "Password cannot be empty"}), 400
        if len(password) < 12:
            return jsonify({"error": "Password should be at least 12 characters long"}), 400

        if len(password) > 128:
            return jsonify({"error": "Password cannot be longer than 128 characters"}), 400

        if username in password:
            return jsonify({"error": "Password cannot contain your username"}), 400

        # create the user objectusername = escape(request.form.get('username'))


        # create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "username": username,
            "email": email,
            "phonenumber": phonenumber,
            "password": password,
        #    "failed_logins": 0,
            "virtualCredit": 1000,
            "verified" : 0
        }

        # encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

       
        # insert user if there is no existing email
        #if db.User.insert_one(user):
            #return self.start_session(user)
            #return self.requestOTP()
        self.start_session(user, False)
        return self.requestOTP()
        
        # throw error
        #return jsonify({"error:" "Signup failed"}), 400

    def signout(self):
        session.clear()
        return redirect(url_for("homePage"))

    def login(self):
        # check for user email in db and if password matches

        # login user validation
        login_email = escape(request.form.get('email'))
        
        if re.match("^[a-zA-Z0-9@_.-]+$", login_email) == None:
            return jsonify({"error": "Please input a valid email"}), 400
            
        user = db.User.find_one({"email": login_email})

        #if user['failed_logins'] == 5 :
        #    return jsonify({"error": "Too many failed attempts" }), 401

        ## request.form.get('password') is un-encrypted
        ## user['password'] is encrypted
        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            self.start_session(user, False)
            return self.requestOTP()
            #return self.start_session(user)

        # db.User.update_one(
        #    {'email': request.form.get('email')},
        #    {'$inc': 
        #        {'failed_logins': 1}}
        #)

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
