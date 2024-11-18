from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

# Initialize database and bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    is_department_head = db.Column(db.Boolean, default=False)

    # Relationships
    department = db.relationship('Department', back_populates='members')
    sent_messages = db.relationship('Message', back_populates='sender', lazy=True)

    def __repr__(self):
        return f"<User(username={self.username}, is_admin={self.is_admin}, department_id={self.department_id})>"

class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    # Relationships
    members = db.relationship('User', back_populates='department', lazy=True)
    messages = db.relationship('Message', back_populates='department', lazy=True)

    def __repr__(self):
        return f"<Department(name={self.name})>"

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    sender = db.relationship('User', back_populates='sent_messages')
    department = db.relationship('Department', back_populates='messages')

    def __repr__(self):
        return f"<Message(sender_id={self.sender_id}, department_id={self.department_id}, content={self.content})>"

