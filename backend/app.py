import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from models import db
from routes import auth_bp, faq_bp, chatbot_bp, company_bp, pdf_bp, analytics_bp, import_bp, conversation_bp, user_profile_bp
from middleware import rate_limit

load_dotenv()

app = Flask(__name__)

# Enable CORS with explicit settings
CORS(app, 
     resources={r"/api/*": {
         "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         "allow_headers": ["Content-Type", "Authorization"],
         "supports_credentials": True
     }})

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# JWT error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'error': 'Token expired'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'error': 'Invalid token'}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'error': 'Authorization required'}), 401

# Create tables
with app.app_context():
    db.create_all()

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(faq_bp)
app.register_blueprint(chatbot_bp)
app.register_blueprint(company_bp)
app.register_blueprint(pdf_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(import_bp)
app.register_blueprint(conversation_bp)
app.register_blueprint(user_profile_bp)

@app.route('/api/health', methods=['GET'])
@rate_limit
def health():
    return {'status': 'healthy'}

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'message': str(error)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

