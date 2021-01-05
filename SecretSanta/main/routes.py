from flask import render_template, request, Blueprint

main = Blueprint('main', __name__)


# Main page
@main.route("/")
def home():
    return render_template("home.html", title="Home")


# About page
@main.route("/about")
def about():
    return render_template("about.html", title="About")


# Contact page
@main.route("/contact")
def contact():
    return render_template("contact.html", title="Contact")