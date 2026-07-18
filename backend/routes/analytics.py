from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, FAQ, Conversation
from datetime import datetime
from sqlalchemy import func

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

@analytics_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def analytics_dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {'error': 'Unauthorized'}, 403
    
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    if start_date_str and end_date_str:
        try:
            start_date = datetime.fromisoformat(start_date_str)
            end_date = datetime.fromisoformat(end_date_str)
        except:
            start_date = None
            end_date = None
    else:
        start_date = None
        end_date = None
    
    total_faqs = FAQ.query.filter_by(company_id=user.company_id).count()
    manual_faqs = FAQ.query.filter_by(company_id=user.company_id, source='manual').count()
    pdf_faqs = FAQ.query.filter_by(company_id=user.company_id, source='pdf').count()
    
    if start_date and end_date:
        conversations = Conversation.query.filter_by(company_id=user.company_id).filter(
            Conversation.created_at >= start_date,
            Conversation.created_at <= end_date
        ).all()
    else:
        conversations = Conversation.query.filter_by(company_id=user.company_id).all()
    
    total_conversations = len(conversations)
    helpful_count = len([c for c in conversations if c.feedback == 'helpful'])
    not_helpful_count = len([c for c in conversations if c.feedback == 'not_helpful'])
    low_confidence = len([c for c in conversations if c.confidence < 0.5])
    
    conversations_sorted = sorted(conversations, key=lambda x: x.created_at, reverse=True)
    
    return jsonify({
        'total_faqs': int(total_faqs),
        'manual_faqs': int(manual_faqs),
        'pdf_faqs': int(pdf_faqs),
        'avg_faq_length': int(calculate_avg_length(user.company_id)),
        'total_conversations': int(total_conversations),
        'helpful_feedback': int(helpful_count),
        'not_helpful_feedback': int(not_helpful_count),
        'low_confidence_answers': int(low_confidence),
        'conversations': [{
            'id': c.id,
            'question': c.user_question,
            'answer': c.chatbot_answer,
            'confidence': float(c.confidence),
            'source': c.source,
            'feedback': c.feedback,
            'created_at': c.created_at.isoformat()
        } for c in conversations_sorted]
    }), 200

@analytics_bp.route('/top-questions', methods=['GET'])
@jwt_required()
def top_questions():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {'error': 'Unauthorized'}, 403
    
    conversations = Conversation.query.filter_by(company_id=user.company_id).all()
    
    question_count = {}
    for conv in conversations:
        q = conv.user_question
        question_count[q] = question_count.get(q, 0) + 1
    
    sorted_questions = sorted(question_count.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return jsonify({
        'top_questions': [{'question': q, 'count': int(c)} for q, c in sorted_questions]
    }), 200

def calculate_avg_length(company_id):
    faqs = FAQ.query.filter_by(company_id=company_id).all()
    if not faqs:
        return 0
    total_length = sum(len(faq.answer) for faq in faqs)
    return int(round(total_length / len(faqs), 0))

