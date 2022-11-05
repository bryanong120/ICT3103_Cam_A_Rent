import os
from flask import Flask, render_template, request
from user.view import user_bp
from product.view import product_bp
from product.models import Product
from csrf import csrf
from dotenv import load_dotenv
from decorator import login_not_required
from flask_session import Session
from datetime import timedelta

load_dotenv()

app = Flask(__name__, instance_relative_config=False)

app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config.update(
    TESTING=True,    
    SECRET_KEY = os.getenv('SECRET_KEY_TESTING'),
    SESSION_COOKIE_SECURE=True, # Makes sure cookies can only be sent on HTTPS
    SESSION_COOKIE_HTTPONLY=True,# Mitigate client side scripts from accessing cookie
    SESSION_COOKIE_SAMESITE='Lax', #CSRF prevention
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30), # When Idle or not in use the session is set to expire in 30 mins
    SESSION_PERMANENT = True, # if the user is still using the app, carry on.
    SESSION_FILE_THRESHOLD = 100, # keeps up to 100 sessions before deleting some of it.
)

csrf.init_app(app)

@ app.route("/signup/", methods=['GET'])
@login_not_required
def signupPage():
    return render_template('signup.html')


@ app.route("/login/", methods=['GET'])
@login_not_required
def loginPage():
    return render_template('login.html')


@app.route("/", methods=['GET', 'POST'])
def homePage():
    if request.method == 'POST':
        object_id = request.form['objectID']
        single_product = Product().viewProduct(
            object_id)  # get the product to be viewed
        single_username = Product().viewProductUsername(
            object_id)  # get the User ID that product belongs to
        return render_template('productDetails.html', single_product=list([single_product]), single_username=list([single_username]))
    else:
        productlist = Product().homePageProduct()
        return render_template("home.html", product=list(productlist))


def create_app():
    app.secret_key = os.getenv('APP_SECRET_KEY')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(product_bp, url_prefix='/product')
    return app
