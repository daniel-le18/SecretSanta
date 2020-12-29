from flask import render_template, flash, redirect, url_for
from SecretSanta import app
from SecretSanta.forms import RegistrationForm, LoginForm
from SecretSanta.models import User, Post


# Main
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Count Down")


@app.route("/secretsanta")
def secretsanta():
    return render_template("secret.html", title="Secret Santa")


@app.route("/thanks")
def thanks():
    return render_template("thanks.html", title="Thanks")


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data} !')
        return redirect(url_for('home'))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@gmail.com' and form.password.data == 'testing':
            flash(f'You have been logged in !')
            return redirect(url_for('home'))
        else:
            flash(f'Login unsucessfully. Please check again!')
    return render_template("login.html", title="Log In", form=form)
