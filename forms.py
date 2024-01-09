from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, IntegerField
from wtforms.validators import DataRequired
from wtforms.validators import NumberRange
from wtforms import SelectField
from datetime import datetime as dt


class TodoForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    author = TextAreaField('author', validators=[DataRequired()])
    year = IntegerField('year', validators=[NumberRange(min=-5000,
                                                        max=dt.today().year)])
    number_of_pages = IntegerField('number_of_pages',
                                   validators=[DataRequired()])
    language = SelectField('language', choices=['Polski', 'Angielski'])
    form_of = SelectField('form_of', choices=['Papierowa', 'Ebook'])
    genre = TextAreaField('genre', validators=[DataRequired()])
    done = BooleanField('done')
