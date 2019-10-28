from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


from .config import DevelopmentConfig

db = SQLAlchemy()
login = None

def create_app():
    global login

    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(DevelopmentConfig)
    db.init_app(app)
    login = LoginManager(app)

    with app.app_context():

        # Imports
        from . import routes

        # Create tables for our models
        db.create_all()

        return app