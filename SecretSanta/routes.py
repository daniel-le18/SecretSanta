from flask import render_template, flash, redirect, url_for, request
from SecretSanta import app, db, bcrypt
from SecretSanta.forms import RegistrationForm, LoginForm
from SecretSanta.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data} !')
        return redirect(url_for('home'))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(
                url_for('home'))
        else:
            flash(f'Login unsucessfully. Please check again!')
    return render_template("login.html", title="Log In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", title="Profile")
