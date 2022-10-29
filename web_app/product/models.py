from flask import Flask, jsonify, request, session, redirect, url_for, flash
import uuid
from db import db
import os
import cloudinary as cloud
import cloudinary.uploader
from werkzeug.utils import secure_filename
from tokenize import String

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


class Product:
    def uploadProduct(self):

        # check if user is logged in
        if session['logged_in'] == True:

            # check request if it is POST
            if request.method == "POST":
                if 'file' not in request.files:
                    flash('No file part')
                    return redirect(url_for("uploadListing"))
                file = request.files['file']
                print(secure_filename(file.filename))
                if file.filename == '':
                    flash('No image selected for uploading')
                    return redirect(url_for("uploadListing"))

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
                    return redirect(url_for("dashboard"))
                else:
                    flash('Allowed image types are - png, jpg, jpeg, gif')
                    return redirect(url_for("uploadListing"))

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

