from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


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


# Form for login
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = StringField("Password",
                           validators=[DataRequired(),
                                       Length(min=4, max=12)])
    remember = BooleanField("REMEMBER ME")
    submit = SubmitField("LOG IN")
