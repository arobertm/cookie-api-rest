from flask import Blueprint, request, jsonify, make_response
import jwt
from datetime import datetime, timedelta
from functools import wraps

auth_bp = Blueprint('auth', __name__)

users_db = {
    "admin@test.com": {
        "password": "admin123",
        "role": "admin"
    }
}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('access_token')
        if not token:
            return jsonify({"error": "Token lipsește!"}), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = users_db.get(data['email'])
        except:
            return jsonify({"error": "Token invalid!"}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = users_db.get(data['email'])
    
    if user and user['password'] == data['password']:
        token = jwt.encode({
            'email': data['email'],
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, current_app.config['SECRET_KEY'])
        
        response = make_response(jsonify({"message": "Login successful"}))
        response.set_cookie(
            'access_token', 
            token,
            httponly=True,
            secure=True,
            samesite='Strict',
            max_age=3600
        )
        return response
    
    return jsonify({"error": "Invalid credentials"}), 401