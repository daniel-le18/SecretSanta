from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from SecretSanta import db, bcrypt
from SecretSanta.models import User, Post
from SecretSanta.users.forms import (RegistrationForm, LoginForm, UpdateForm,
                                     RequestResetForm, ResetPassWordForm,
                                     DrawForm)
from SecretSanta.users.utils import get_random_user, save_pic, send_email, send_reset_email
users = Blueprint('users', __name__)


# Register page
# Take all information from html's Register form and put them into database
# Hash password before putting in
@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password,
                    wish=form.wish.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data} !')
        return redirect(url_for('users.login'))
    return render_template("register.html", title="Register", form=form)


# Login page
# Take all the information users put in from html's Login form
# Check the input with the database, checking password by checking with hased password
@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(
                url_for('main.home'))
        else:
            flash(f'Login unsucessfully. Please check again!')
    return render_template("login.html", title="Log In", form=form)


# Log out page
# Using flask_login logout_user
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


# Profile page
# TODO: prevent users from changing information after joining
@users.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    image_file = url_for('static',
                         filename='profile_pics/' + current_user.image_file)
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_pic(form.picture.data)
            current_user.image_file = picture_file

        # Make changes to database from form
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Account has been updated')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("profile.html",
                           title="Profile",
                           image_file=image_file,
                           form=form)


# User's posts page
# Take out posts by user by query the posts with the user relationship
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()

    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page,per_page=12)
    return render_template("user_posts.html",
                           title="User Post",
                           posts=posts,
                           user=user)


# Reset page
# Take in input using htlm form RequestResetForm
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instruction to reset your password')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',
                           title='Reset Password',
                           form=form)


# Reset the password using token
# Take in token and check if token is valid
# Then reset the password (hash it before)
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash(f'Invalid or expired token')
        return redirect('reset_request.html')
    form = ResetPassWordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Password has been updated !')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',
                           title='Reset PassWord',
                           form=form)


# Shuffle page
@users.route("/join", methods=['GET', 'POST'])
@login_required
def join():
    form = DrawForm()
    if form.validate_on_submit():
        if current_user.isJoined == True:
            flash(f'You have already joined !')
        else:
            random_user = get_random_user()
            if random_user is None:
                flash(f'Not enough participants, please join later !')
                return redirect(url_for('main.home'))
            else:
                # send_email(current_user, random_user)
                secret_santa = f'''{random_user.username}'''
                wish = f'''{random_user.wish}'''
                return render_template("result.html",
                                       result=[secret_santa, wish],
                                       legend="RESULT")
    return render_template("join.html",
                           title="Join",
                           form=form,
                           legend="JOIN SECRET SANTA")
