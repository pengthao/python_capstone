from flask_wtf import FlaskForm
from flask_login import current_user
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
    search_term = StringField('Search: ', validators=[DataRequired()], render_kw={"placeholder": "Enter search term"}, description='search_term')
    search_location = StringField('Location: ', validators=[DataRequired()], render_kw={"placeholder": "Enter location"}, description='search_location')
    search_radius = IntegerField('Search Radius: ', validators=[DataRequired()], render_kw={"placeholder": "Radius"}, description='search_radius')
    submit = SubmitField('submit')

def status_choices():
    status_choices = [(choice, choice) for choice in ['Interested', 'Applied', 'Accepted', 'Not Interested']]
    return status_choices

class updateStatus(FlaskForm):
    
    status = SelectField('Status: ', choices=status_choices())
    submit = SubmitField('Update')

    def set_default_status(self, job_id):
            user_id = current_user.get_id()
            saved_job = UserJob.query.filter_by(user_id=user_id, job_result_id=job_id).first()
            if saved_job:
                self.status.data = saved_job.status

    
