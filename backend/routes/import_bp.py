from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, FAQ
import csv
import json
import uuid

import_bp = Blueprint('import', __name__, url_prefix='/api/import')

@import_bp.route('/csv', methods=['POST'])
@jwt_required()
def import_csv():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'admin':
        return {'error': 'Unauthorized'}, 403
    
    if 'file' not in request.files:
        return {'error': 'No file provided'}, 400
    
    file = request.files['file']
    if not file.filename.endswith('.csv'):
        return {'error': 'Only CSV files allowed'}, 400
    
    try:
        stream = file.stream.read().decode("UTF8")
        data = stream.split("\n")
        reader = csv.DictReader(data)
        
        count = 0
        for row in reader:
            if row.get('question') and row.get('answer'):
                faq = FAQ(
                    id=str(uuid.uuid4()),
                    company_id=user.company_id,
                    question=row['question'],
                    answer=row['answer'],
                    source='csv'
                )
                db.session.add(faq)
                count += 1
        
        db.session.commit()
        return {'message': f'{count} FAQs imported successfully'}, 201
    except Exception as e:
        return {'error': str(e)}, 400

@import_bp.route('/json', methods=['POST'])
@jwt_required()
def import_json():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'admin':
        return {'error': 'Unauthorized'}, 403
    
    if 'file' not in request.files:
        return {'error': 'No file provided'}, 400
    
    file = request.files['file']
    if not file.filename.endswith('.json'):
        return {'error': 'Only JSON files allowed'}, 400
    
    try:
        data = json.load(file)
        count = 0
        
        for item in data.get('faqs', []):
            if item.get('question') and item.get('answer'):
                faq = FAQ(
                    id=str(uuid.uuid4()),
                    company_id=user.company_id,
                    question=item['question'],
                    answer=item['answer'],
                    source='json'
                )
                db.session.add(faq)
                count += 1
        
        db.session.commit()
        return {'message': f'{count} FAQs imported successfully'}, 201
    except Exception as e:
        return {'error': str(e)}, 400

