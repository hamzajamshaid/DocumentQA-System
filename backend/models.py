from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    api_key = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = db.Column(db.String(36), db.ForeignKey('companies.id'), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='viewer')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FAQ(db.Model):
    __tablename__ = 'faqs'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = db.Column(db.String(36), db.ForeignKey('companies.id'), nullable=False)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(50), default='manual')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PDFDocument(db.Model):
    __tablename__ = 'pdf_documents'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = db.Column(db.String(36), db.ForeignKey('companies.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Conversation(db.Model):
    __tablename__ = 'conversations'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = db.Column(db.String(36), db.ForeignKey('companies.id'), nullable=False)
    user_profile_id = db.Column(db.String(36), db.ForeignKey('user_profiles.id'))
    user_question = db.Column(db.Text, nullable=False)
    chatbot_answer = db.Column(db.Text, nullable=False)
    confidence = db.Column(db.Float, default=0.0)
    source = db.Column(db.String(50), default='faq')
    feedback = db.Column(db.String(50))
    language = db.Column(db.String(50), default='en')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = db.Column(db.String(36), db.ForeignKey('companies.id'), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    ip_address = db.Column(db.String(50))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class WidgetConfig(db.Model):
    __tablename__ = 'widget_configs'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = db.Column(db.String(36), db.ForeignKey('companies.id'), nullable=False, unique=True)
    primary_color = db.Column(db.String(7), default='#6366f1')
    secondary_color = db.Column(db.String(7), default='#ffffff')
    text_color = db.Column(db.String(7), default='#000000')
    theme = db.Column(db.String(50), default='modern')
    position = db.Column(db.String(50), default='bottom-right')
    greeting_message = db.Column(db.Text, default='Hi! How can I help you today?')
    font_size = db.Column(db.Integer, default=14)
    bubble_size = db.Column(db.Integer, default=60)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

