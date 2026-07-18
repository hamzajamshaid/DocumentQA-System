from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Company
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

notifications_bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'your-email@gmail.com'
SENDER_PASSWORD = 'your-app-password'

def send_email(recipient, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email error: {str(e)}")
        return False

@notifications_bp.route('/send-welcome', methods=['POST'])
@jwt_required()
def send_welcome():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {'error': 'Unauthorized'}, 403
    
    company = Company.query.get(user.company_id)
    subject = f"Welcome to DocumentQA, {company.name}!"
    body = f"""
    <h2>Welcome to DocumentQA!</h2>
    <p>Your account has been created successfully.</p>
    <p>Your API Key: <code>{company.api_key}</code></p>
    <p>Start integrating our chatbot into your application.</p>
    """
    
    if send_email(user.email, subject, body):
        return {'message': 'Welcome email sent'}, 200
    return {'error': 'Failed to send email'}, 500

