from flask import render_template, flash, redirect, url_for, request, abort
from SecretSanta import app, db, bcrypt
from SecretSanta.forms import RegistrationForm, LoginForm, PostForm, UpdateForm
from SecretSanta.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

from PIL import Image
import secrets
import os


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
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,
                                                                  per_page=12)
    return render_template("thanks.html", title="Thanks", posts=posts)


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


def save_pic(form_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics',
                                picture_fn)
    output_size = (125, 125)
    i = Image.open(form_pic)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


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


@app.route("/thanks/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


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
