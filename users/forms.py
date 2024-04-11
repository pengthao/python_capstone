from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, IntegerField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email
from model import User, UserJob


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

class updateStatus(FlaskForm):
    status_choices = [(choice, choice) for choice in ['Interested', 'Applied', 'Accepted', 'Not Interested']]
    status = SelectField('Status: ', validators=[DataRequired()], choices=status_choices)
    submit = SubmitField('Update')

    '''def __init__(self, *args, **kwargs):
        super(updateStatus, self).__init__(*args, **kwargs)
        enum_choices = [(choice.name, choice.value) for choice in UserJob.status.property.columns[0].type.enums]
        self.status.choices = enum_choices'''