# backend/models/patient.py

from . import mongo
from bson.objectid import ObjectId

def get_all_patients():
    return list(mongo.db.patients.find())

def get_patient_by_id(patient_id):
    return mongo.db.patients.find_one({"_id": ObjectId(patient_id)})

def create_patient(patient_data):
    mongo.db.patients.insert_one(patient_data)

def update_patient(patient_id, update_data):
    mongo.db.patients.update_one({"_id": ObjectId(patient_id)}, {"$set": update_data})

def delete_patient(patient_id):
    mongo.db.patients.delete_one({"_id": ObjectId(patient_id)})
