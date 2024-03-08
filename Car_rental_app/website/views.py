from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")
    
@views.route('/reservations')
def reservation():
    return render_template("base.html")    

@views.route('/browse')
def browse():
    return render_template("browse.html")   