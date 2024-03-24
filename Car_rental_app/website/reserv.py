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
    
    # session['total_price']=total_price

    new_reservation = Reservation(location=location, checkin=checkin, email_res=email_res,checkout=checkout, vehicle_id=vehicle_id,user_id=user_id,vehicle_price=vehicle.price, final_price=total_price)
   
    db.session.add(new_reservation)
    db.session.commit()

    send_confirmation_email(new_reservation)

    return redirect(url_for('res.success'))
    
    # return redirect(url_for('res.process_payment'))

def send_confirmation_email(reservation):
    # Construct email message
    msg = Message('Reservation Confirmation', recipients=[reservation.email_res])
    msg.body = f"Your reservation details:\nLocation: {reservation.location}\nCheck-in: {reservation.checkin}\nCheck-out: {reservation.checkout}\nVehicle ID: {reservation.vehicle_id}\nVehicle Price: {reservation.vehicle_price}\nFinal Price: {reservation.final_price}"
    mail.send(msg)

@res.route('/success')
def success():
    flash ("Reservation submitted successfully!The payment has been accepted An email has been sent to you with the confirmation of your reservation !")
    return render_template("home.html")

# @res.route('/process_payment', methods=['GET','POST'])
# def process_payment():
#     total_price = session.get('total_price')
    
#     if request.method == 'POST':
#         card_number = request.form['card_number']
#         expiry_date = request.form['expiry_date']
#         cvv = request.form['cvv']
#         name_on_card = request.form['name_on_card']
#         billing_address = request.form['billing_address']

        
#     payment = Payment(
#             card_number=card_number,
#             expiry_date=expiry_date,
#             cvv=cvv,
#             name_on_card=name_on_card,
#             billing_address=billing_address,
#             total_price=total_price
#         )

#     db.session.add(payment)
#     db.session.commit()

#     payment_successful=True
    
#     if payment_successful:
    
#         reservation_id = request.form.get('reservation_id')
#         reservation = Reservation.query.get_or_404(reservation_id)
#         send_confirmation_email(reservation)
#         return redirect(url_for('res.success'))
#     else:
#         return flash('Please Try Again. The payment was unsuccessful.')
        

