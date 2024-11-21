#!/usr/bin/python3
import os 
from flask import Flask
from config import Config
from models import db, bcrypt, User, Department, Message  # Import models to create tables
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///message_name.db'

    #app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate = Migrate(app, db)  # Add database migrations support

    # Register the main blueprint
    from routes import main
    app.register_blueprint(main)

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')

