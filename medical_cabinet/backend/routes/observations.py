# backend/routes/observations.py

from flask import Blueprint, request, jsonify
from models.observation import get_all_observations, get_observation_by_id, create_observation, update_observation, delete_observation
from utils.auth_decorator import token_required
from bson.objectid import ObjectId

observations_bp = Blueprint('observations', __name__)

@observations_bp.route('/observations', methods=['GET'])
@token_required(required_roles=['medecin', 'secretaire', 'service_externe'])
def list_observations(user_info):
    observations = get_all_observations()
    for obs in observations:
        obs['_id'] = str(obs['_id'])
    return jsonify(observations), 200

@observations_bp.route('/observations/<observation_id>', methods=['GET'])
@token_required(required_roles=['medecin', 'secretaire', 'service_externe'])
def get_observation_route(user_info, observation_id):
    observation = get_observation_by_id(observation_id)
    if not observation:
        return jsonify({'message': 'Observation non trouvée'}), 404
    observation['_id'] = str(observation['_id'])
    return jsonify(observation), 200

@observations_bp.route('/observations', methods=['POST'])
@token_required(required_roles=['medecin', 'secretaire', 'service_externe'])
def create_observation_route(user_info):
    observation_data = request.get_json()
    create_observation(observation_data)
    return jsonify({'message': 'Observation créée'}), 201

@observations_bp.route('/observations/<observation_id>', methods=['PUT'])
@token_required(required_roles=['medecin', 'secretaire', 'service_externe'])
def update_observation_route(user_info, observation_id):
    update_data = request.get_json()
    update_observation(observation_id, update_data)
    return jsonify({'message': 'Observation mise à jour'}), 200

@observations_bp.route('/observations/<observation_id>', methods=['DELETE'])
@token_required(required_roles=['medecin'])
def delete_observation_route(user_info, observation_id):
    delete_observation(observation_id)
    return jsonify({'message': 'Observation supprimée'}), 200
