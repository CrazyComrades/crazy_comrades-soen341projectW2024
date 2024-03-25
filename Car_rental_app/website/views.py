from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Vehicle,Branch, Reservation, DamageReport, RentalAgreement
from flask import send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional
from sqlalchemy import or_
from . import db   ##means from __init__.py import db
from .forms import PickUpForm, PickUpForm2
from datetime import datetime
from flask_login import login_user, login_required, logout_user, current_user
# Custom filter to convert string to datetime


# Add custom filter to Jinja environment

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")
    
@views.route('/reservation', methods=['GET'])
def reservation():
    vehicle_id = request.args.get('vehicle_id')
    user_id = request.args.get('user_id')
    return render_template("reservation.html",vehicle_id=vehicle_id,user_id = user_id)    

@views.route('/branches')
def branches():
    branches = Branch.query.all()
    return render_template('branches.html', branches=branches)

class CarFilterForm(FlaskForm):
    type_car = StringField('Type')
    brand = StringField('Brand')
    car_model = StringField('Model')
    year = IntegerField('Year', validators=[Optional()])
    price = IntegerField('Price', validators=[Optional()])
    mileage = IntegerField('Mileage', validators=[Optional()])
    availability = BooleanField('Available')
    submit = SubmitField('Filter')

@views.route('/branch/<int:branch_id>', methods=['GET', 'POST'])
def branch_cars(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    form = CarFilterForm()
    cars_query = Vehicle.query.filter_by(branch_id=branch_id, availability=True)

    if request.method == 'POST' and form.validate_on_submit():
        type_car = form.type_car.data
        brand = form.brand.data
        car_model = form.car_model.data
        year = form.year.data
        price = form.price.data
        mileage = form.mileage.data
        availability = form.availability.data

        # Apply filter conditions
        if type_car:
            cars_query = cars_query.filter(Vehicle.type_car.like(f'%{type_car}%'))
        if brand:
            cars_query = cars_query.filter(Vehicle.brand.like(f'%{brand}%'))
        if car_model:
            cars_query = cars_query.filter(Vehicle.car_model.like(f'%{car_model}%'))
        if year:
            cars_query = cars_query.filter_by(year=year)
        if price:
            cars_query = cars_query.filter_by(price=price)
        if mileage:
            cars_query = cars_query.filter_by(mileage=mileage)
        if availability:
            cars_query = cars_query.filter_by(availability=True)

    # Execute the query to get the filtered cars
    cars = cars_query.all()

    return render_template('branch_cars.html', branch=branch, cars=cars, form=form)

@views.route('/clientreservation')
def resforclient():
    return render_template("resforclient.html")
@views.route('/admin')
def admin():
    return admin.index()


@views.route('/browse')
def vehicles():
    vehicles = Vehicle.query.all()
    return render_template('browse.html', vehicles=vehicles)

@views.route('/car_images/Car_rental_app/website/<path:filename>')
def car_images(filename):
    return send_from_directory('C:/Users/dawis/crazy_comrades-soen341projectW2024/Car_rental_app/website/car_images/Car_rental_app/website', filename)

@views.route('/pick-up', methods=['GET', 'POST'])
def pick_up():
    if current_user.is_authenticated:
        form = PickUpForm()
        if form.validate_on_submit():
            reservation_id = int(form.reservation_id.data)
            
            # Retrieve the user's reservations
            user_reservations = current_user.reservation
            
            # Check if any reservation matches the entered ID
            matching_reservation = next((r for r in user_reservations if r.id == reservation_id), None)
            
            if matching_reservation:
                current_user.driver_license = form.driver_license.data
                db.session.commit()  # Commit the changes
                return redirect(url_for('views.pick_up_car', reservation_id=reservation_id))  # Pass reservation_id
            else:
                flash('You do not have a reservation with that ID.', 'error')
                return redirect(url_for('views.pick_up'))  # Redirect back to the pick-up page
        return render_template('pick_up_form.html', form=form)
    else:
        flash('Please log in to pick up a car.', 'error')
        return redirect(url_for('login'))

@views.route('/pick_up_car/<int:reservation_id>', methods=['GET', 'POST'])
def pick_up_car(reservation_id):
    form = PickUpForm2()
    reservation = Reservation.query.get_or_404(reservation_id)  # Retrieve reservation based on ID
    
    if form.validate_on_submit():
        # Get reservation ID from the form
        reservation_id = int(form.reservation_id.data)
        
        # Check if the user has a reservation with the entered ID
        if reservation.id != reservation_id:
            flash('Invalid reservation ID.', 'error')
            return redirect(url_for('views.pick_up_car', reservation_id=reservation.id))
        
        # Retrieve the associated vehicle based on the reservation's vehicle_id
        vehicle = Vehicle.query.get(reservation.vehicle_id)

        if not vehicle:
            flash('Vehicle associated with this reservation not found.', 'error')
            return redirect(url_for('views.home'))  # Redirect to home or appropriate page
        
        # Calculate duration
        pick_up_time = reservation.checkin
        drop_off_time = form.drop_off_time.data
        duration = drop_off_time - pick_up_time

        # Update vehicle availability and record any damages reported
        vehicle.availability = False
        db.session.commit()

        if form.damages.data:
            damage_report = DamageReport(
                reservation_id=reservation.id,
                vehicle_id=vehicle.id,
                description=form.damages.data
            )
            db.session.add(damage_report)
            db.session.commit()

        # Create rental agreement
        # Calculate duration in days
        duration_days = duration.days + duration.seconds / (3600 * 24)  # Convert timedelta to days
        price = vehicle.price * duration_days

        pick_up_location = reservation.location
        drop_off_location = form.drop_off_location.data
        additional_services = form.additional_services.data

        rental_agreement = RentalAgreement(
            reservation_id=reservation.id,
            user_id=current_user.id,
            duration=duration_days,
            price=price,
            pick_up_location=pick_up_location,
            drop_off_location=drop_off_location,
            additional_services=additional_services,
            created_at=datetime.now(),
            pick_up_time = pick_up_time,
            drop_off_time = drop_off_time,
            Confirmation = False  

        )
        db.session.add(rental_agreement)
        db.session.commit()

        flash('Car picked up successfully. Rental agreement created.', 'success')
        return redirect(url_for('views.rental_agreement_details', rental_agreement_id=rental_agreement.id))

    # Pass the reservation to the template context
    return render_template('pick_up_car.html', form=form, reservation=reservation)
from flask import request, flash, redirect, url_for

@views.route('/rental_agreement_details/<int:rental_agreement_id>', methods=['GET', 'POST'])
def rental_agreement_details(rental_agreement_id):
    rental_agreement = RentalAgreement.query.get_or_404(rental_agreement_id)
    vehicle = rental_agreement.reservation.vehicle
    renter = rental_agreement.reservation.user
    
    if request.method == 'POST':
        # Assuming you have a form with signature and date fields
        company_signature = request.form.get('company_signature')
        company_date = request.form.get('company_date')
        renter_signature = request.form.get('renter_signature')
        renter_date = request.form.get('renter_date')

        # Update database with confirmation
        # Assuming you have a column named 'confirmed' in your RentalAgreement model
        rental_agreement.Confirmation = True  # Update confirmation status
        db.session.commit()

        flash('Agreement confirmed successfully, A deposit of 500 CAD has been credited. You are free to drive away', 'success')
        return redirect(url_for('views.home'))  # Redirect to the homepage after confirmation

    return render_template('rental_agreement_details.html', rental_agreement=rental_agreement, vehicle=vehicle, renter=renter)

