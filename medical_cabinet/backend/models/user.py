# backend/models/user.py

from . import mongo, bcrypt
from bson.objectid import ObjectId

def get_user_by_username(username):
    return mongo.db.users.find_one({"username": username})

def get_user_by_id(user_id):
    return mongo.db.users.find_one({"_id": ObjectId(user_id)})

def create_user(user_data):
    hashed_password = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
    user_data['password'] = hashed_password
    mongo.db.users.insert_one(user_data)

def update_user(user_id, update_data):
    if 'password' in update_data:
        update_data['password'] = bcrypt.generate_password_hash(update_data['password']).decode('utf-8')
    mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})

def delete_user(user_id):
    mongo.db.users.delete_one({"_id": ObjectId(user_id)})

def get_all_users():
    return list(mongo.db.users.find())
