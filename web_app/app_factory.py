from flask import Flask, jsonify, render_template, request, url_for, session, redirect, session
import os
from pymongo import MongoClient
import db

app = Flask(__name__)
app.secret_key = "apple1234"

# Connection to mongo database


@app.route('/test', methods=['POST', 'GET'])
def MongoDB():
    return "I am connected to db!"


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('home.html')


@app.route('/signup/', methods=['POST', 'GET'])
def signup():
    return render_template('signup.html')


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        user = request.form["email"]
        session["user"] = user
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template('login.html')


@app.route('/user', methods=['POST', 'GET'])
def user():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}<h1>"
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


def create_app():
    return app
