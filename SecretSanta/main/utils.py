from flask_mail import Message
from SecretSanta import mail
import os


def send_mail(email, name, message):
    recipient = os.environ.get('recipient')
    msg = Message('Contact Me',
                  sender='no-reply@sneakyelf.com',
                  recipients=[recipient])
    msg.body = f'''Name: {name}
Email: {email}
Message: {message}'''
    mail.send(msg)