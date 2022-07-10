from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, MultipleFileField


class FileForm(FlaskForm):
    photo = MultipleFileField()
    visits_allowed = StringField('visits_allowed', default=1)
    comment = StringField('comment')
