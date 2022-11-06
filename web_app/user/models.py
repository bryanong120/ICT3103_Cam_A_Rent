from datetime import datetime, timedelta
from flask import jsonify, request, session, redirect, url_for, flash, escape
from passlib.hash import pbkdf2_sha256
import uuid
import re
from db import db
from tokenize import String
import logging
from otpverify import requestPhoneOTP,checkPhoneOTP,requestEmailOTP,checkEmailOTP

# status code 200 = OK request fulfilled
# status code 400 = BAD request
# status code 401 = Unauthorized entry
logger = logging.getLogger('werkzeug') # grabs underlying WSGI logger
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('user.log') # creates handler for the log file
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler) # adds handler to the werkzeug WSGI logger


class User:
        
    def start_session(self, user, verified):
        if 'password' in user:
            del user['password']
            
        session['user'] = user
        
        #Checks if user has passed the otp verification
        if verified:
            session['logged_in'] = True
            return jsonify(user), 200
        else:
            session['logged_in'] = False
            return
           
    def requestOTP(self):
        user = session['user']
        phone = user['phone']
        if user['verified']:
            logger.info("OTP sent to %s", phone)
            
            requestPhoneOTP(phone)
            return jsonify(True), 200
        else:
            email = user['email']
            logger.info("OTP sent to %s and %s", phone, email)
            
            requestPhoneOTP(phone)
            requestEmailOTP(email)
            return jsonify(True), 200
        
    def verifyOTP(self):
        phoneotp = escape(request.form.get('phoneotp'))
        if re.match("^[\d]+$", phoneotp) == None:
            return jsonify({"error": "Please input valid phone OTP"}), 400
        
        emailotp = escape(request.form.get('emailotp'))
        if re.match("^[\d]+$", emailotp) == None:
            return jsonify({"error": "Please input valid email OTP"}), 400
            
        user = session['user']
        phone = user['phone']
        email = user['email']
        if checkPhoneOTP(phone, phoneotp) and checkEmailOTP(email, emailotp):
            logger.info("%s has verified their account", email)
            db.User.update_one(
                {'email': email},
                {
                '$set': 
                    {'verified': True}
                }
            )
            return self.start_session(user, True)
        
        return jsonify({"error": "Incorrect code submitted"}), 400
        
    def loginOTP(self):
        phoneotp = escape(request.form.get('phoneotp'))
        if re.match("^[\d]+$", phoneotp) == None:
            return jsonify({"error": "Please input valid phone OTP"}), 400
        
        user = session['user']
        phone = user['phone']
        
        if checkPhoneOTP(phone, phoneotp):
            logger.info("%s has logged in.", user['email'])
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
        phone = escape(request.form.get('phone'))
        phone = phone.replace(' ','')
        if re.match("^\+[\d]+$", phone) == None:
            return jsonify({"error": "Please input valid phone number with country code +65"}), 400

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

        if email in password:
            return jsonify({"error": "Password cannot contain your email"}), 400

        # create the user objectusername = escape(request.form.get('username'))



        # create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "username": username,
            "email": email,
            "phone": phone,
            "password": password,
            "virtualCredit": 1000,
            "failed_logins": 0,
            "last_failed": datetime.utcnow(),
            "verified" : False
        }

        # encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

       
        # insert user if there is no existing email
        if db.User.insert_one(user):
            logger.info("Username: %s and Email: %s created ", username, email)
            self.start_session(user, False)
            return self.requestOTP()
            #return self.start_session(user, True)

        # throw error
        return jsonify({"error:" "Signup failed"}), 400

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

        if user:
            if (user['failed_logins'] == 5) and (datetime.utcnow() < user['last_failed'] + timedelta(minutes=5)):
                logger.warning("%s has been locked for 5 minutes for too many failed attempts", login_email)
                return jsonify({"error": "Too many failed attempts, please wait 5 minutes before attempting, any earlier than that will result in the lock timer resetting!" }), 401

            ## request.form.get('password') is un-encrypted
            ## user['password'] is encrypted
            if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
                db.User.update_one(
                    {'email': request.form.get('email')},
                    {'$set':
                        {'failed_logins': 0}}
                        )
                self.start_session(user, False)
                return self.requestOTP()

            db.User.update_one(
                {'email': request.form.get('email')},
                {
                '$inc': 
                    {'failed_logins': 1},
                '$set': 
                    {'last_failed': datetime.utcnow()}
                }
            )
            logger.info("%s has failed to login %d times.", login_email, user['failed_logins']+1)
            return jsonify({"error": "Invalid login credentials"}), 401

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
            
