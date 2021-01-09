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


# Rules page
@main.route("/rules")
def rules():
    return render_template("rules.html", title="Rules")


# Contact page
@main.route("/contact")
def contact():
    return render_template("contact.html", title="Contact")
