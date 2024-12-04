from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, SubmitField
from wtforms.validators import DataRequired, Optional

class EventForm(FlaskForm):
    title = StringField('Event Title', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    estimated_budget = FloatField('Estimated Budget', validators=[Optional()])
    actual_spent = FloatField('Actual Spent', validators=[Optional()])
    submit = SubmitField('Save')
