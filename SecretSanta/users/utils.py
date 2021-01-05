import secrets
import os
from PIL import Image

from flask import current_app
from flask import url_for
from flask_mail import Message
from flask_login import current_user
from sqlalchemy.sql import func
from SecretSanta import mail, db
from SecretSanta.models import User


def save_pic(form_pic):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics',
                                picture_fn)
    output_size = (125, 125)
    i = Image.open(form_pic)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='no-reply@sneakyelf.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{ url_for('users.reset_token',token=token,_external=True) }

If you did not make this request please ignore this email and no changes will be made
    '''
    mail.send(msg)


def get_random_user():
    random_user = User.query.filter().order_by(func.random()).first()
    while current_user.email == random_user.email:
        random_user = User.query.filter().order_by(func.random()).first()
    current_user.isJoined = True
    db.session.commit()
    return random_user


def send_email(user, random_user):
    msg = Message('Secret Santa',
                  sender='no-reply@sneakyelf.com',
                  recipients=[user.email])
    msg.body = f'''You will be the Secret Santa of  {random_user.username}. You can contact them at
{random_user.email}'''
    mail.send(msg)