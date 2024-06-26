from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Vehicle,Branch, Reservation, DamageReport, RentalAgreement
from flask import send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional
from sqlalchemy import or_
from . import db,mail   ##means from __init__.py import db
from .forms import PickUpForm, PickUpForm2
from datetime import datetime
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Mail,Message

from flask import render_template, request
from sqlalchemy import func
from datetime import datetime
from .models import RentalAgreement
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
            confirmation = False  

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
        rental_agreement.confirmation = True  # Update confirmation status
        db.session.commit()

        flash('Agreement confirmed successfully, A deposit of 500 CAD has been credited. You are free to drive away', 'success')
        return redirect(url_for('views.home'))  # Redirect to the homepage after confirmation

    return render_template('rental_agreement_details.html', rental_agreement=rental_agreement, vehicle=vehicle, renter=renter)

@views.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        reservation_id = request.form['reservation_id']
        drop_off_location = request.form['drop_off_location']
        return_date = datetime.strptime(request.form['return_date'], '%Y-%m-%d')
        
        # Retrieve reservation based on ID
        reservation = Reservation.query.get_or_404(reservation_id)
        
        # Update rental agreement with drop-off location and return date
        rental_agreement = RentalAgreement.query.filter_by(reservation_id=reservation.id).first()
        rental_agreement.drop_off_location = drop_off_location
        rental_agreement.drop_off_time = return_date
        rental_agreement.checkout_confirmation = False  # Reset confirmation status
        db.session.commit()
        
        flash('Checkout submitted. Awaiting confirmation from the reservation representative.', 'success')
        return redirect(url_for('views.home'))

    return render_template('checkout.html')

    
@views.route('/rep_checkout/<int:rental_agreement_id>', methods=['GET', 'POST'])
def rep_checkout(rental_agreement_id):
    rental_agreement = RentalAgreement.query.get_or_404(rental_agreement_id)

    if request.method == 'POST':
        # Assuming you have a form with fields for damages, deposit deduction, and confirmation
        damages = request.form['damages']
        deposit_deduction = request.form['deposit_deduction']
        checkout_confirmation = request.form.get('confirmation')

        # Update rental agreement with confirmation and any deductions made
        rental_agreement.damages = damages
        rental_agreement.deposit_deduction = deposit_deduction

        if checkout_confirmation == 'confirmed':
            rental_agreement.checkout_confirmation = True
            # Send email notification to renter about the confirmation and deductions
            send_confirmation_email(rental_agreement)
            vehicle = rental_agreement.reservation.vehicle
            vehicle.availability = True
            flash('Checkout confirmed. An email has been sent to the renter.', 'success')
        else:

            rental_agreement.checkout_confirmation = True
            send_confirmation_email(rental_agreement)
            vehicle = rental_agreement.reservation.vehicle
            vehicle.availability = True
            flash('Checkout confirmed. Please review the damages and deductions in you email.', 'error')

        db.session.commit()

        return redirect(url_for('views.home'))

    return render_template('rep_checkout.html', rental_agreement=rental_agreement)

def send_confirmation_email(rental_agreement):
    
    # Retrieve the reservation associated with the rental agreement
    reservation = rental_agreement.reservation
    
    # Retrieve the renter's email from the reservation
    renter_email = reservation.user.email

    rental_agreement.deposit_deduction = int(request.form['deposit_deduction'])
    
    # Render the email template with necessary details
    subject = "Confirmation of Car Rental Agreement"
    recipients = [renter_email]

    # Send the email
    msg = Message(subject, recipients=recipients)
    msg.body = f"You have been succesfully checkout!\n Reservation ID: {reservation.id}!\n A total of ${rental_agreement.deposit_deduction} has been deducted from your deposit.\n You will then receive confirmation from your bank that you will be receiving {500-rental_agreement.deposit_deduction}.\n Thank you for doing business with us! \nIf you have been deducted money the damages will appear below :\n {rental_agreement.damages}  "
    mail.send(msg)

from flask import render_template

@views.route('/checkout_requests', methods=['GET'])
def checkout_requests():
    # Query all rental agreements pending checkout confirmation
    pending_checkouts = RentalAgreement.query.filter_by(checkout_confirmation=False).all()
    return render_template('list_checkouts.html', pending_checkouts=pending_checkouts)




@views.route('/admin/sales', methods=['GET', 'POST'])
def admin_sales():
    if request.method == 'POST':
        month = int(request.form['month'])
        year = int(request.form['year'])
        
        # Calculate start and end dates of the specified month
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month, 1).replace(month=month+1) if month < 12 else datetime(year, 12, 31)
        
        # Query confirmed rental agreements within the specified month
        rental_agreements = RentalAgreement.query.filter(
            RentalAgreement.confirmation == True,
            RentalAgreement.created_at >= start_date,
            RentalAgreement.created_at <= end_date
        ).all()
        
        # Calculate total sales
        total_sales = sum(agreement.price for agreement in rental_agreements)
        
        # Pass rental agreements data to the template context
        return render_template('admin_sales.html', total_sales=total_sales, month=month, year=year, rental_agreements=rental_agreements, datetime = datetime)
    
    return render_template('sales_select_month_year.html',datetime = datetime)
