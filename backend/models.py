from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
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
    
    users = db.relationship('User', backref='company', lazy=True, cascade='all, delete-orphan')
    faqs = db.relationship('FAQ', backref='company', lazy=True, cascade='all, delete-orphan')
    conversations = db.relationship('Conversation', backref='company', lazy=True, cascade='all, delete-orphan')
    user_profiles = db.relationship('UserProfile', backref='company', lazy=True, cascade='all, delete-orphan')

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = db.Column(db.String(36), db.ForeignKey('companies.id'), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='viewer')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('company_id', 'email', name='unique_company_email'),)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class FAQ(db.Model):
    __tablename__ = 'faqs'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = db.Column(db.String(36), db.ForeignKey('companies.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    source = db.Column(db.String(50), default='manual')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PDFDocument(db.Model):
    __tablename__ = 'pdf_documents'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = db.Column(db.String(36), db.ForeignKey('companies.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Conversation(db.Model):
    __tablename__ = 'conversations'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = db.Column(db.String(36), db.ForeignKey('companies.id'), nullable=False)
    user_profile_id = db.Column(db.String(36), db.ForeignKey('user_profiles.id'), default=None)
    user_question = db.Column(db.Text, nullable=False)
    chatbot_answer = db.Column(db.Text, nullable=False)
    confidence = db.Column(db.Float, default=0.0)
    source = db.Column(db.String(50), default='faq')
    feedback = db.Column(db.String(10), default=None)
    language = db.Column(db.String(10), default='en')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_profile = db.relationship('UserProfile', backref='conversations')

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = db.Column(db.String(36), db.ForeignKey('companies.id'), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    ip_address = db.Column(db.String(50), default=None)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('company_id', 'username', name='unique_company_username'),)

