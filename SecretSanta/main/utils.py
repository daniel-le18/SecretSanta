from flask_mail import Message
from SecretSanta import mail
import os
import smtplib


def send_mail(email, name, message):
    myemail = os.environ.get('email')
    mypassword = os.environ.get('password')
    reciepient = os.environ.get('recipient')
    print(myemail, mypassword, reciepient)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    try:
        server.starttls()
        server.login(myemail, mypassword)
        message = name + "\n" + email + "\n" + message
        server.sendmail(myemail, reciepient, message)
    except Exception as e:
        print(e)
    finally:
        server.quit()


#     recipient = os.environ.get('recipient')
#     msg = Message('Contact Me',
#                   sender='no-reply@sneakyelf.com',
#                   recipients=[recipient])
#     msg.body = f'''Name: {name}
# Email: {email}
# Message: {message}'''
#     mail.send(msg)