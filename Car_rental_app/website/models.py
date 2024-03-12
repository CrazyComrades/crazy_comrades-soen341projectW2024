from sqlalchemy import func
from . import db, admin
from flask_login import UserMixin, LoginManager, current_user
from flask_admin.contrib.sqla import ModelView
from flask import redirect, url_for

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    role = db.Column(db.String(150))
    reservation = db.relationship("Reservation", back_populates="user")
    def __str__(self):
        return self.name
        
    
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checkin = db.Column(db.DateTime(timezone=True), default=func.now())
    checkout = db.Column(db.DateTime(timezone=True), default=func.now())
    final_price = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Specify foreign key relationship
    user = db.relationship("User", back_populates="reservation")
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    vehicle_price = db.Column(db.Float)
    vehicle_avail = db.Column(db.Integer)


class Vehicle(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    type_car = db.Column(db.String(150))
    brand = db.Column(db.String(150))
    car_model = db.Column(db.String(150))
    year = db.Column(db.Integer)
    price = db.Column(db.Double)
    mileage = db.Column(db.Integer)
    availability = db.Column (db.Boolean)

class ReservationView(ModelView):
    form_columns = ["checkin", "checkout", "final_price", "user", "vehicle_id", "vehicle_price", "vehicle_avail"]
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
    def is_accessible(self):
        return current_user.is_authenticated and (current_user.role == 'Admin' or current_user.role == 'Reservation Representative')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))

admin.add_view(Controller(User, db.session))
admin.add_view((Reservation, db.session))
admin.add_view(VehicleView(Vehicle, db.session))




    



