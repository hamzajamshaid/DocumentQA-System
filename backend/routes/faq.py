from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, FAQ, User
import uuid

faq_bp = Blueprint('faq', __name__, url_prefix='/api/faq')

@faq_bp.route('/create', methods=['POST'])
@jwt_required()
def create_faq():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'admin':
        return {'error': 'Unauthorized'}, 403
    
    data = request.json
    question = data.get('question')
    answer = data.get('answer')
    
    if not question or not answer:
        return {'error': 'Missing fields'}, 400
    
    faq = FAQ(
        id=str(uuid.uuid4()),
        company_id=user.company_id,
        question=question,
        answer=answer,
        source='manual'
    )
    db.session.add(faq)
    db.session.commit()
    
    return {'id': faq.id, 'message': 'FAQ created'}, 201

@faq_bp.route('/list', methods=['GET'])
@jwt_required()
def list_faqs():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {'error': 'Unauthorized'}, 403
    
    faqs = FAQ.query.filter_by(company_id=user.company_id).all()
    return {
        'faqs': [{
            'id': faq.id,
            'question': faq.question,
            'answer': faq.answer,
            'source': faq.source
        } for faq in faqs]
    }, 200

@faq_bp.route('/delete/<faq_id>', methods=['DELETE'])
@jwt_required()
def delete_faq(faq_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'admin':
        return {'error': 'Unauthorized'}, 403
    
    faq = FAQ.query.get(faq_id)
    if not faq or faq.company_id != user.company_id:
        return {'error': 'FAQ not found'}, 404
    
    db.session.delete(faq)
    db.session.commit()
    
    return {'message': 'FAQ deleted'}, 200

