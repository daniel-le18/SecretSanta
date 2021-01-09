from flask import render_template, Blueprint

main = Blueprint('main', __name__)
from SecretSanta.main.forms import ContactForm


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
@main.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
    return render_template("contact.html", title="Contact", form=form)
