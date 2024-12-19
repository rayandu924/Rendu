# backend/models/professional.py

from . import mongo
from bson.objectid import ObjectId

def get_all_professionals():
    return list(mongo.db.professionals.find())

def get_professional_by_id(professional_id):
    return mongo.db.professionals.find_one({"_id": ObjectId(professional_id)})

def create_professional(professional_data):
    mongo.db.professionals.insert_one(professional_data)

def update_professional(professional_id, update_data):
    mongo.db.professionals.update_one({"_id": ObjectId(professional_id)}, {"$set": update_data})

def delete_professional(professional_id):
    mongo.db.professionals.delete_one({"_id": ObjectId(professional_id)})
