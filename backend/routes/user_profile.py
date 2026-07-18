from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, UserProfile, Conversation
import uuid

user_profile_bp = Blueprint('user_profile', __name__, url_prefix='/api/user-profile')

@user_profile_bp.route('/create', methods=['POST'])
def create_user_profile():
    data = request.json
    api_key = data.get('api_key')
    username = data.get('username')
    email = data.get('email')
    ip_address = data.get('ip_address')
    
    from models import Company
    company = Company.query.filter_by(api_key=api_key).first()
    if not company:
        return {'error': 'Invalid API key'}, 401
    
    existing = UserProfile.query.filter_by(company_id=company.id, username=username).first()
    if existing:
        existing.last_seen = datetime.utcnow()
        db.session.commit()
        return {'id': existing.id}, 200
    
    user_profile = UserProfile(
        id=str(uuid.uuid4()),
        company_id=company.id,
        username=username,
        email=email,
        ip_address=ip_address
    )
    db.session.add(user_profile)
    db.session.commit()
    
    return {'id': user_profile.id}, 201

@user_profile_bp.route('/list', methods=['GET'])
@jwt_required()
def list_users():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {'error': 'Unauthorized'}, 403
    
    users = UserProfile.query.filter_by(company_id=user.company_id).all()
    
    return {
        'users': [{
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'ip_address': u.ip_address,
            'last_seen': u.last_seen.isoformat(),
            'conversation_count': len(u.conversations),
            'created_at': u.created_at.isoformat()
        } for u in users]
    }, 200

@user_profile_bp.route('/<user_profile_id>', methods=['GET'])
@jwt_required()
def get_user_detail(user_profile_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {'error': 'Unauthorized'}, 403
    
    user_profile = UserProfile.query.get(user_profile_id)
    if not user_profile or user_profile.company_id != user.company_id:
        return {'error': 'User not found'}, 404
    
    conversations = Conversation.query.filter_by(user_profile_id=user_profile_id).order_by(Conversation.created_at.desc()).all()
    
    return {
        'user': {
            'id': user_profile.id,
            'username': user_profile.username,
            'email': user_profile.email,
            'ip_address': user_profile.ip_address,
            'last_seen': user_profile.last_seen.isoformat(),
            'created_at': user_profile.created_at.isoformat(),
            'conversation_count': len(conversations)
        },
        'conversations': [{
            'id': c.id,
            'question': c.user_question,
            'answer': c.chatbot_answer,
            'confidence': c.confidence,
            'source': c.source,
            'feedback': c.feedback,
            'created_at': c.created_at.isoformat()
        } for c in conversations]
    }, 200

from datetime import datetime

