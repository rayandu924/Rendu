# backend/models/appointment.py

from . import mongo
from bson.objectid import ObjectId

def get_all_appointments():
    return list(mongo.db.appointments.aggregate([
        {
            "$lookup": {
                "from": "patients",
                "localField": "patient_id",
                "foreignField": "_id",
                "as": "patient"
            }
        },
        {
            "$lookup": {
                "from": "professionals",
                "localField": "professional_id",
                "foreignField": "_id",
                "as": "professional"
            }
        },
        {
            "$unwind": {
                "path": "$patient",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$unwind": {
                "path": "$professional",
                "preserveNullAndEmptyArrays": True
            }
        }
    ]))

def get_appointment_by_id(appointment_id):
    return mongo.db.appointments.aggregate([
        {"$match": {"_id": ObjectId(appointment_id)}},
        {
            "$lookup": {
                "from": "patients",
                "localField": "patient_id",
                "foreignField": "_id",
                "as": "patient"
            }
        },
        {
            "$lookup": {
                "from": "professionals",
                "localField": "professional_id",
                "foreignField": "_id",
                "as": "professional"
            }
        },
        {
            "$unwind": {
                "path": "$patient",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$unwind": {
                "path": "$professional",
                "preserveNullAndEmptyArrays": True
            }
        }
    ])

def create_appointment(appointment_data):
    mongo.db.appointments.insert_one(appointment_data)

def update_appointment(appointment_id, update_data):
    mongo.db.appointments.update_one({"_id": ObjectId(appointment_id)}, {"$set": update_data})

def delete_appointment(appointment_id):
    mongo.db.appointments.delete_one({"_id": ObjectId(appointment_id)})
