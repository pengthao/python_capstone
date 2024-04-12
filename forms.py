from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class searchForm(FlaskForm):
    search_term = StringField('Search: ', validators=[DataRequired()], render_kw={"placeholder": "Keywords"}, description='search_term')
    search_location = StringField('Location: ', validators=[DataRequired()], render_kw={"placeholder": "Location"}, description='search_location')
    search_radius = IntegerField('Location: ', validators=[DataRequired()], render_kw={"placeholder": "Radius"}, description='search_radius')
    submit = SubmitField('submit')