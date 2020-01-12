from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LicensePlateForm(FlaskForm):
    licensePlate = StringField('License Plate', validators=[DataRequired()])
    submit = SubmitField('Check for validity')
