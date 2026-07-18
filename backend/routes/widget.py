from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, WidgetConfig, Company, User
import uuid

widget_bp = Blueprint('widget', __name__, url_prefix='/api/widget')

@widget_bp.route('/config', methods=['GET'])
@jwt_required()
def get_widget_config():
    """Get widget config for logged-in user's company"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Unauthorized'}), 403
    
    config = WidgetConfig.query.filter_by(company_id=user.company_id).first()
    
    if not config:
        config = WidgetConfig(
            id=str(uuid.uuid4()),
            company_id=user.company_id
        )
        db.session.add(config)
        db.session.commit()
    
    return jsonify({
        'id': config.id,
        'primary_color': config.primary_color,
        'secondary_color': config.secondary_color,
        'text_color': config.text_color,
        'theme': config.theme,
        'position': config.position,
        'greeting_message': config.greeting_message,
        'font_size': config.font_size,
        'bubble_size': config.bubble_size
    }), 200

@widget_bp.route('/config', methods=['POST'])
@jwt_required()
def update_widget_config():
    """Update widget config"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    config = WidgetConfig.query.filter_by(company_id=user.company_id).first()
    
    if not config:
        config = WidgetConfig(
            id=str(uuid.uuid4()),
            company_id=user.company_id
        )
        db.session.add(config)
    
    # Update fields
    if 'primary_color' in data:
        config.primary_color = data['primary_color']
    if 'secondary_color' in data:
        config.secondary_color = data['secondary_color']
    if 'text_color' in data:
        config.text_color = data['text_color']
    if 'theme' in data:
        config.theme = data['theme']
    if 'position' in data:
        config.position = data['position']
    if 'greeting_message' in data:
        config.greeting_message = data['greeting_message']
    if 'font_size' in data:
        config.font_size = data['font_size']
    if 'bubble_size' in data:
        config.bubble_size = data['bubble_size']
    
    db.session.commit()
    
    return jsonify({'message': 'Widget config updated', 'config': {
        'primary_color': config.primary_color,
        'secondary_color': config.secondary_color,
        'text_color': config.text_color,
        'theme': config.theme,
        'position': config.position,
        'greeting_message': config.greeting_message,
        'font_size': config.font_size,
        'bubble_size': config.bubble_size
    }}), 200

@widget_bp.route('/public-config/<api_key>', methods=['GET'])
def get_public_widget_config(api_key):
    """Get widget config by API key (no auth needed - for embedding)"""
    company = Company.query.filter_by(api_key=api_key).first()
    
    if not company:
        return jsonify({'error': 'Invalid API key'}), 403
    
    config = WidgetConfig.query.filter_by(company_id=company.id).first()
    
    if not config:
        config = WidgetConfig(
            id=str(uuid.uuid4()),
            company_id=company.id
        )
        db.session.add(config)
        db.session.commit()
    
    return jsonify({
        'primary_color': config.primary_color,
        'secondary_color': config.secondary_color,
        'text_color': config.text_color,
        'theme': config.theme,
        'position': config.position,
        'greeting_message': config.greeting_message,
        'font_size': config.font_size,
        'bubble_size': config.bubble_size,
        'api_key': api_key
    }), 200

@widget_bp.route('/embed-code', methods=['GET'])
@jwt_required()
def get_embed_code():
    """Generate embed code for customer to use on their website"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'Unauthorized'}), 403
    
    company = Company.query.get(user.company_id)
    
    embed_code = f"""
<!-- DocumentQA Chatbot Widget -->
<script>
  (function() {{
    var script = document.createElement('script');
    script.src = 'https://your-railway-url.app/static/widget.js';
    script.setAttribute('data-api-key', '{company.api_key}');
    document.head.appendChild(script);
  }})();
</script>
"""
    
    return jsonify({'embed_code': embed_code.strip()}), 200

