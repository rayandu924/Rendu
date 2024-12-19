# backend/routes/appointments.py

from flask import Blueprint, request, jsonify
from models.appointment import get_all_appointments, get_appointment_by_id, create_appointment, update_appointment, delete_appointment
from utils.auth_decorator import token_required
from bson.objectid import ObjectId

appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/appointments', methods=['GET'])
@token_required(required_roles=['medecin', 'secretaire'])
def list_appointments(user_info):
    appointments = get_all_appointments()
    for appt in appointments:
        appt['_id'] = str(appt['_id'])
    return jsonify(appointments), 200

@appointments_bp.route('/appointments/<appointment_id>', methods=['GET'])
@token_required(required_roles=['medecin', 'secretaire'])
def get_appointment_route(user_info, appointment_id):
    appointment = get_appointment_by_id(appointment_id)
    if not appointment:
        return jsonify({'message': 'Rendez-vous non trouvé'}), 404
    appointment['_id'] = str(appointment['_id'])
    return jsonify(appointment), 200

@appointments_bp.route('/appointments', methods=['POST'])
@token_required(required_roles=['medecin', 'secretaire'])
def create_appointment_route(user_info):
    appointment_data = request.get_json()
    create_appointment(appointment_data)
    return jsonify({'message': 'Rendez-vous créé'}), 201

@appointments_bp.route('/appointments/<appointment_id>', methods=['PUT'])
@token_required(required_roles=['medecin', 'secretaire'])
def update_appointment_route(user_info, appointment_id):
    update_data = request.get_json()
    update_appointment(appointment_id, update_data)
    return jsonify({'message': 'Rendez-vous mis à jour'}), 200

@appointments_bp.route('/appointments/<appointment_id>', methods=['DELETE'])
@token_required(required_roles=['medecin'])
def delete_appointment_route(user_info, appointment_id):
    delete_appointment(appointment_id)
    return jsonify({'message': 'Rendez-vous supprimé'}), 200
