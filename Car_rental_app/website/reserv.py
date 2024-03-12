from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Reservation
from . import db

res = Blueprint('res', __name__)

@res.route('/submit_reservation', methods=['POST'])
def submit_reservation():
    location = request.form['location']
    checkin_str = request.form['checkin']
    checkout_str = request.form['checkout']
    user_id = request.form['email']
    checkin = datetime.strptime(checkin_str, '%Y-%m-%d')
    checkout = datetime.strptime(checkout_str, '%Y-%m-%d')
  
    new_reservation = Reservation(location=location, checkin=checkin, checkout=checkout, user_id =user_id)
   
    db.session.add(new_reservation)
    db.session.commit()
    
    return redirect(url_for('res.success'))

@res.route('/success')
def success():
    flash ("Reservation submitted successfully!")
    return render_template("home.html")