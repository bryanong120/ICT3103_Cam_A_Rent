from flask import Flask, jsonify, render_template, request, url_for, session, redirect, session
from functools import wraps
from db import db
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


@app.route('/user/signout/', methods=['POST', 'GET'])
def signout():
    return User().signout()


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        object_id = request.form['objectID']
        single_product = Product().viewProduct(object_id)
        single_username = Product().viewProductUsername(object_id)
        return render_template('productDetails.html', single_product=list([single_product]), single_username=list([single_username]))
    else:
        productlist = Product().homePageProduct()
        return render_template("home.html", product=list(productlist))


@ app.route('/user/uploadListing', methods=['POST', 'GET'])
@ login_required
def uploadListing():
    Product().uploadProduct()
    return render_template('uploadListing.html')


@app.route('/uploadListing/', methods=['GET'])
@login_required
def uploadListingPage():
    return render_template('uploadListing.html')


@app.route('/listing', methods=['POST', 'GET'])
@login_required
def listingPage():
    userProductList = User().viewUserListing()
    return render_template('listing.html', userProducts=list(userProductList))


@app.route('/user/delListing', methods=['POST'])
@login_required
def delProduct():
    if request.method == 'POST':
        object_id = request.form['delObjID']
        User().delProduct(object_id)
        return redirect(url_for("listingPage"))
    else:
        return redirect(url_for("listingPage"))


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
