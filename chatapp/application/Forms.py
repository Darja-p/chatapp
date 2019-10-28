from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired,Length, ValidationError
from wtforms.fields.html5 import DateField
from .models import Messages


class AddingMessage(FlaskForm):
    body = StringField("Description",validators=[DataRequired(),Length(min=3, max=8000 )])
    submit = SubmitField('Add')


class LoginForm(FlaskForm):
    username = StringField ('Username' , validators=[DataRequired ()])
    password = PasswordField ('Password' , validators=[DataRequired ()])
    remember_me = BooleanField ('Remember Me')
    submit = SubmitField ('Sign In')