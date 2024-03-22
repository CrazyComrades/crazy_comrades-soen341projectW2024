from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from .models import Reservation, Vehicle, User
from . import db,mail
from flask_mail import Mail,Message

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
    user = User.query.get_or_404(user_id)

    email_res = user.email



    duration = (checkout - checkin).days
    vehicle_price = float(vehicle.price)
    total_price = duration * vehicle_price
    
    new_reservation = Reservation(location=location, checkin=checkin, email_res=email_res,checkout=checkout, vehicle_id=vehicle_id,user_id=user_id,vehicle_price=vehicle.price, final_price=total_price)
   
    db.session.add(new_reservation)
    db.session.commit()
    send_confirmation_email(new_reservation)
    
    return redirect(url_for('res.success'))

def send_confirmation_email(reservation):
    # Construct email message
    msg = Message('Reservation Confirmation', recipients=[reservation.email_res])
    msg.body = f"Your reservation details:\nLocation: {reservation.location}\nCheck-in: {reservation.checkin}\nCheck-out: {reservation.checkout}\nVehicle ID: {reservation.vehicle_id}\nVehicle Price: {reservation.vehicle_price}\nFinal Price: {reservation.final_price}"
    mail.send(msg)

@res.route('/success')
def success():
    flash ("Reservation submitted successfully! An email has been sent to you with the confirmation of your reservation !")
    return render_template("home.html")

@res.route('/process_payment', methods=['POST'])
def process_payment():
    # Payment processing logic
    return 'Payment processed successfully'
