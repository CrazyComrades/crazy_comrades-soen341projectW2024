from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Reservation, Vehicle
from . import db

res = Blueprint('res', __name__)

@res.route('/submit_reservation', methods=['POST'])
def submit_reservation():
    location = request.form['location']
    checkin_str = request.form['checkin']
    checkout_str = request.form['checkout']
    user_id = request.form['user_id']
    checkin = datetime.strptime(checkin_str, '%Y-%m-%d')
    checkout = datetime.strptime(checkout_str, '%Y-%m-%d')
    vehicle_id = request.form['vehicle_id']
    
    vehicle = Vehicle.query.get_or_404(vehicle_id)

    duration = (checkout - checkin).days
    vehicle_price = float(vehicle.price)
    total_price = duration * vehicle_price
    
    new_reservation = Reservation(location=location, checkin=checkin, checkout=checkout, vehicle_id=vehicle_id,user_id=user_id,vehicle_price=vehicle.price, final_price=total_price)
   
    db.session.add(new_reservation)
    db.session.commit()
    
    return redirect(url_for('res.success'))

@res.route('/success')
def success():
    flash ("Reservation submitted successfully!")
    return render_template("home.html")

