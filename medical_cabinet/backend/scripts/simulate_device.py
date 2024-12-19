import requests
import time
import random
from datetime import datetime
import os

# Configuration
API_URL = os.getenv('API_URL', 'http://localhost:5000/api/observations')
LOGIN_URL = os.getenv('LOGIN_URL', 'http://localhost:5000/api/auth/login')
USERNAME = os.getenv('SIMULATE_USERNAME', 'medecin1')  # Nom d'utilisateur par défaut
PASSWORD = os.getenv('SIMULATE_PASSWORD', 'medecin123')  # Mot de passe par défaut

def get_jwt_token(username, password):
    """
    Obtient un token JWT en se connectant à l'API.
    """
    payload = {
        'username': username,
        'password': password
    }
    try:
        response = requests.post(LOGIN_URL, json=payload)
        if response.status_code == 200:
            token = response.json().get('access_token')
            if token:
                print(f"Token obtenu pour l'utilisateur {username}")
                return token
            else:
                print("Échec de l'obtention du token : clé 'access_token' manquante.")
        else:
            print(f"Échec de la connexion : {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Erreur lors de la connexion : {e}")
    return None

def get_random_patient_id(token):
    """
    Récupère un ID de patient aléatoire depuis le backend.
    """
    headers = {'Authorization': f'Bearer {token}'}
    try:
        response = requests.get('http://localhost:5000/api/patients', headers=headers)
        if response.status_code == 200:
            patients = response.json()
            if patients:
                patient = random.choice(patients)
                print(f"Patient sélectionné : {patient['_id']}")
                return patient['_id']
            else:
                print("Aucun patient disponible.")
        else:
            print(f"Échec de la récupération des patients : {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Erreur lors de la récupération des patients : {e}")
    return None

def send_observation(token, patient_id):
    """
    Envoie une observation pour un patient donné.
    """
    headers = {'Authorization': f'Bearer {token}'}
    observation = {
        "patient_id": patient_id,
        "date": datetime.utcnow().isoformat(),
        "tension_systolic": random.randint(110, 140),
        "tension_diastolic": random.randint(70, 90),
        "rythme_cardiaque": random.randint(60, 100),
        "oxymetrie": random.randint(95, 100)
    }
    try:
        response = requests.post(API_URL, json=observation, headers=headers)
        if response.status_code == 201:
            print(f"Observation envoyée pour le patient {patient_id}")
        else:
            print(f"Échec de l'envoi de l'observation : {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'observation : {e}")

def main():
    # Obtenir le token JWT
    token = get_jwt_token(USERNAME, PASSWORD)
    if not token:
        print("Impossible d'obtenir un token. Arrêt du script.")
        return

    while True:
        patient_id = get_random_patient_id(token)
        if patient_id:
            send_observation(token, patient_id)
        else:
            print("Aucun patient trouvé pour envoyer des observations.")
        time.sleep(60)  # Envoyer toutes les minutes

if __name__ == '__main__':
    main()
