from flask import session, redirect, url_for
from functools import wraps


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("homePage"))
    return wrap

def login_not_required(f): #if user is logged in, redirects user back to home page
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return redirect(url_for("homePage"))
        else:
            return f(*args, **kwargs)
    return decorated_function