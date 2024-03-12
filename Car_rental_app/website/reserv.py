from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Reservation, Vehicle
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

res = Blueprint('res', __name__)

@res.route('/submit_reservation', methods=['POST'])
def submit_reservation():
    location = request.form['location']
    checkin_str = request.form['checkin']
    checkout_str = request.form['checkout']
    
    checkin = datetime.strptime(checkin_str, '%Y-%m-%d')
    checkout = datetime.strptime(checkout_str, '%Y-%m-%d')
    # Create a new reservation object
    new_reservation = Reservation(location=location, checkin=checkin, checkout=checkout)
    
    # Add the new reservation to the database
    db.session.add(new_reservation)
    db.session.commit()
    
    # Redirect to a success page or wherever appropriate
    return redirect(url_for('res.success'))

@res.route('/success')
def success():
    flash ("Reservation submitted successfully!")
    return render_template("home.html")