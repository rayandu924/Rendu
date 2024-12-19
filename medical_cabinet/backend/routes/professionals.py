# backend/routes/professionals.py

from flask import Blueprint, request, jsonify
from models.professional import get_all_professionals, get_professional_by_id, create_professional, update_professional, delete_professional
from utils.auth_decorator import token_required
from bson.objectid import ObjectId

professionals_bp = Blueprint('professionals', __name__)

@professionals_bp.route('/professionals', methods=['GET'])
@token_required(required_roles=['medecin', 'secretaire'])
def list_professionals(user_info):
    professionals = get_all_professionals()
    for prof in professionals:
        prof['_id'] = str(prof['_id'])
    return jsonify(professionals), 200

@professionals_bp.route('/professionals/<professional_id>', methods=['GET'])
@token_required(required_roles=['medecin', 'secretaire'])
def get_professional_route(user_info, professional_id):
    professional = get_professional_by_id(professional_id)
    if not professional:
        return jsonify({'message': 'Professionnel non trouvé'}), 404
    professional['_id'] = str(professional['_id'])
    return jsonify(professional), 200

@professionals_bp.route('/professionals', methods=['POST'])
@token_required(required_roles=['medecin'])
def create_professional_route(user_info):
    professional_data = request.get_json()
    create_professional(professional_data)
    return jsonify({'message': 'Professionnel créé'}), 201

@professionals_bp.route('/professionals/<professional_id>', methods=['PUT'])
@token_required(required_roles=['medecin'])
def update_professional_route(user_info, professional_id):
    update_data = request.get_json()
    update_professional(professional_id, update_data)
    return jsonify({'message': 'Professionnel mis à jour'}), 200

@professionals_bp.route('/professionals/<professional_id>', methods=['DELETE'])
@token_required(required_roles=['medecin'])
def delete_professional_route(user_info, professional_id):
    delete_professional(professional_id)
    return jsonify({'message': 'Professionnel supprimé'}), 200
