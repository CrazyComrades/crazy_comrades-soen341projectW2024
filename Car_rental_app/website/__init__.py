from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_mail import Mail
from datetime import datetime
class MainIndexLink(MenuLink):
    def get_url(self):
        return url_for("views.home")

db = SQLAlchemy()
admin = Admin(name='My Admin Panel', template_mode='bootstrap4')
admin.add_link(MainIndexLink(name="Get Back to the Main Site"))
DB_NAME = "database.db"
login_manager = LoginManager()
mail = Mail()

def str_to_datetime(value):
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'crazycomradessoen@gmail.com'
    app.config['MAIL_PASSWORD'] = 'dzly lcrz qcdb ftol'
    app.config['MAIL_DEFAULT_SENDER'] = 'crazycomradessoen@gmail.com'
    app.jinja_env.filters['str_to_datetime'] = str_to_datetime

    db.init_app(app)
    admin.init_app(app)
    mail.init_app(app)
    

    

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


