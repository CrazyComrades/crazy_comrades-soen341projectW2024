from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_admin import Admin

db = SQLAlchemy()
admin = Admin(name='My Admin Panel', template_mode='bootstrap4')
DB_NAME = "database.db"
login_manager = LoginManager()



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    admin.init_app(app)

    

    from .views import views
    from .auth import auth
    from .reserv import res

    app.register_blueprint(res, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Vehicle, Reservation
    
    create_database(app)

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


    return app



def create_database(app):
    with app.app_context():
        if not path.exists('website/' + DB_NAME):
            db.create_all()
            print('Created Database!')


