# backend/routes/devices.py

from flask import Blueprint, request, jsonify
from models.device import get_all_devices, get_device_by_id, create_device, update_device, delete_device
from utils.auth_decorator import token_required
from bson.objectid import ObjectId

devices_bp = Blueprint('devices', __name__)

@devices_bp.route('/devices', methods=['GET'])
@token_required(required_roles=['medecin', 'secretaire', 'service_externe'])
def list_devices(user_info):
    devices = get_all_devices()
    for device in devices:
        device['_id'] = str(device['_id'])
    return jsonify(devices), 200

@devices_bp.route('/devices/<device_id>', methods=['GET'])
@token_required(required_roles=['medecin', 'secretaire', 'service_externe'])
def get_device_route(user_info, device_id):
    device = get_device_by_id(device_id)
    if not device:
        return jsonify({'message': 'Dispositif médical non trouvé'}), 404
    device['_id'] = str(device['_id'])
    return jsonify(device), 200

@devices_bp.route('/devices', methods=['POST'])
@token_required(required_roles=['medecin', 'secretaire'])
def create_device_route(user_info):
    device_data = request.get_json()
    create_device(device_data)
    return jsonify({'message': 'Dispositif médical créé'}), 201

@devices_bp.route('/devices/<device_id>', methods=['PUT'])
@token_required(required_roles=['medecin', 'secretaire'])
def update_device_route(user_info, device_id):
    update_data = request.get_json()
    update_device(device_id, update_data)
    return jsonify({'message': 'Dispositif médical mis à jour'}), 200

@devices_bp.route('/devices/<device_id>', methods=['DELETE'])
@token_required(required_roles=['medecin'])
def delete_device_route(user_info, device_id):
    delete_device(device_id)
    return jsonify({'message': 'Dispositif médical supprimé'}), 200
