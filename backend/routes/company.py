from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Company

company_bp = Blueprint('company', __name__, url_prefix='/api/company')

@company_bp.route('/api-key', methods=['GET'])
@jwt_required()
def get_api_key():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {'error': 'Unauthorized'}, 403
    
    company = Company.query.get(user.company_id)
    return {'api_key': company.api_key}, 200

