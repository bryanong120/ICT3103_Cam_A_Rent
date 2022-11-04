from itertools import product
from flask import Blueprint, render_template, request, redirect, url_for
from user.models import User
from product.models import Product
from decorator import login_required

user_bp = Blueprint("user_bp", __name__,
                    static_folder='static', template_folder='templates')


    
@user_bp.route("/signup/", methods=['POST'])
def signup():
    if request.form.get('sendphoneotp') == 'sendphoneotop':
        return User().sendPhoneOTP()
    elif request.form.get('sendemailotp') == 'sendemailotp':
        return User().sendEmailOTP()
    else:
        return User().sendhelp()
    #return User().signup()
    
@user_bp.route("/sendPhoneOTP/", methods=['POST'])
def sendPhoneOTP():
    return User().sendPhoneOTP()
    
@user_bp.route("/sendEmailOTP/", methods=['POST'])
def sendEmailOTP():
    return User().sendEmailOTP()


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


@user_bp.route('/editListing/', methods=['POST', 'GET'])
@login_required
def editListing():
    if request.method == 'POST':
        object_id = request.form['editObjID']
        single_product = Product().viewProduct(object_id)
        return render_template('editListing.html', single_product=list([single_product]))


@user_bp.route('/updateListing/', methods=['POST', 'GET'])
@login_required
def updateListing():
    if request.method == 'POST':
        object_id = request.form['updateObjID']
        Product().updateProduct(object_id)
        single_product = Product().viewProduct(object_id)
        return render_template('editListing.html', single_product=list([single_product]))


@user_bp.route('/viewListing/', methods=['POST', 'GET'])
@login_required
def viewListing():
    userProductList = User().viewListing()
    return render_template('listing.html', userProducts=list(userProductList))


@user_bp.route('/uploadListing/', methods=['POST', 'GET'])
@login_required
def uploadListing():
    if request.method == "POST":
        Product().uploadProduct()
        return render_template('uploadListing.html')
    else:
        return render_template('uploadListing.html')

@user_bp.route('/deposit', methods=['POST'])
@login_required
def deposit():
    productObj = Product().viewProduct(request.form['depositPID'])
    single_username = Product().viewProductUsername(request.form['depositPID'])
    User().deductDeposit(productObj)
    return render_template('productDetails.html', single_product = list([productObj]), single_username=list([single_username]))
        
        
