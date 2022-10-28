from flask import Flask, jsonify, render_template, request, url_for, session, redirect, session
from functools import wraps
import db
import os
from user.models import User
from product.models import Product

app = Flask(__name__)
app.secret_key = "b'Y\x1alF\x01\xe8i\xcaM\x93\x052\xbd\x1f[\x99'"

# Decorators (logic to check if a user is signed in if not redirect to home page)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("home"))
    return wrap


@app.route('/user/signup/', methods=['POST'])
def signup():
    return User().signup()


@app.route('/user/login/', methods=['POST'])
def login():
    return User().login()


@app.route('/user/signout/', methods=['POST'])
def signout():
    return User().signout()


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/user/uploadListing/', methods=['POST'])
def uploadListing():
    return Product().uploadListing()


@ app.route('/uploadListing/',)
@ login_required
def uploadListingPage():
    return render_template('uploadListing.html')


@ app.route('/dashboard/')
@ login_required
def dashboard():
    return render_template('dashboard.html')


@ app.route('/signup/', methods=['GET'])
def signupPage():
    return render_template('signup.html')


@ app.route('/login/', methods=['GET'])
def loginPage():
    return render_template('login.html')


def create_app():
    return app
