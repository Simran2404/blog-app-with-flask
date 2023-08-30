from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint("views", __name__)

# the routes indicate the type of url that takes us to home.html
@views.route("/")
def base():
    return render_template("base.html", name="guest")
@views.route("/home")
def home():
    return render_template("home.html", name=current_user.username)