from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


DB_NAME = 'redlist.db'
app = Flask(__name__)

app.config['SECRET_KEY'] = 'VJwrDxGxslqGvlouPjAw'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

db = SQLAlchemy(app)
db.init_app(app)


def create_app():
    from website.views import views
    from website.auth import auth
    from website.controllers import controllers

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(controllers, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from website.models import User, Species, Habitat, Threat, ThreatenedBy, Inhabits

    create_database()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(_id):
        return User.query.get(int(_id))

    return app


def create_database():
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        create_users()
        print('Database Created!')


def create_users():
    from website.models import User
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

