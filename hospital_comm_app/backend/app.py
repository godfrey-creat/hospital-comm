#!/usr/bin/python3
import os 
from flask import Flask
from config import Config
from api.v1.routes import routes
from models.models import db
#from hospital_comm_app.backend.models.models import db, bcrypt, User, Department, Message  # Import models to create tables
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
    #from hospital_comm_app.backend.api.v1.routes import main
    #app.register_blueprint(main)

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    create_db()
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )


