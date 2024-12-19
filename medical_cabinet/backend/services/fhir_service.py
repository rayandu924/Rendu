# backend/services/fhir_service.py

from datetime import timedelta
from flask import Blueprint, request, jsonify
from models.patient import get_all_patients, get_patient_by_id, create_patient, update_patient, delete_patient
from models.professional import get_all_professionals, get_professional_by_id, create_professional, update_professional, delete_professional
from models.appointment import get_all_appointments, get_appointment_by_id, create_appointment, update_appointment, delete_appointment
from models.device import get_all_devices, get_device_by_id, create_device, update_device, delete_device
from models.observation import get_all_observations, get_observation_by_id, create_observation, update_observation, delete_observation
from utils.auth_decorator import token_required
from bson.objectid import ObjectId
from models import mongo  # Assurez-vous d'avoir cet import pour accéder au client Mongo

fhir_bp = Blueprint('fhir', __name__)

# Endpoint FHIR pour les Patients
@fhir_bp.route('/fhir/Patient', methods=['GET', 'POST'])
@token_required(required_roles=['medecin', 'secretaire'])
def handle_patient(user_info):
    if request.method == 'GET':
        patients = get_all_patients()
        # Conversion des patients en format FHIR
        fhir_patients = []
        for patient in patients:
            fhir_patient = {
                "resourceType": "Patient",
                "id": str(patient["_id"]),
                "name": [{
                    "use": "official",
                    "family": patient.get("last_name", ""),
                    "given": [patient.get("first_name", "")]
                }],
                "gender": patient.get("gender", ""),
                "birthDate": patient.get("birth_date", "")
            }
            fhir_patients.append(fhir_patient)
        return jsonify(fhir_patients), 200

    elif request.method == 'POST':
        patient_data = request.json
        # Mapper les données FHIR vers le modèle MOS
        mos_data = {
            "first_name": patient_data.get("name", [{}])[0].get("given", [""])[0],
            "last_name": patient_data.get("name", [{}])[0].get("family", ""),
            "gender": patient_data.get("gender", ""),
            "birth_date": patient_data.get("birthDate", ""),
            "contact": patient_data.get("contact", "")
        }
        create_patient(mos_data)
        return jsonify({"message": "Patient ajouté"}), 201

