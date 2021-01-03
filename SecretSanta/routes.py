from flask import render_template, flash, redirect, url_for, request, abort
from SecretSanta import app, db, bcrypt
from SecretSanta.forms import (RegistrationForm, LoginForm, PostForm,
                               UpdateForm, RequestResetForm, ResetPassWordForm)
from SecretSanta.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

from SecretSanta.functions import save_pic
from SecretSanta import mail


# Main page
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Count Down")


# Shuffle page
@app.route("/join")
def join():
    return render_template("join.html", title="Join")


# About page
@app.route("/about")
def about():
    return render_template("about.html", title="About")


# Thanks posting page
@app.route("/thanks")
def thanks():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,
                                                                  per_page=12)
    return render_template("thanks.html", title="Thanks", posts=posts)


# Contact page
@app.route("/contact")
def contact():
    return render_template("contact.html", title="Contact")


# Register page
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
        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form=form)


# Login page
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


# Log out page
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


# Profile page
@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    image_file = url_for('static',
                         filename='profile_pics/' + current_user.image_file)
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_pic(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Account has been updated')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("profile.html",
                           title="Profile",
                           image_file=image_file,
                           form=form)


# User's posts page
@app.route("/user/<string:username>")
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


# Create new post page
@app.route("/thanks/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data,
                    author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Post has been created !')
        return redirect(url_for('thanks'))
    return render_template("new_post.html",
                           title="New Post",
                           form=form,
                           legend='New Post')


# View post by id page
@app.route("/thanks/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


# Update post by id page
@app.route("/thanks/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('new_post.html',
                           title='Update Post',
                           form=form,
                           legend='Update Post')


# Delete post by id page
@app.route("/thanks/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f'Post has been deleted !')
    return redirect(url_for('thanks'))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='no-reply@sneakyelf.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{ url_for('reset_token',token=token,_external=True) }

If you did not make this request please ignore this email and no changes will be made
    '''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instruction to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_request.html',
                           title='Reset Password',
                           form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
        return redirect(url_for('login'))
    return render_template('reset_token.html',
                           title='Reset PassWord',
                           form=form)
