# backend/scripts/populate_db.py

import os
from pymongo import MongoClient
from flask_bcrypt import Bcrypt

# Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongo:27017/medical_cabinet')

# Initialiser Bcrypt
bcrypt = Bcrypt()

# Connexion à MongoDB
client = MongoClient(MONGO_URI)
db = client.get_default_database()

def hash_password(plain_password):
    return bcrypt.generate_password_hash(plain_password).decode('utf-8')

def populate_roles():
    roles = [
        {
            "name": "administrateur",
            "permissions": [
                "create_user",
                "read_user",
                "update_user",
                "delete_user",
                "create_patient",
                "read_patient",
                "update_patient",
                "delete_patient",
                "create_professional",
                "read_professional",
                "update_professional",
                "delete_professional",
                "create_appointment",
                "read_appointment",
                "update_appointment",
                "delete_appointment",
                "create_device",
                "read_device",
                "update_device",
                "delete_device",
                "create_observation",
                "read_observation",
                "update_observation",
                "delete_observation"
            ]
        },
        {
            "name": "medecin",
            "permissions": [
                "create_patient",
                "read_patient",
                "update_patient",
                "delete_patient",
                "create_professional",
                "read_professional",
                "update_professional",
                "delete_professional",
                "create_appointment",
                "read_appointment",
                "update_appointment",
                "delete_appointment",
                "create_device",
                "read_device",
                "update_device",
                "delete_device",
                "create_observation",
                "read_observation",
                "update_observation",
                "delete_observation"
            ]
        },
        {
            "name": "secretaire",
            "permissions": [
                "create_patient",
                "read_patient",
                "update_patient",
                "delete_patient",
                "create_appointment",
                "read_appointment",
                "update_appointment",
                "delete_appointment",
                "create_device",
                "read_device",
                "update_device",
                "delete_device",
                "create_observation",
                "read_observation",
                "update_observation",
                "delete_observation"
            ]
        },
        {
            "name": "service_externe",
            "permissions": [
                "read_device",
                "read_observation"
            ]
        }
    ]
    
    for role in roles:
        existing_role = db.roles.find_one({"name": role['name']})
        if not existing_role:
            db.roles.insert_one(role)
            print(f"Rôle '{role['name']}' créé.")
        else:
            print(f"Rôle '{role['name']}' existe déjà.")

def populate_users():
    users = [
        {
            'username': 'admin',
            'password': 'admin123',  # Changez ce mot de passe en production
            'roles': ['administrateur']
        },
        {
            'username': 'medecin1',
            'password': 'medecin123',
            'roles': ['medecin']
        },
        {
            'username': 'secretaire1',
            'password': 'secretaire123',
            'roles': ['secretaire']
        },
        {
            'username': 'service1',
            'password': 'service123',
            'roles': ['service_externe']
        }
    ]

    for user in users:
        existing_user = db.users.find_one({"username": user['username']})
        if not existing_user:
            hashed_password = hash_password(user['password'])
            user['password'] = hashed_password
            db.users.insert_one(user)
            print(f"Utilisateur '{user['username']}' créé.")
        else:
            print(f"Utilisateur '{user['username']}' existe déjà.")

def populate_db():
    print("Début de l'initialisation de la base de données...")
    populate_roles()
    populate_users()
    print("Initialisation de la base de données terminée.")

if __name__ == '__main__':
    populate_db()
