from flask import Flask, render_template, request
from user.view import user_bp
from product.view import product_bp
from product.models import Product
from csrf import csrf

app = Flask(__name__, instance_relative_config=False)

app.config.update(
    TESTING=True,
    SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
)
csrf.init_app(app)

# routes


@ app.route("/signup/", methods=['GET'])
def signupPage():
    return render_template('signup.html')


@ app.route("/login/", methods=['GET'])
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
    app.secret_key = "b'Y\x1alF\x01\xe8i\xcaM\x93\x052\xbd\x1f[\x99'"
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(product_bp, url_prefix='/product')
    return app
