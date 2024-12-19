# backend/routes/patients.py

from flask import Blueprint, request, jsonify
from models.patient import get_all_patients, get_patient_by_id, create_patient, update_patient, delete_patient
from utils.auth_decorator import token_required
from bson.objectid import ObjectId

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/patients', methods=['GET'])
@token_required(required_roles=['medecin', 'secretaire'])
def list_patients(user_info):
    patients = get_all_patients()
    for patient in patients:
        patient['_id'] = str(patient['_id'])
    return jsonify(patients), 200

@patients_bp.route('/patients/<patient_id>', methods=['GET'])
@token_required(required_roles=['medecin', 'secretaire'])
def get_patient_route(user_info, patient_id):
    patient = get_patient_by_id(patient_id)
    if not patient:
        return jsonify({'message': 'Patient non trouvé'}), 404
    patient['_id'] = str(patient['_id'])
    return jsonify(patient), 200

@patients_bp.route('/patients', methods=['POST'])
@token_required(required_roles=['medecin'])
def create_patient_route(user_info):
    patient_data = request.get_json()
    create_patient(patient_data)
    return jsonify({'message': 'Patient créé'}), 201

@patients_bp.route('/patients/<patient_id>', methods=['PUT'])
@token_required(required_roles=['medecin'])
def update_patient_route(user_info, patient_id):
    update_data = request.get_json()
    update_patient(patient_id, update_data)
    return jsonify({'message': 'Patient mis à jour'}), 200

@patients_bp.route('/patients/<patient_id>', methods=['DELETE'])
@token_required(required_roles=['medecin'])
def delete_patient_route(user_info, patient_id):
    delete_patient(patient_id)
    return jsonify({'message': 'Patient supprimé'}), 200
