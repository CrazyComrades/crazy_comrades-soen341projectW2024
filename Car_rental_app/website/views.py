from flask import Blueprint, render_template,request, jsonify
from .models import Vehicle,Branch
from flask import send_from_directory

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

@views.route('/branch/<int:branch_id>/cars')
def branch_cars(branch_id):
    branch = Branch.query.get_or_404(branch_id)
    cars = Vehicle.query.filter_by(branch_id=branch_id, availability=True).all()
    return render_template('branch_cars.html', branch=branch, cars=cars)



@views.route('/search_cars', methods=['GET'])
def search_cars():
    branch_id = request.args.get('branch_id')
    car_type = request.args.get('car_type')
    # Other search criteria

    # Query cars based on selected branch and search criteria
    available_cars = Vehicle.query.filter_by(branch_id=branch_id, type_car=car_type).all()  # Example query

    # Serialize car data and return as JSON response
    car_data = [{'id': car.id, 'type_car': car.type_car, 'brand': car.brand} for car in available_cars]
    return jsonify(car_data)

@views.route('/admin')
def admin():
    return render_template("admin.html")    

@views.route('/myreservation')
def myres():
    return render_template("myres.html")

@views.route('/browse')
def vehicles():
    vehicles = Vehicle.query.all()
    return render_template('browse.html', vehicles=vehicles)

@views.route('/car_images/Car_rental_app/website/<path:filename>')
def car_images(filename):
    return send_from_directory('C:/Users/dawis/crazy_comrades-soen341projectW2024/Car_rental_app/website/car_images/Car_rental_app/website', filename)