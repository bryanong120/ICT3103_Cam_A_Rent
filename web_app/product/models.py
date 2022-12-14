from flask import jsonify, request, session, redirect, url_for, flash, escape
import os
import uuid
from db import db
import re
from tokenize import String
import cloudinary as cloud
import cloudinary.uploader
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import logging

load_dotenv()

# cloudinary
cloud.config(
    cloud_name=os.getenv('cloud_name'),
    api_key=os.getenv('api_key'),
    api_secret=os.getenv('api_secret')
)

UPLOAD_FOLDER = 'product/UPLOAD_FOLDER'
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])

logger = logging.getLogger('werkzeug') # grabs underlying WSGI logger
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('product.log') # creates handler for the log file
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler) # adds handler to the werkzeug WSGI logger

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
                    return redirect(url_for("user_bp.uploadListing"))
                file = request.files['file']
                print(secure_filename(file.filename))
                if file.filename == '':
                    flash('No image selected for uploading')
                    return redirect(url_for("user_bp.uploadListing"))
                # check if image file is in acceptable format png, jpeg, jpg
                if file and allowed_file(file.filename):
                    try:
                        upload_result = cloud.uploader.upload(file)
                    except Exception as e:
                        flash(e) # displays cloudinary.execeptions.error
                        return redirect(url_for("user_bp.uploadListing"))
                    title0 = escape(request.form.get('title'))
                    description0 = escape(request.form.get('description'))
                    product = {
                        "_id": uuid.uuid4().hex,
                        "uid": session['user']['_id'],
                        "title": title0,
                        "dayPrice": request.form.get('dayPrice'),
                        "weekPrice": request.form.get('weekPrice'),
                        "monthPrice": request.form.get('monthPrice'),
                        "initialDeposit": request.form.get('initialDeposit'),
                        "stock": request.form.get('stock'),
                        "category": request.form.get('category'),
                        "image_url": upload_result['secure_url'],
                        "description": description0.strip()
                    }
                    db.Product.insert_one(product)
                    logger.info("%s has uploaded product id: %s , titled %s", session['user']['username'], uuid.uuid4().hex, title0)
                    flash('Image successfully uploaded')
                    return redirect(url_for("user_bp.dashboardPage"))
                else:
                    flash('Allowed image types are - png, jpg, jpeg, gif')
                    print("not acceptable!")
                    return redirect(url_for("user_bp.uploadListing"))

    def updateProduct(self, productID: String):
        # check if user is logged in
        if session['logged_in'] == True:
            filter = {"_id": productID}
            # check request if it is POST
            if request.method == "POST":
                file = request.files['file']
                if file.filename == '':
                    title1 = escape(request.form.get('title'))
                    description1 = escape(request.form.get('description'))
                    product = {"$set":
                               {
                                   "title": title1,
                                   "dayPrice": request.form.get('dayPrice'),
                                   "weekPrice": request.form.get('weekPrice'),
                                   "monthPrice": request.form.get('monthPrice'),
                                   "stock": request.form.get('stock'),
                                   "category": request.form.get('category'),
                                   "description": description1.strip()
                               }
                               }
                    db.Product.update_one(filter, product)
                    logger.info("%s has updated product id: %s, titled %s", session['user']['username'], uuid.uuid4().hex, title1)
                    flash('Successfully updated')
                    return redirect(url_for("user_bp.updateListing"))
                else:
                    # check if image file is in acceptable format png, jpeg, jpg
                    if file and allowed_file(file.filename):
                        try:
                            upload_result = cloud.uploader.upload(file)
                        except Exception as err:
                            flash(err) # displays cloudinary.execeptions.error
                        title2 = escape(request.form.get('title'))
                        description2 = escape(request.form.get('description'))
                        product = {"$set":
                                    {
                                       "title": title2,
                                       "dayPrice": request.form.get('dayPrice'),
                                       "weekPrice": request.form.get('weekPrice'),
                                       "monthPrice": request.form.get('monthPrice'),
                                       "stock": request.form.get('stock'),
                                       "category": request.form.get('category'),
                                       "image_url": upload_result['secure_url'],
                                       "description": description2.strip()
                                   }
                        }
                        db.Product.update_one(filter, product)
                        flash('Image successfully uploaded')
                        return redirect(url_for("user_bp.updateListing"))
                    else:
                        flash('Allowed image types are - png, jpg, jpeg, gif')
                        return redirect(url_for("user_bp.updateListing"))

    def showAllProduct(self):
        return db.Product.find()

    def homePageProduct(self):
        return db.Product.find(limit=9)

    def viewProduct(self, productID: str):
        # oid = ObjectId(productID)
        return db.Product.find_one({"_id": productID})

    def viewProductUsername(self, productID: str):
        product = db.Product.find_one({"_id": productID})
        return db.User.find_one({"_id": product["uid"]})

    def searchProduct(self, searchText: str):
        return db.Product.find({"$text": {"$search": searchText}})
