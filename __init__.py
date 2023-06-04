from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db=SQLAlchemy()
DB_NAME='db.database'  # can name anything you want

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='anything you want'  # Encrypts/secures cookies or session data
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # will store the database
                                                   # where __init__.py is located
    db.init_app(app)    # initialises the database, and says will work on app

    from .views import views  # we need to register our views here
    from .auth import auth

    app.register_blueprint(views,url_prefix='/') # we don't want any prefixes to the url.
    app.register_blueprint(auth,url_prefix='/') # if we do put anything, like '/something' it will mean that 
                                                # if we want to access a specific route, say
                                                # auth here, then whatever we might have written
                                                # @auth.route('here') we have to call by /something/here

    from .models import User,Note  # makes sure that the models file is running

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # where to go if user isn't logged in
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/'+DB_NAME):  # checking if db already exists, no need to tamper if it does already exist
        db.create_all(app=app) # we are saying which app is being created
        print('Database created successfully')
