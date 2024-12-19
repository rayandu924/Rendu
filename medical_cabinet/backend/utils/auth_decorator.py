# backend/utils/auth_decorator.py

import logging
from functools import wraps
from flask import request, jsonify
import jwt
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def token_required(required_roles=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                try:
                    token = request.headers['Authorization'].split(" ")[1]
                except IndexError:
                    return jsonify({'message': 'Format du token invalide!'}), 401
            if not token:
                logger.warning("Aucun token fourni")
                return jsonify({'message': 'Token manquant!'}), 401
            try:
                decoded_token = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
                user_info = {
                    'user_id': decoded_token['user_id'],
                    'username': decoded_token['username'],
                    'roles': decoded_token.get('roles', [])
                }
                logger.info(f"Informations utilisateur: {user_info}")
                if required_roles:
                    user_roles = user_info.get('roles', [])
                    logger.info(f"Rôles de l'utilisateur: {user_roles}")
                    if not any(role in user_roles for role in required_roles):
                        logger.warning("Accès refusé: rôles insuffisants")
                        return jsonify({'message': 'Accès refusé!'}), 403
            except jwt.ExpiredSignatureError:
                logger.error("Token expiré")
                return jsonify({'message': 'Token expiré!'}), 401
            except jwt.InvalidTokenError as e:
                logger.error(f"Échec de la vérification du token: {e}")
                return jsonify({'message': 'Token invalide!'}), 401
            return f(user_info, *args, **kwargs)
        return decorated_function
    return decorator
