import os
from flask import Flask
from flask_bcrypt import bcrypt
from flask_bcrypt import Bcrypt
from config import Config
from api.v1 import routes
from models.models import db
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///message_name.db'

    # Initialize extensions
    db.init_app(app)
    # bcrypt.init_app(app)
    migrate = Migrate(app, db)  # Add database migrations support

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    # Correctly assign the app instance
    app = create_app()
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )