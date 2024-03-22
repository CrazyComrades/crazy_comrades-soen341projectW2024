from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Reservation
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if (user.password == password):
                login_user(user)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect email or password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(name) < 2:
            flash('First name must be greater than 1 character.', category='error')   
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, name=name, password=
                password, role = 'user')
            db.session.add(new_user)
            db.session.commit()
            
            flash('Account created!', category='success')
            login_user(new_user)
            
            return redirect(url_for('views.home'))
    
    return render_template("register.html", user=current_user)
@auth.route('/my_reservations')
@login_required
def my_reservations():
    # Query reservations associated with the current user
    reservations = Reservation.query.filter_by(user=current_user).all()
    return render_template('myres.html', reservations=reservations)