# Endpoint FHIR pour les Observations (DM)
@fhir_bp.route('/fhir/Observation', methods=['GET', 'POST'])
@token_required(required_roles=['medecin', 'secretaire', 'service_externe'])
def handle_observation(user_info):
    if request.method == 'GET':
        observations = get_all_observations()
        fhir_observations = []
        for obs in observations:
            fhir_obs = {
                "resourceType": "Observation",
                "id": str(obs["_id"]),
                "status": "final",
                "category": [{
                    "coding": [{
                        "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                        "code": "vital-signs",
                        "display": "Vital Signs"
                    }]
                }],
                "code": {
                    "coding": [{
                        "system": "http://loinc.org",
                        "code": "85354-9",
                        "display": "Blood pressure panel with all children optional"
                    }]
                },
                "subject": {
                    "reference": "Patient/" + str(obs["patient_id"])
                },
                "effectiveDateTime": obs["date"],
                "component": [
                    {
                        "code": {
                            "coding": [{
                                "system": "http://loinc.org",
                                "code": "8462-4",
                                "display": "Diastolic blood pressure"
                            }]
                        },
                        "valueQuantity": {
                            "value": obs.get("tension_diastolic", 0),
                            "unit": "mmHg",
                            "system": "http://unitsofmeasure.org",
                            "code": "mm[Hg]"
                        }
                    },
                    {
                        "code": {
                            "coding": [{
                                "system": "http://loinc.org",
                                "code": "8480-6",
                                "display": "Systolic blood pressure"
                            }]
                        },
                        "valueQuantity": {
                            "value": obs.get("tension_systolic", 0),
                            "unit": "mmHg",
                            "system": "http://unitsofmeasure.org",
                            "code": "mm[Hg]"
                        }
                    },
                    {
                        "code": {
                            "coding": [{
                                "system": "http://loinc.org",
                                "code": "8867-4",
                                "display": "Heart rate"
                            }]
                        },
                        "valueQuantity": {
                            "value": obs.get("rythme_cardiaque", 0),
                            "unit": "/min",
                            "system": "http://unitsofmeasure.org",
                            "code": "/min"
                        }
                    },
                    {
                        "code": {
                            "coding": [{
                                "system": "http://loinc.org",
                                "code": "2710-2",
                                "display": "Oxygen saturation in Arterial blood"
                            }]
                        },
                        "valueQuantity": {
                            "value": obs.get("oxymetrie", 0),
                            "unit": "%",
                            "system": "http://unitsofmeasure.org",
                            "code": "%"
                        }
                    }
                ]
            }
            fhir_observations.append(fhir_obs)
        return jsonify(fhir_observations), 200

    elif request.method == 'POST':
        observation_data = request.json
        # Mapper les données FHIR vers le modèle MOS
        patient_ref = observation_data.get("subject", {}).get("reference", "")
        patient_id = ObjectId(patient_ref.split("/")[1]) if "/" in patient_ref else None
        mos_data = {
            "patient_id": patient_id,
            "date": observation_data.get("effectiveDateTime", ""),
            "tension_systolic": observation_data.get("component", [])[1].get("valueQuantity", {}).get("value", 0),
            "tension_diastolic": observation_data.get("component", [])[0].get("valueQuantity", {}).get("value", 0),
            "rythme_cardiaque": observation_data.get("component", [])[2].get("valueQuantity", {}).get("value", 0),
            "oxymetrie": observation_data.get("component", [])[3].get("valueQuantity", {}).get("value", 0)
        }
        create_observation(mos_data)
        return jsonify({"message": "Observation ajoutée"}), 201
    
# Endpoint FHIR pour les Practitioners
@fhir_bp.route('/fhir/Practitioner', methods=['GET', 'POST'])
@token_required(required_roles=['medecin', 'secretaire'])
def handle_practitioner(user_info):
    if request.method == 'GET':
        professionals = get_all_professionals()
        fhir_practitioners = []
        for prof in professionals:
            fhir_prof = {
                "resourceType": "Practitioner",
                "id": str(prof["_id"]),
                "name": [{
                    "use": "official",
                    "family": prof.get("last_name", ""),
                    "given": [prof.get("first_name", "")]
                }],
                "telecom": [{
                    "system": "phone",
                    "value": prof.get("contact", ""),
                    "use": "work"
                }],
                "qualification": [{
                    "code": {
                        "text": prof.get("specialty", "")
                    }
                }]
            }
            fhir_practitioners.append(fhir_prof)
        return jsonify(fhir_practitioners), 200

    elif request.method == 'POST':
        prof_data = request.json
        mos_data = {
            "first_name": prof_data.get("name", [{}])[0].get("given", [""])[0],
            "last_name": prof_data.get("name", [{}])[0].get("family", ""),
            "specialty": prof_data.get("qualification", [{}])[0].get("code", {}).get("text", ""),
            "contact": prof_data.get("telecom", [{}])[0].get("value", "")
        }
        create_professional(mos_data)
        return jsonify({"message": "Praticien ajouté"}), 201

