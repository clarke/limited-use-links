from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, HiddenField
from wtforms.validators import DataRequired, Regexp
from datetime import datetime


class LinkForm(FlaskForm):
    original_url = StringField('original_url', validators=[DataRequired()])
    visits_allowed = StringField('visits_allowed', default=1)


class LinkDeleteForm(FlaskForm):
    link_id = HiddenField('link_id', validators=[DataRequired()])
