from flask import render_template, flash, redirect, url_for, request, abort, Blueprint
from flask_login import current_user, login_required
from SecretSanta import db
from SecretSanta.posts.forms import PostForm
from SecretSanta.models import Post

posts = Blueprint('posts', __name__)


# Wish posting page
@posts.route("/thanks")
def thanks():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,
                                                                  per_page=6)
    return render_template("thanks.html", title="Thanks", posts=posts)


# Create new post page
@posts.route("/thanks/new", methods=['GET', 'POST'])
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
        return redirect(url_for('posts.thanks'))
    return render_template("new_post.html",
                           title="New Post",
                           form=form,
                           legend='New Post')


# View post by id page
@posts.route("/thanks/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


# Update post by id page
@posts.route("/thanks/<int:post_id>/update", methods=['GET', 'POST'])
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
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('new_post.html',
                           title='Update Post',
                           form=form,
                           legend='Update Post')


# Delete post by id page
@posts.route("/thanks/<int:post_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f'Post has been deleted !')
    return redirect(url_for('main.thanks'))