# Endpoint FHIR pour les Appointments
@fhir_bp.route('/fhir/Appointment', methods=['GET', 'POST'])
@token_required(required_roles=['medecin', 'secretaire'])
def handle_appointment(user_info):
    if request.method == 'GET':
        appointments = get_all_appointments()
        fhir_appointments = []
        for appt in appointments:
            fhir_appt = {
                "resourceType": "Appointment",
                "id": str(appt["_id"]),
                "status": "booked",
                "participant": [
                    {
                        "actor": {
                            "reference": f"Patient/{appt['patient_id']}"
                        },
                        "status": "accepted"
                    },
                    {
                        "actor": {
                            "reference": f"Practitioner/{appt['professional_id']}"
                        },
                        "status": "accepted"
                    }
                ],
                "start": appt["date"],
                "end": (ObjectId(appt["_id"]).generation_time + timedelta(minutes=30)).isoformat(),  # Example duration
                "description": appt["reason"]
            }
            fhir_appointments.append(fhir_appt)
        return jsonify(fhir_appointments), 200

    elif request.method == 'POST':
        appt_data = request.json
        mos_data = {
            "patient_id": ObjectId(appt_data.get("participant", [{}])[0].get("actor", {}).get("reference", "").split("/")[1]),
            "professional_id": ObjectId(appt_data.get("participant", [{}])[1].get("actor", {}).get("reference", "").split("/")[1]),
            "date": appt_data.get("start", ""),
            "reason": appt_data.get("description", "")
        }
        create_appointment(mos_data)
        return jsonify({"message": "Rendez-vous ajouté"}), 201

# Endpoint FHIR pour les Devices
@fhir_bp.route('/fhir/Device', methods=['GET', 'POST'])
@token_required(required_roles=['medecin', 'secretaire'])
def handle_device(user_info):
    if request.method == 'GET':
        devices = get_all_devices()
        fhir_devices = []
        for device in devices:
            fhir_device = {
                "resourceType": "Device",
                "id": str(device["_id"]),
                "identifier": [{
                    "system": "http://hospital.smarthealthit.org/devices",
                    "value": device.get("device_name", "")
                }],
                "type": {
                    "coding": [{
                        "system": "http://snomed.info/sct",
                        "code": "123456",  # Example code
                        "display": device.get("device_type", "")
                    }]
                },
                "patient": {
                    "reference": f"Patient/{device['patient_id']}"
                }
            }
            fhir_devices.append(fhir_device)
        return jsonify(fhir_devices), 200

    elif request.method == 'POST':
        device_data = request.json
        mos_data = {
            "device_name": device_data.get("identifier", [{}])[0].get("value", ""),
            "device_type": device_data.get("type", {}).get("coding", [{}])[0].get("display", ""),
            "patient_id": ObjectId(device_data.get("patient", {}).get("reference", "").split("/")[1])
        }
        create_device(mos_data)
        return jsonify({"message": "Dispositif médical ajouté"}), 201

