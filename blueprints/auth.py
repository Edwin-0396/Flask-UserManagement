from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from app import db  # Import the db instance
import jwt
import datetime

auth_blueprint = Blueprint('auth', __name__)

# User registration route
@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Email and password are required'}), 400

    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'Email is already in use'}), 400

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

# User login route
@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'message': 'Email and password are required'}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid email or password'}), 401

    # Generate JWT token
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, current_app.config['SECRET_KEY'])  # Use current_app

    return jsonify({'token': token})
