from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,TextAreaField, IntegerField
from wtforms.validators import DataRequired
from wtforms.fields import DateTimeLocalField

class PickUpForm(FlaskForm):
    reservation_id = StringField('Reservation ID', validators=[DataRequired()])
    driver_license = StringField('Driver\'s License Number', validators=[DataRequired()])
    credit_card = StringField('Credit Card Number', validators=[DataRequired()])
    submit = SubmitField('Submit')
class PickUpForm2(FlaskForm):
    reservation_id = IntegerField('Reservation ID', validators=[DataRequired()])
    drop_off_time = DateTimeLocalField('Drop-off Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    damages = StringField('Damages')
    drop_off_location = StringField('Drop-off Location')
    additional_services = StringField('Additional Services')
    submit = SubmitField('Submit')
class RentalAgreementForm(FlaskForm):
    damages = TextAreaField('Report Damages (if any)')
    submit = SubmitField('Submit Rental Agreement')