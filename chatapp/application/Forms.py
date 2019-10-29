from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired,Length, ValidationError, EqualTo
from wtforms.fields.html5 import DateField
from .models import Messages, Users


class AddingMessage(FlaskForm):
    body = StringField("Description",validators=[DataRequired(),Length(min=3, max=8000 )])
    submit = SubmitField('Add')

class LoginForm (FlaskForm) :
    email = StringField ('Username' , validators=[DataRequired ()])
    password = PasswordField ('Password' , validators=[DataRequired ()])
    remember_me = BooleanField ('Remember Me')
    submit = SubmitField ('Sign In')


class RegistrationForm(FlaskForm):
    first_name = StringField ('First name' , validators=[DataRequired ()])
    last_name = StringField ('First name' , validators=[DataRequired ()])
    email = StringField ('email' , validators=[DataRequired ()])
    password = PasswordField ('Password' , validators=[DataRequired ()])
    password2 = PasswordField (
        'Repeat Password' , validators=[DataRequired () , EqualTo ('password')])
    remember_me = BooleanField ('Remember Me')
    submit = SubmitField ('Sign In')


    def validate_username (self , username):
        user = Users.query.filter_by (username=username.data).first ()
        if user is not None :
            raise ValidationError ('Please use a different username.')

    def validate_email (self , email) :
        user = Users.query.filter_by (email=email.data).first ()
        if user is not None :
            raise ValidationError ('Please use a different email address.')
