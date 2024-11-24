from flask import Blueprint, request, jsonify, render_template
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from models.models import db, User, Department, Message
from forms.forms import RegisterAdminForm, LoginForm, CreateDepartmentForm, SendMessageForm
import jwt
from functools import wraps

main = Blueprint('main', __name__)

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, "SECRET_KEY", algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

# Route to register the first administrator
@main.route('/api/register_admin', methods=['GET', 'POST'])
def register_admin():
    form = RegisterAdminForm()
    if form.validate_on_submit():
        if User.query.filter_by(is_admin=True).first():
            return jsonify({'message': 'An administrator already exists!'}), 403

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_admin = User(username=form.username.data, password=hashed_password, is_admin=True)
        db.session.add(new_admin)
        db.session.commit()
        return jsonify({'message': 'Administrator registered successfully!'})
    return render_template('register_admin.html', form=form)

# Login route
@main.route('/api/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            token = jwt.encode({'user_id': user.id}, "SECRET_KEY", algorithm='HS256')
            return jsonify({'token': token})
        return jsonify({'message': 'Invalid credentials'}), 401
    return render_template('login.html', form=form)


# Route to create departments (accessible by admin only)
@main.route('/api/departments', methods=['GET', 'POST'])
@token_required
def create_department(current_user):
    if not current_user.is_admin:
        return jsonify({'message': 'Unauthorized access'}), 403

    form = CreateDepartmentForm()
    if form.validate_on_submit():
        department = Department(name=form.name.data)
        db.session.add(department)
        db.session.commit()
        return jsonify({'message': f'Department {department.name} created successfully'})
    return render_template('create_department.html', form=form)

# Route to add user to a department (admin only)
@main.route('/api/departments/<int:department_id>/users', methods=['POST'])
@token_required
def add_user_to_department(current_user, department_id):
    if not current_user.is_admin:
        return jsonify({'message': 'Unauthorized access'}), 403
    data = request.get_json()
    user = User(username=data['username'], password=bcrypt.generate_password_hash(data['password']).decode('utf-8'), department_id=department_id)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': f'User {user.username} added to department {department_id} successfully'})

@main.route('/api/departments/<int:department_id>/messages', methods=['GET', 'POST'])
@token_required
def handle_messages(current_user, department_id):
    if current_user.department_id != department_id and not current_user.is_admin:
        return jsonify({'message': 'Access denied'}), 403

    form = SendMessageForm()
    if form.validate_on_submit():
        message = Message(sender_id=current_user.id, department_id=department_id, content=form.content.data)
        db.session.add(message)
        db.session.commit()
        return jsonify({'message': 'Message sent successfully'})

    messages = Message.query.filter_by(department_id=department_id).all()
    messages_data = [{'sender': msg.sender_id, 'content': msg.content, 'timestamp': msg.timestamp} for msg in messages]
    return render_template('messages.html', form=form, messages=messages_data)

# Route to assign department head (admin only)
@main.route('/api/departments/<int:department_id>/assign_head', methods=['POST'])
@token_required
def assign_department_head(current_user, department_id):
    if not current_user.is_admin:
        return jsonify({'message': 'Unauthorized access'}), 403
    data = request.get_json()
    user = User.query.get(data['user_id'])
    if not user or user.department_id != department_id:
        return jsonify({'message': 'User not found or not in this department'}), 404
    user.is_department_head = True
    db.session.commit()
    return jsonify({'message': f'User {user.username} assigned as head of department {department_id}'})

# Route to get department info and members (accessible by department users and admin)
@main.route('/api/departments/<int:department_id>', methods=['GET'])
@token_required
def get_department(current_user, department_id):
    if current_user.department_id != department_id and not current_user.is_admin:
        return jsonify({'message': 'Access denied'}), 403
    department = Department.query.get(department_id)
    if not department:
        return jsonify({'message': 'Department not found'}), 404
    members = [{'id': u.id, 'username': u.username} for u in User.query.filter_by(department_id=department_id)]
    return jsonify({'department': department.name, 'members': members})

# Route to send a message within a department
@main.route('/api/departments/<int:department_id>/messages', methods=['POST'])
@token_required
def send_message(current_user, department_id):
    if current_user.department_id != department_id and not current_user.is_admin:
        return jsonify({'message': 'Access denied'}), 403
    data = request.get_json()
    message = Message(sender_id=current_user.id, department_id=department_id, content=data['content'])
    db.session.add(message)
    db.session.commit()
    return jsonify({'message': 'Message sent successfully'})

# Route to get messages within a department
@main.route('/api/departments/<int:department_id>/messages', methods=['GET'])
@token_required
def get_messages(current_user, department_id):
    if current_user.department_id != department_id and not current_user.is_admin:
        return jsonify({'message': 'Access denied'}), 403
    messages = Message.query.filter_by(department_id=department_id).all()
    messages_data = [{'sender': msg.sender_id, 'content': msg.content, 'timestamp': msg.timestamp} for msg in messages]
    return jsonify({'messages': messages_data})

# New Route to create login details for department members (admin only)
@main.route('/api/departments/<int:department_id>/users/<int:user_id>/create_login', methods=['POST'])
@token_required
def create_login_for_user(current_user, department_id, user_id):
    if not current_user.is_admin:
        return jsonify({'message': 'Unauthorized access'}), 403
    user = User.query.filter_by(id=user_id, department_id=department_id).first()
    if not user:
        return jsonify({'message': 'User not found in the specified department'}), 404
    
    data = request.get_json()
    if 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Username and password are required'}), 400
    
    user.username = data['username']
    user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    db.session.commit()
    
    return jsonify({'message': f'Login credentials for user {user.id} created successfully'})

