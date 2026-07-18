from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import db, Company, User
import secrets

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    company_name = data.get('company_name')
    email = data.get('email')
    password = data.get('password')
    
    if not all([company_name, email, password]):
        return {'error': 'Missing fields'}, 400
    
    if Company.query.filter_by(email=email).first():
        return {'error': 'Company already exists'}, 400
    
    api_key = secrets.token_urlsafe(32)
    company = Company(name=company_name, email=email, api_key=api_key)
    db.session.add(company)
    db.session.flush()
    
    user = User(company_id=company.id, email=email, role='admin')
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    access_token = create_access_token(identity=str(user.id))
    return {
        'message': 'Signup successful',
        'access_token': access_token,
        'api_key': api_key,
        'company_id': company.id
    }, 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return {'error': 'Invalid credentials'}, 401
    
    access_token = create_access_token(identity=str(user.id))
    return {
        'access_token': access_token,
        'company_id': user.company_id,
        'user_id': user.id
    }, 200

