#Importing
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path

DB_NAME = "ElimSys.db"
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'abcdef'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/', name = "views")
    app.register_blueprint(auth, url_prefix = '/')

    from .models import Administrators, Teams, Competitors
    with app.app_context():
        db.create_all()
        db.session.commit()
        print('Database created successfully.')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    
    @login_manager.user_loader
    def load_user(id):
        return Administrators.query.get(int(id))
    return app