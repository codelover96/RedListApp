import os.path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'redlist.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'VJwrDxGxslqGvlouPjAw'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from app.views import views
    from app.auth import auth
    from app.controllers import controllers
    from app.models import User, Species, Habitat, Threat, ThreatenedBy, Inhabits

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(controllers, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    with app.app_context():
        create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(_id):
        return User.query.get(int(_id))

    return app


def create_database(app):
    base_path = "D:/Programming/Python/RedListApp/instance"
    db_path = base_path + "/" + DB_NAME
    print(db_path)

    if not path.exists(db_path):
        db.create_all()
        create_users()
        print('Database Created!')


def create_users():
    from app.models import User
    from werkzeug.security import generate_password_hash

    admin1 = User(email="admin@gmail.com", password=generate_password_hash(
        "admin", method='sha256'), role="admin")
    db.session.add(admin1)
    user1 = User(email="user@gmail.com", password=generate_password_hash(
        "user", method='sha256'), role="user")
    db.session.add(user1)
    db.session.commit()
    print("USER CREDENTIALS:")
    print("'username : password'")
    print("user@gmail.com : user")
    print("admin@gmail.com : admin")
