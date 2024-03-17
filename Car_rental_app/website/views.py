from flask import Blueprint, render_template
from .models import Vehicle
from flask import send_from_directory

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")
    
@views.route('/reservation')
def reservation():
    return render_template("reservation.html")    


@views.route('/admin1')
def admin():
    return render_template("admin1.html")    

@views.route('/browse')
def vehicles():
    vehicles = Vehicle.query.all()
    return render_template('browse.html', vehicles=vehicles)

@views.route('/car_images/Car_rental_app/website/<path:filename>')
def car_images(filename):
    return send_from_directory('C:/Users/dawis/crazy_comrades-soen341projectW2024/Car_rental_app/website/car_images/Car_rental_app/website', filename)