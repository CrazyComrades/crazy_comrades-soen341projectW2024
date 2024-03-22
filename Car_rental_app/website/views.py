from flask import Blueprint, render_template,request, jsonify
from .models import Vehicle,Branch
from flask import send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional
from sqlalchemy import or_
from flask_login import current_user, login_required


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

