from flask import render_template, Blueprint, redirect, flash, url_for
from SecretSanta import create_app, db

main = Blueprint('main', __name__)

from SecretSanta.models import User
from SecretSanta.main.forms import ContactForm
from SecretSanta.main.utils import send_mail


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


# About page
@main.route("/participants")
def participants():
    participants = User.query.filter_by(isJoined=True).all()
    # for participant in participants:
    #     print(participant.username)
    return render_template("participants.html",
                           title="Participants",
                           participants=participants)


# Contact page
@main.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        message = form.message.data
        if form.submit.data:
            send_mail(email, name, message)
            flash(f'Thank you, I will get back to you as soon as possible !')
            return redirect(url_for('main.home'))
    return render_template("contact.html", title="Contact", form=form)


# Services page
@main.route("/services")
def services():
    return render_template("services.html", title="Rules")
