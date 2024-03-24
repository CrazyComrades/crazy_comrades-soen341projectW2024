from sqlalchemy import func
from . import db, admin
from flask_login import UserMixin, LoginManager, current_user
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for, current_app
from flask_admin.form.upload import FileUploadField
from wtforms.fields import FileField
from wtforms.validators import DataRequired
from datetime import datetime
from sqlalchemy.orm import relationship





class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    role = db.Column(db.String(150))
    reservation = db.relationship("Reservation", back_populates="user")
    def __str__(self):
        return self.name

class DamageReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    description = db.Column(db.String(255))


    
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checkin = db.Column(db.DateTime(timezone=True), default=func.now())
    checkout = db.Column(db.DateTime(timezone=True), default=func.now())
    final_price = db.Column(db.Float)
    location = db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Specify foreign key relationship
    user = db.relationship("User", back_populates="reservation", foreign_keys=[user_id])
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    vehicle_price = db.Column(db.Float)
    vehicle_avail = db.Column(db.Boolean)
    email_res = db.Column(db.String(150))
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    branch = relationship('Branch', primaryjoin='Reservation.branch_id == Branch.id')

    
class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    # Define backref in the Branch class
    vehicles = db.relationship('Vehicle', backref='branch_ref', lazy=True)
    def __str__(self):
        return self.location

class Vehicle(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    type_car = db.Column(db.String(150))
    brand = db.Column(db.String(150))
    car_model = db.Column(db.String(150))
    year = db.Column(db.Integer)
    price = db.Column(db.Float)
    mileage = db.Column(db.Integer)
    availability = db.Column(db.Boolean)
    image = db.Column(db.String(255))
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))

class Payment(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    card_number = db.Column(db.Integer)
    expiry_date = db.Column(db.String(150))
    cvv = db.Column(db.Integer)
    name_on_card = db.Column(db.String(150))
    billing_adress = db.Column(db.String(150))

   



class RentalAgreement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservation.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    duration = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    pick_up_location = db.Column(db.String(255), nullable=False)
    drop_off_location = db.Column(db.String(255), nullable=False)
    additional_services = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    reservation = db.relationship('Reservation', backref=db.backref('rental_agreement', uselist=False), lazy=True)
    user = db.relationship('User', backref=db.backref('rental_agreements', lazy=True))



class ReservationView(ModelView):
    form_columns = ["checkin", "checkout", "final_price", "user", "vehicle_id", "vehicle_price", "vehicle_avail", "branch"]
    
    def is_accessible(self):
        return current_user.is_authenticated and (current_user.role == 'Admin' or current_user.role == 'Reservation Representative')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))
    
class PaymentView(ModelView):
    form_columns = ["card_number", "cvv", "expiry_date"]
    
    def is_accessible(self):
        return current_user.is_authenticated and (current_user.role == 'Admin' or current_user.role == 'Reservation Representative')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))

class Controller(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'Admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))

class VehicleView(ModelView):
    form_extra_fields = {
        'image': FileUploadField(
            label='Image',
            base_path='C:/Users/dawis/crazy_comrades-soen341projectW2024/Car_rental_app/website/car_images/Car_rental_app/website',
            relative_path='Car_rental_app/website/car_images/Car_rental_app/website',
            validators=[DataRequired()],
            allowed_extensions=['jpg', 'png']
        )
    }
    

    def is_accessible(self):
        return current_user.is_authenticated and (current_user.role == 'Admin' or current_user.role == 'Reservation Representative')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))

admin.add_view(Controller(User, db.session))
admin.add_view(Controller(Branch, db.session))
admin.add_view(ReservationView(Reservation, db.session))
admin.add_view(VehicleView(Vehicle, db.session))
admin.add_view(PaymentView(Payment, db.session))






    



