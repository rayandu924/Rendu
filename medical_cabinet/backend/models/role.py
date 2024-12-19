# backend/models/role.py

from . import mongo
from bson.objectid import ObjectId

def get_role_by_name(role_name):
    return mongo.db.roles.find_one({"name": role_name})

def get_all_roles():
    return list(mongo.db.roles.find())

def create_role(role_data):
    mongo.db.roles.insert_one(role_data)

def update_role(role_id, update_data):
    mongo.db.roles.update_one({"_id": ObjectId(role_id)}, {"$set": update_data})

def delete_role(role_id):
    mongo.db.roles.delete_one({"_id": ObjectId(role_id)})
