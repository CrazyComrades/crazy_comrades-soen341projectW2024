from sqlalchemy import func
from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    role = db.Column(db.String(150))
    reservations = db.relationship('Reservation')
    

class Vehicle(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    type_car = db.Column(db.String(150))
    brand = db.Column(db.String(150))
    car_model = db.Column(db.String(150))
    year = db.Column(db.Integer)
    price = db.Column(db.Double)
    mileage = db.Column(db.Integer)
    availability = db.Column (db.Boolean)

    
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checkin = db.Column(db.DateTime(timezone=True), default=func.now())
    checkout = db.Column(db.DateTime(timezone=True), default=func.now())
    final_price = db.Column(db.Double)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'))
    vehicle_price = db.Column(db.Integer, db.ForeignKey('vehicle.price'))
    vehicle_avail = db.Column(db.Integer, db.ForeignKey('vehicle.availability'))



