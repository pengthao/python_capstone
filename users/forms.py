from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email
from model import User


class LoginForm(FlaskForm):
    email = StringField('email: ', validators=[DataRequired(), Email()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Log in')

class RegistrationForm(FlaskForm):
    username = StringField('username: ', validators=[DataRequired()])
    email = StringField('email: ', validators=[DataRequired(), Email()])
    password = PasswordField('Password: ', validators=[DataRequired(),EqualTo('pass_confirm', message='Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password: ', validators=[DataRequired()])
    submit = SubmitField('Register!')


    def check_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already taken. Try again')
    
    def check_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Email already taken. Try again')

class searchForm(FlaskForm):
    search_term = StringField('Search: ', validators=[DataRequired()])
    search_location = StringField('Location: ', validators=[DataRequired()])
    search_radius = IntegerField('Search Radius: ', validators=[DataRequired()])
    submit = SubmitField('submit')