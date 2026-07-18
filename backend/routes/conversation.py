from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Conversation
import uuid

conversation_bp = Blueprint('conversation', __name__, url_prefix='/api/conversation')

@conversation_bp.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {'error': 'Unauthorized'}, 403
    
    conversations = Conversation.query.filter_by(company_id=user.company_id).order_by(Conversation.created_at.desc()).limit(100).all()
    
    return {
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

@conversation_bp.route('/feedback/<conv_id>', methods=['POST'])
@jwt_required()
def submit_feedback(conv_id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {'error': 'Unauthorized'}, 403
    
    data = request.json
    feedback = data.get('feedback')
    
    if feedback not in ['helpful', 'not_helpful']:
        return {'error': 'Invalid feedback'}, 400
    
    conversation = Conversation.query.get(conv_id)
    if not conversation or conversation.company_id != user.company_id:
        return {'error': 'Conversation not found'}, 404
    
    conversation.feedback = feedback
    db.session.commit()
    
    return {'message': 'Feedback recorded'}, 200

@conversation_bp.route('/save', methods=['POST'])
def save_conversation():
    data = request.json
    api_key = data.get('api_key')
    question = data.get('question')
    answer = data.get('answer')
    confidence = data.get('confidence', 0.0)
    source = data.get('source', 'faq')
    
    from models import Company
    company = Company.query.filter_by(api_key=api_key).first()
    if not company:
        return {'error': 'Invalid API key'}, 401
    
    conversation = Conversation(
        id=str(uuid.uuid4()),
        company_id=company.id,
        user_question=question,
        chatbot_answer=answer,
        confidence=confidence,
        source=source
    )
    db.session.add(conversation)
    db.session.commit()
    
    return {'id': conversation.id}, 201

