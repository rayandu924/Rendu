# backend/routes/users.py

from flask import Blueprint, request, jsonify
from models.user import get_all_users, get_user_by_id, create_user, update_user, delete_user, get_user_by_username
from utils.auth_decorator import token_required
from bson.objectid import ObjectId

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
@token_required(required_roles=['administrateur'])
def list_users(user_info):
    users = get_all_users()
    for user in users:
        user['_id'] = str(user['_id'])
        user['password'] = '********'  # Masquer les mots de passe
    return jsonify(users), 200

@users_bp.route('/users/<user_id>', methods=['GET'])
@token_required(required_roles=['administrateur'])
def get_user_route(user_info, user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({'message': 'Utilisateur non trouvé'}), 404
    user['_id'] = str(user['_id'])
    user['password'] = '********'
    return jsonify(user), 200

@users_bp.route('/users', methods=['POST'])
@token_required(required_roles=['administrateur'])
def create_user_route(user_info):
    user_data = request.get_json()
    if not user_data.get('username') or not user_data.get('password'):
        return jsonify({'message': 'Nom d\'utilisateur et mot de passe requis'}), 400
    existing_user = get_user_by_username(user_data['username'])
    if existing_user:
        return jsonify({'message': 'Utilisateur déjà existant'}), 400
    create_user(user_data)
    return jsonify({'message': 'Utilisateur créé'}), 201

@users_bp.route('/users/<user_id>', methods=['PUT'])
@token_required(required_roles=['administrateur'])
def update_user_route(user_info, user_id):
    update_data = request.get_json()
    update_user(user_id, update_data)
    return jsonify({'message': 'Utilisateur mis à jour'}), 200

@users_bp.route('/users/<user_id>', methods=['DELETE'])
@token_required(required_roles=['administrateur'])
def delete_user_route(user_info, user_id):
    delete_user(user_id)
    return jsonify({'message': 'Utilisateur supprimé'}), 200
