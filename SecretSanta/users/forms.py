from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_login import current_user

from SecretSanta.models import User


# Form for registration
class RegistrationForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(),
                                       Length(min=2, max=12)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = StringField("Password",
                           validators=[DataRequired(),
                                       Length(min=4, max=12)])
    confirm_password = StringField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password"),
            Length(min=4, max=12)
        ],
    )
    submit = SubmitField("SUBMIT")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already taken.')


# Form for login
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = StringField("Password",
                           validators=[DataRequired(),
                                       Length(min=4, max=12)])
    remember = BooleanField("REMEMBER ME")
    submit = SubmitField("LOG IN")


# Form for update
class UpdateForm(FlaskForm):
    username = StringField("Username",
                           validators=[DataRequired(),
                                       Length(min=2, max=12)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    picture = FileField(
        'Update Profile Picture',
        validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    submit = SubmitField("UPDATE")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is already taken.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is already taken.')


class RequestResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("REQUEST PASSWORD RESET")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no matching account for the email')


class ResetPassWordForm(FlaskForm):
    password = StringField("Password",
                           validators=[DataRequired(),
                                       Length(min=4, max=12)])
    confirm_password = StringField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password"),
            Length(min=4, max=12)
        ],
    )
    submit = SubmitField("RESET PASSWORD")


class DrawForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("JOIN THE SHUFFLE")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Your email does not match')