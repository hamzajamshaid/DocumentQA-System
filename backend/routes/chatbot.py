from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Conversation, UserProfile, Company, User
from chatbot import DocumentQAChatbot
from difflib import SequenceMatcher
import uuid

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/chatbot')

# Greeting messages
GREETINGS = {
    'hello': "Hello! Welcome to our support. How can I help you today?",
    'hi': "Hi there! I'm here to answer your questions. What would you like to know?",
    'hey': "Hey! Thanks for reaching out. How can I assist?",
    'good morning': "Good morning! Welcome to support. How can I assist?",
    'good afternoon': "Good afternoon! How can I help you today?",
    'good evening': "Good evening! I'm here to help. What's your question?",
    'thanks': "You're welcome! Is there anything else I can help with?",
    'thank you': "Happy to help! Feel free to ask anything else.",
    'bye': "Goodbye! Thanks for using our support. Have a great day!",
    'help': "I'm here to help! You can ask me anything about our services."
}

def fuzzy_match(text, keywords, threshold=0.5):
    """Find best matching keyword using fuzzy matching"""
    text_lower = text.lower().strip()
    best_match = None
    best_score = 0
    
    for keyword in keywords:
        if keyword in text_lower:
            return keyword
        score = SequenceMatcher(None, text_lower, keyword).ratio()
        if score > best_score:
            best_score = score
            best_match = keyword
    
    if best_score >= threshold:
        return best_match
    return None

def is_greeting(question):
    """Check if question is a greeting"""
    return fuzzy_match(question, GREETINGS.keys(), threshold=0.5) is not None

def get_greeting_response(question):
    """Get appropriate greeting response"""
    matched = fuzzy_match(question, GREETINGS.keys(), threshold=0.5)
    if matched:
        return GREETINGS[matched]
    return GREETINGS['hello']

@chatbot_bp.route('/ask', methods=['POST'])
def ask_chatbot():
    data = request.get_json()
    api_key = data.get('api_key')
    question = data.get('question', '').strip()
    username = data.get('username', 'Anonymous')
    email = data.get('email', '')
    
    if not api_key or not question:
        return jsonify({'error': 'API key and question required'}), 400
    
    company = Company.query.filter_by(api_key=api_key).first()
    if not company:
        return jsonify({'error': 'Invalid API key'}), 403
    
    # Check if greeting
    if is_greeting(question):
        answer = get_greeting_response(question)
        confidence = 1.0
        source = 'greeting'
    else:
        # Use chatbot engine for normal questions
        engine = DocumentQAChatbot()
        answer, confidence = engine.find_answer(question)
        source = 'faq' if confidence > 0.3 else 'none'
    
    # Create or get user profile
    user_profile = UserProfile.query.filter_by(
        company_id=company.id,
        username=username
    ).first()
    
    if not user_profile:
        user_profile = UserProfile(
            id=str(uuid.uuid4()),
            company_id=company.id,
            username=username,
            email=email,
            ip_address=request.remote_addr
        )
        db.session.add(user_profile)
        db.session.flush()
    
    # Save conversation
    conversation = Conversation(
        id=str(uuid.uuid4()),
        company_id=company.id,
        user_profile_id=user_profile.id,
        user_question=question,
        chatbot_answer=answer,
        confidence=float(confidence),
        source=source
    )
    db.session.add(conversation)
    db.session.commit()
    
    return jsonify({
        'answer': answer,
        'confidence': float(confidence),
        'source': source,
        'conversation_id': conversation.id
    }), 200

@chatbot_bp.route('/feedback/<conversation_id>', methods=['POST'])
def provide_feedback(conversation_id):
    data = request.get_json()
    feedback = data.get('feedback')
    
    conversation = Conversation.query.get(conversation_id)
    if not conversation:
        return jsonify({'error': 'Conversation not found'}), 404
    
    conversation.feedback = feedback
    db.session.commit()
    
    return jsonify({'message': 'Feedback saved'}), 200

