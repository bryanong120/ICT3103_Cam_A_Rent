from flask import jsonify, request, session, redirect, url_for, flash
from passlib.hash import pbkdf2_sha256
import uuid
from db import db
from tokenize import String
import cloudinary as cloud
import cloudinary.uploader
from werkzeug.utils import secure_filename
# status code 200 = OK request fulfilled
# status code 400 = BAD request
# status code 401 = Unauthorized entry

# cloudinary
cloud.config(
    cloud_name="ds5ib7aij",
    api_key="867155213339131",
    api_secret="yt-vTKEI9Ad0p-fsI5emvfSqudE"
)

UPLOAD_FOLDER = 'product/UPLOAD_FOLDER'
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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
        if session['logged_in'] == True:
            user = session['user']
            user_product = db.Product.find({"uid": user['_id']})
            return user_product

    def delListing(self, productID: String):
        return db.Product.delete_one({"_id": productID})

##################################################################################################################################


class Product:
    def uploadProduct(self):

        # check if user is logged in
        if session['logged_in'] == True:

            # check request if it is POST
            if request.method == "POST":
                if 'file' not in request.files:
                    flash('No file part')
                    return redirect(url_for("user_bp.uploadListing"))
                file = request.files['file']
                print(secure_filename(file.filename))
                if file.filename == '':
                    flash('No image selected for uploading')
                    return redirect(url_for("user_bp.uploadListing"))

                # check if image file is in acceptable format png, jpeg, jpg
                if file and allowed_file(file.filename):
                    upload_result = cloud.uploader.upload(file)
                    product = {
                        "_id": uuid.uuid4().hex,
                        "uid": session['user']['_id'],
                        "title": request.form.get('title'),
                        "dayPrice": request.form.get('dayPrice'),
                        "weekPrice": request.form.get('weekPrice'),
                        "monthPrice": request.form.get('monthPrice'),
                        "stock": request.form.get('stock'),
                        "category": request.form.get('category'),
                        "image_url": upload_result['secure_url'],
                        "description": (request.form.get('description')).strip()
                    }
                    db.Product.insert_one(product)
                    flash('Image successfully uploaded')
                    return redirect(url_for("user_bp.dashboardPage"))
                else:
                    flash('Allowed image types are - png, jpg, jpeg, gif')
                    print("not acceptable!")
                    return redirect(url_for("user_bp.uploadListing"))

    def showAllProduct(self):
        return db.Product.find()

    def homePageProduct(self):
        return db.Product.find(limit=9)

    def viewProduct(self, productID: String):
        # oid = ObjectId(productID)
        return db.Product.find_one({"_id": productID})

    def viewProductUsername(self, productID: String):
        product = db.Product.find_one({"_id": productID})
        return db.User.find_one({"_id": product["uid"]})

    def searchProduct(self, searchText: String):
        return db.Product.find({"$text": {"$search": searchText}})
