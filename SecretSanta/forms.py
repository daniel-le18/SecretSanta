from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
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
