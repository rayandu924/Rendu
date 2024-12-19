# backend/models/device.py

from . import mongo
from bson.objectid import ObjectId

def get_all_devices():
    return list(mongo.db.devices.aggregate([
        {
            "$lookup": {
                "from": "patients",
                "localField": "patient_id",
                "foreignField": "_id",
                "as": "patient"
            }
        },
        {
            "$unwind": {
                "path": "$patient",
                "preserveNullAndEmptyArrays": True
            }
        }
    ]))

def get_device_by_id(device_id):
    return mongo.db.devices.aggregate([
        {"$match": {"_id": ObjectId(device_id)}},
        {
            "$lookup": {
                "from": "patients",
                "localField": "patient_id",
                "foreignField": "_id",
                "as": "patient"
            }
        },
        {
            "$unwind": {
                "path": "$patient",
                "preserveNullAndEmptyArrays": True
            }
        }
    ])

def create_device(device_data):
    mongo.db.devices.insert_one(device_data)

def update_device(device_id, update_data):
    mongo.db.devices.update_one({"_id": ObjectId(device_id)}, {"$set": update_data})

def delete_device(device_id):
    mongo.db.devices.delete_one({"_id": ObjectId(device_id)})
