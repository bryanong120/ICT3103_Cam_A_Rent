from flask import Flask, jsonify, render_template, request, url_for, session, redirect, session
import os
from pymongo import MongoClient
import db

app = Flask(__name__)
app.secret_key = "apple1234"

# Connection to mongo database


@app.route('/test', methods=['POST', 'GET'])
def MongoDB():
    db.db.User.insert_one({"email": "jon@gmail.com"})
    return "I am connected to db!"


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
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


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