@fhir_bp.route('/fhir/Patient/<patient_id>/$transfer', methods=['POST'])
@token_required(required_roles=['medecin', 'secretaire'])
def transfer_patient_record(user_info, patient_id):
    # Vérifier si le patient existe
    patient = get_patient_by_id(patient_id)
    if not patient:
        return jsonify({'message': 'Patient non trouvé'}), 404
    
    # Récupérer toutes les données associées au patient
    observations = mongo.db.observations.find({"patient_id": ObjectId(patient_id)})
    appointments = mongo.db.appointments.find({"patient_id": ObjectId(patient_id)})
    devices = mongo.db.devices.find({"patient_id": ObjectId(patient_id)})
    
    # Construire un Bundle FHIR
    bundle = {
        "resourceType": "Bundle",
        "type": "transaction",
        "entry": []
    }
    
    # Ajouter le Patient
    fhir_patient = {
        "resource": {
            "resourceType": "Patient",
            "id": str(patient["_id"]),
            "name": [{
                "use": "official",
                "family": patient.get("last_name", ""),
                "given": [patient.get("first_name", "")]
            }],
            "gender": patient.get("gender", ""),
            "birthDate": patient.get("birth_date", "")
        },
        "request": {
            "method": "PUT",
            "url": f"Patient/{str(patient['_id'])}"
        }
    }
    bundle["entry"].append(fhir_patient)
    
    # Ajouter les Observations
    for obs in observations:
        fhir_obs = {
            "resource": {
                "resourceType": "Observation",
                "id": str(obs["_id"]),
                "status": "final",
                "category": [{
                    "coding": [{
                        "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                        "code": "vital-signs",
                        "display": "Vital Signs"
                    }]
                }],
                "code": {
                    "coding": [{
                        "system": "http://loinc.org",
                        "code": "85354-9",
                        "display": "Blood pressure panel with all children optional"
                    }]
                },
                "subject": {
                    "reference": f"Patient/{str(obs['patient_id'])}"
                },
                "effectiveDateTime": obs["date"],
                "component": [
                    {
                        "code": {
                            "coding": [{
                                "system": "http://loinc.org",
                                "code": "8462-4",
                                "display": "Diastolic blood pressure"
                            }]
                        },
                        "valueQuantity": {
                            "value": obs.get("tension_diastolic", 0),
                            "unit": "mmHg",
                            "system": "http://unitsofmeasure.org",
                            "code": "mm[Hg]"
                        }
                    },
                    {
                        "code": {
                            "coding": [{
                                "system": "http://loinc.org",
                                "code": "8480-6",
                                "display": "Systolic blood pressure"
                            }]
                        },
                        "valueQuantity": {
                            "value": obs.get("tension_systolic", 0),
                            "unit": "mmHg",
                            "system": "http://unitsofmeasure.org",
                            "code": "mm[Hg]"
                        }
                    },
                    {
                        "code": {
                            "coding": [{
                                "system": "http://loinc.org",
                                "code": "8867-4",
                                "display": "Heart rate"
                            }]
                        },
                        "valueQuantity": {
                            "value": obs.get("rythme_cardiaque", 0),
                            "unit": "/min",
                            "system": "http://unitsofmeasure.org",
                            "code": "/min"
                        }
                    },
                    {
                        "code": {
                            "coding": [{
                                "system": "http://loinc.org",
                                "code": "2710-2",
                                "display": "Oxygen saturation in Arterial blood"
                            }]
                        },
                        "valueQuantity": {
                            "value": obs.get("oxymetrie", 0),
                            "unit": "%",
                            "system": "http://unitsofmeasure.org",
                            "code": "%"
                        }
                    }
                ]
            },
            "request": {
                "method": "PUT",
                "url": f"Observation/{str(obs['_id'])}"
            }
        }
        bundle["entry"].append(fhir_obs)
    
    # Ajouter les Appointments
    for appt in appointments:
        fhir_appt = {
            "resource": {
                "resourceType": "Appointment",
                "id": str(appt["_id"]),
                "status": "booked",
                "participant": [
                    {
                        "actor": {
                            "reference": f"Patient/{str(appt['patient_id'])}"
                        },
                        "status": "accepted"
                    },
                    {
                        "actor": {
                            "reference": f"Practitioner/{str(appt['professional_id'])}"
                        },
                        "status": "accepted"
                    }
                ],
                "start": appt["date"],
                "end": (ObjectId(appt["_id"]).generation_time + timedelta(minutes=30)).isoformat(),
                "description": appt["reason"]
            },
            "request": {
                "method": "PUT",
                "url": f"Appointment/{str(appt['_id'])}"
            }
        }
        bundle["entry"].append(fhir_appt)
    
    # Ajouter les Devices
    for device in devices:
        fhir_device = {
            "resource": {
                "resourceType": "Device",
                "id": str(device["_id"]),
                "identifier": [{
                    "system": "http://hospital.smarthealthit.org/devices",
                    "value": device.get("device_name", "")
                }],
                "type": {
                    "coding": [{
                        "system": "http://snomed.info/sct",
                        "code": "123456",
                        "display": device.get("device_type", "")
                    }]
                },
                "patient": {
                    "reference": f"Patient/{str(device['patient_id'])}"
                }
            },
            "request": {
                "method": "PUT",
                "url": f"Device/{str(device['_id'])}"
            }
        }
        bundle["entry"].append(fhir_device)
    
    return jsonify(bundle), 200