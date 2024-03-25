from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import Reservation, Vehicle, User, Payment
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

    return redirect(url_for('res.process_payment', total_price=total_price))
    
    

def send_confirmation_email(reservation):
    # Construct email message
    msg = Message('Reservation Confirmation', recipients=[reservation.email_res])
    msg.body = f"Your reservation details:\nLocation: {reservation.location}\nCheck-in: {reservation.checkin}\nCheck-out: {reservation.checkout}\nReservation ID: {reservation.id}\nVehicle Price per day: ${reservation.vehicle_price}\nFinal Price: ${reservation.final_price}"
    mail.send(msg)

@res.route('/success')
def success():
    flash ("Reservation submitted successfully!The payment has been accepted An email has been sent to you with the confirmation of your reservation !")
    return render_template("home.html")


@res.route('/process_payment', methods=["GET","POST"])
def process_payment():
    if request.method == "POST":
        # Retrieve form fields
        card_number = request.form.get('card_number')
        expiry_date = request.form.get('expiry_date')
        cvv = request.form.get('cvv')
        name_on_card = request.form.get('name_on_card')
        billing_address = request.form.get('billing_address')
        total_price = request.form.get('total_price')

        # Check if any required form field is missing
        if None in (card_number, expiry_date, cvv, name_on_card, billing_address, total_price):
            flash('Please fill out all required fields.')
            return redirect(url_for('res.process_payment'))

        # Create a new Payment object
        new_payment = Payment(
            card_number=card_number,
            expiry_date=expiry_date,
            cvv=cvv,
            name_on_card=name_on_card,
            billing_address=billing_address,
            total_price=total_price
        )

        # Add the new_payment to the database
        db.session.add(new_payment)
        db.session.commit()

        flash('Payment successful.')
        return redirect(url_for('res.success'))

# If it's a GET request, render the payment form
    total_price = request.args.get('total_price')
    return render_template('payment_form.html', total_price=total_price)

