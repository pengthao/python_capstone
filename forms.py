from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class favorite(FlaskForm):
    favorite = SubmitField('Favorite')

class searchForm(FlaskForm):
    search_term = StringField('Search: ', validators=[DataRequired()])
    search_location = StringField('Location: ', validators=[DataRequired()])
    search_radius = IntegerField('Location: ', validators=[DataRequired()])
    submit = SubmitField('submit')