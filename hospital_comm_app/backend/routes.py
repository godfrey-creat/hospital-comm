from flask import Blueprint, request, jsonify
from models import db, User, Message, bcrypt
import jwt

main = Blueprint('main', __name__)

@main.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = jwt.encode({'user_id': user.id}, "SECRET_KEY", algorithm='HS256')
        return jsonify({'token': token})
    return jsonify({'message': 'Invalid credentials'}), 401

# Add more routes for sending messages, fetching departments, etc.

