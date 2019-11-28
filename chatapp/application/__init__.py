import flask_migrate
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from oauthlib.oauth2 import WebApplicationClient


from .config import DevelopmentConfig

db = SQLAlchemy()
login = None
oauth_client = None


def create_app():
    global login

    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    migrate = Migrate (app , db)
    login = LoginManager(app)
    login.login_view = 'login'
    login.login_message_category = 'info'

    # OAuth 2 client setup
    oauth_client = WebApplicationClient(app.config ['GOOGLE_CLIENT_ID'])


    with app.app_context():

        # Imports
        from . import routes

        # Create tables for our models
        db.create_all()

        return app


