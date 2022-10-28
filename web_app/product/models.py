from flask import Flask, jsonify, request, session, redirect, url_for, flash
import uuid
from db import db
import os
import cloudinary as cloud
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]


class Product:
    def uploadListing(self):
        if session['logged_in'] == True:
            if 'img' not in request.files:
                print("gg")
                return redirect(url_for("uploadListing"))
            image = request.files['img']
            # check if image is in correct format
            if image and image.filename.split(".")[-1].lower in ALLOWED_EXTENSIONS:
                filename = secure_filename(image.filename)
                image.save(os.path.join("product/UPLOAD_FOLDER", filename))
                # create product object
                product = {
                    "_id": uuid.uuid4().hex,
                    "uid": session['user']['_id'],
                    "title": request.form.get('title'),
                    "dayPrice": request.form.get('dayPrice'),
                    "weekPrice": request.form.get('weekPrice'),
                    "monthPrice": request.form.get('monthPrice'),
                    "stock": request.form.get('stock'),
                    "category": request.form.get('category'),
                    "filename": filename,
                    "description": (request.form.get('description')).strip()
                }
                db.Product.insert_one(product)
                flash("Succesfully uploaded image!", "success")
                return jsonify(product), 200

            flash("Invalid product inputs!", "danger")
            return jsonify({"error": "Invalid product inputs!"}), 400
