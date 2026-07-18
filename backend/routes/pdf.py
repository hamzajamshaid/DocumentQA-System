from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, PDFDocument, FAQ
import pdfplumber
import os
import uuid
from sklearn.feature_extraction.text import TfidfVectorizer
import re

pdf_bp = Blueprint('pdf', __name__, url_prefix='/api/pdf')

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@pdf_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_pdf():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {'error': 'Unauthorized'}, 403
    
    if 'file' not in request.files:
        return {'error': 'No file provided'}, 400
    
    file = request.files['file']
    if not file.filename.endswith('.pdf'):
        return {'error': 'Only PDF files allowed'}, 400
    
    filename = f"{uuid.uuid4()}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    try:
        text = extract_pdf_text(filepath)
        faqs = generate_knowledge_base_faqs(text)
        
        pdf_doc = PDFDocument(
            id=str(uuid.uuid4()),
            company_id=user.company_id,
            filename=file.filename,
            file_path=filepath
        )
        db.session.add(pdf_doc)
        db.session.flush()
        
        for q, a in faqs:
            faq = FAQ(
                id=str(uuid.uuid4()),
                company_id=user.company_id,
                question=q,
                answer=a,
                source='pdf'
            )
            db.session.add(faq)
        
        db.session.commit()
        
        return {
            'message': 'PDF processed successfully',
            'faqs_created': len(faqs),
            'filename': file.filename
        }, 201
    except Exception as e:
        return {'error': str(e)}, 500

def extract_pdf_text(filepath):
    text = ""
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        raise Exception(f"Failed to extract PDF: {str(e)}")
    return text

def generate_knowledge_base_faqs(text):
    """
    Convert company knowledge base text into Q&A pairs
    by analyzing content and generating relevant questions
    """
    faqs = []
    
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    if not sentences:
        return faqs
    
    keywords_questions = {
        'what': 'What is {company}?',
        'where': 'Where does {company} operate?',
        'how': 'How does {company} work?',
        'who': 'Who is involved in {company}?',
        'when': 'When was {company} founded?',
        'why': 'Why does {company} exist?',
        'provide': 'What services does {company} provide?',
        'help': 'How can {company} help me?',
        'contact': 'How do I contact {company}?',
        'donate': 'How can I donate to {company}?',
    }
    
    company_name = extract_company_name(text)
    
    for i, sentence in enumerate(sentences[:15]):
        if len(sentence) < 20:
            continue
        
        question = generate_question_from_sentence(sentence, company_name)
        if question:
            answer = sentence.strip()
            faqs.append((question, answer))
    
    return faqs[:20]

def extract_company_name(text):
    """Extract likely company name from text"""
    lines = text.split('\n')
    for line in lines[:5]:
        line = line.strip()
        if len(line) > 3 and len(line) < 50:
            return line
    return "the organization"

def generate_question_from_sentence(sentence, company_name=""):
    """Generate a natural question from a sentence"""
    sentence = sentence.strip()
    
    if sentence.startswith('The '):
        question = "What is " + sentence[4:50] + "?"
        return question
    
    if 'provide' in sentence.lower() or 'offer' in sentence.lower():
        return f"What services does {company_name} provide?"
    
    if 'work' in sentence.lower() or 'operate' in sentence.lower():
        return f"How does {company_name} work?"
    
    if 'help' in sentence.lower() or 'support' in sentence.lower():
        return f"How can {company_name} help?"
    
    if 'contact' in sentence.lower() or 'reach' in sentence.lower():
        return f"How do I contact {company_name}?"
    
    if 'donate' in sentence.lower() or 'contribute' in sentence.lower():
        return f"How can I donate?"
    
    if len(sentence) > 50:
        return sentence[:60].rstrip() + "?"
    
    return None

