from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_ckeditor import CKEditor

# setting up a database
db = SQLAlchemy()
DB_NAME = "database.db"

ckeditor = CKEditor()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'a secret string'
    app.app_context().push()

    # database config
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    #ckeditor
    ckeditor.init_app(app)


    # before creating a database you need to import the model we created at models.py
    from .models import User, Post, Comment

    # create database
    create_database(app)

    # setting up flask login manager
    login_manager = LoginManager()
    login_manager.login_view = "auth.login" # redirect anon user who tries to see a page that have login_required.
    login_manager.init_app(app)

    @login_manager.user_loader # user loader login
    def load_user(id):
        return User.query.get(int(id))


    # the dot is because you are importing stuff from a python package init website folder
    from .views import views
    app.register_blueprint(views, url_prefix="/")

    from .auth import auth
    app.register_blueprint(auth, url_prefix="/")

    return app

def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all()
        print("Created database")