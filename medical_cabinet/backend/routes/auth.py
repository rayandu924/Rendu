# backend/routes/auth.py

import logging
from flask import Blueprint, request, jsonify
from models.user import get_user_by_username, create_user
from models import bcrypt  # Correct import
import jwt
from datetime import datetime, timedelta
from config import Config

auth_bp = Blueprint('auth', __name__)

logger = logging.getLogger(__name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    logger.debug("Requête de connexion reçue")
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        logger.warning("Nom d'utilisateur ou mot de passe manquant")
        return jsonify({'message': 'Nom d\'utilisateur et mot de passe requis'}), 400
    
    user = get_user_by_username(username)
    if not user or not bcrypt.check_password_hash(user['password'], password):
        logger.error("Échec de l'authentification pour %s", username)
        return jsonify({'message': 'Échec de l\'authentification'}), 401
    
    payload = {
        'user_id': str(user['_id']),
        'username': user['username'],
        'roles': user.get('roles', []),
        'exp': datetime.utcnow() + timedelta(seconds=Config.JWT_ACCESS_TOKEN_EXPIRES)
    }
    token = jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')
    logger.debug("Token obtenu pour l'utilisateur %s: %s", username, token)
    return jsonify({'access_token': token}), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    logger.debug("Requête d'inscription reçue")
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    roles = data.get('roles', ['secretaire'])  # Rôle par défaut
    
    if not username or not password:
        logger.warning("Nom d'utilisateur ou mot de passe manquant lors de l'inscription")
        return jsonify({'message': 'Nom d\'utilisateur et mot de passe requis'}), 400
    
    existing_user = get_user_by_username(username)
    if existing_user:
        logger.warning("Tentative d'inscription d'un utilisateur existant: %s", username)
        return jsonify({'message': 'Utilisateur déjà existant'}), 400
    
    user_data = {
        'username': username,
        'password': password,
        'roles': roles
    }
    create_user(user_data)
    logger.info("Utilisateur %s créé avec succès", username)
    return jsonify({'message': 'Utilisateur créé avec succès'}), 201
