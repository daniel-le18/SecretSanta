from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Email, Length


# Form for contact
class ContactForm(FlaskForm):
    name = StringField("name",
                       validators=[DataRequired(),
                                   Length(min=2, max=12)])
    email = StringField("email", validators=[DataRequired(), Email()])

    message = TextAreaField("message",
                            validators=[DataRequired(),
                                        Length(min=5)])
    submit = SubmitField("SUBMIT")