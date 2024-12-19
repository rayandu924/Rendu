# backend/models/observation.py

from . import mongo
from bson.objectid import ObjectId
from services.alert_service import AlertService

alert_service = AlertService()

def get_all_observations():
    return list(mongo.db.observations.find())

def get_observation_by_id(observation_id):
    return mongo.db.observations.find_one({"_id": ObjectId(observation_id)})

def create_observation(observation_data):
    mongo.db.observations.insert_one(observation_data)
    # Vérifier si les données dépassent les seuils pour déclencher une alerte
    trigger_alert_if_needed(observation_data)

def trigger_alert_if_needed(observation):
    # Définir les seuils
    if (observation['tension_systolic'] > 140 or
        observation['tension_diastolic'] > 90 or
        observation['rythme_cardiaque'] > 100 or
        observation['oxymetrie'] < 95):
        
        # Récupérer le dossier patient pour obtenir les contacts
        patient = mongo.db.patients.find_one({"_id": observation['patient_id']})
        if not patient:
            return
        
        # Récupérer les professionnels associés
        professionals = mongo.db.professionals.find({"_id": {"$in": patient.get('professionals_ids', [])}})
        
        # Envoyer des emails et SMS aux professionnels et proches
        subject = "Alerte de Santé pour le Patient {}".format(patient.get('first_name', ''))
        message = f"""
        Alerte de santé pour le patient {patient.get('first_name', '')} {patient.get('last_name', '')}.

        Tension Systolique: {observation['tension_systolic']} mmHg
        Tension Diastolique: {observation['tension_diastolic']} mmHg
        Rythme Cardiaque: {observation['rythme_cardiaque']} /min
        Oxymétrie: {observation['oxymetrie']} %

        Veuillez prendre les mesures nécessaires.
        """

        # Envoyer des alertes aux professionnels
        for prof in professionals:
            if prof.get('email'):
                alert_service.send_email_alert(prof['email'], subject, message)
            if prof.get('phone'):
                alert_service.send_sms_alert(prof['phone'], message)
        
        # Envoyer une alerte aux proches
        for proche in patient.get('contacts', []):
            if proche.get('email'):
                alert_service.send_email_alert(proche['email'], subject, message)
            if proche.get('phone'):
                alert_service.send_sms_alert(proche['phone'], message)

def update_observation(observation_id, update_data):
    mongo.db.observations.update_one({"_id": ObjectId(observation_id)}, {"$set": update_data})

def delete_observation(observation_id):
    mongo.db.observations.delete_one({"_id": ObjectId(observation_id)})
