from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")
    
@views.route('/reservation')
def reservation():
    return render_template("reservation.html")    


@views.route('/admin')
def admin():
    return render_template("admin.html")    

@views.route('/browse')
def browse():
    return render_template("browse.html")    