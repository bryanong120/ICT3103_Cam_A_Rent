from flask import Blueprint, render_template, request, escape, flash
from product.models import Product
import re

product_bp = Blueprint("product_bp", __name__,
                       static_folder='static', template_folder='templates')


@product_bp.route("/overview/", methods=['POST', 'GET'])
def viewAllProduct():
    productlist = Product().showAllProduct()
    return render_template("allProductView.html", product=list(productlist))


@product_bp.route('/search/', methods=['POST', 'GET'])
def search():
    search_Text = escape(request.form["searchText"])
    if re.match("^[a-zA-Z0-9]+$", search_Text) == None:
        flash("Error: Only alphanumeric allowed")
        return render_template("allProductView.html")
    # search_Text = request.args.get("searchText")
    searched_Product = Product().searchProduct(search_Text)
    return render_template("allProductView.html", product=list(searched_Product))
