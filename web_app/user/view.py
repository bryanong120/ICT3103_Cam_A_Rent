from flask import Blueprint, render_template, request, redirect, url_for
from user.models import User
from product.models import Product
from decorator import login_required

user_bp = Blueprint("user_bp", __name__,
                    static_folder='static', template_folder='templates')


@user_bp.route("/signup/", methods=['POST'])
def signup():
    return User().signup()


@user_bp.route("/login/", methods=['POST'])
def login():
    return User().login()


@user_bp.route("/signout/", methods=['GET', 'POST'])
def signout():
    return User().signout()


@user_bp.route("/dashboard/", methods=['GET', 'POST'])
@login_required
def dashboardPage():
    return render_template('dashboard.html')


@user_bp.route('/delListing/', methods=['POST'])
@login_required
def delListing():
    if request.method == 'POST':
        object_id = request.form['delObjID']
        User().delListing(object_id)
        return redirect(url_for('user_bp.viewListing'))
    else:
        return redirect(url_for('user_bp.viewListing'))


@user_bp.route('/viewListing/', methods=['POST', 'GET'])
@login_required
def viewListing():
    userProductList = User().viewListing()
    return render_template('listing.html', userProducts=list(userProductList))


@user_bp.route('/uploadListing/', methods=['POST', 'GET'])
@ login_required
def uploadListing():
    if request.method == "POST":
        Product().uploadProduct()
        return render_template('uploadListing.html')
    else:
        return render_template('uploadListing.html')
