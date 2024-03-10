from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    role = db.Column(db.String(150))

class Vehicle(db.Model): 
    id = db.Column(db.Integer, primary_key=True)                                                                              
    
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
