from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Company, User
import secrets

company_bp = Blueprint('company', __name__, url_prefix='/api/company')

@company_bp.route('/api-key', methods=['GET'])
@jwt_required()
def get_api_key():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Unauthorized'}), 403
    
    company = Company.query.get(user.company_id)
    return jsonify({'api_key': company.api_key}), 200

@company_bp.route('/regenerate-api-key', methods=['POST'])
@jwt_required()
def regenerate_api_key():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Unauthorized'}), 403
    
    company = Company.query.get(user.company_id)
    new_key = secrets.token_urlsafe(32)
    company.api_key = new_key
    db.session.commit()
    
    return jsonify({'api_key': new_key}), 200

