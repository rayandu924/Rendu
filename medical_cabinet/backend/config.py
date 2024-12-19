# backend/config.py

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'votre_clé_secrète'
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://mongo:27017/medical_cabinet'
    
    # JWT Configuration (si utilisé)
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'votre_jwt_clé_secrète'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 heure

    # SMTP Configuration
    #SMTP_SERVER = os.environ.get('SMTP_SERVER') or 'smtp.gmail.com'
    #SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
    #SMTP_USERNAME = os.environ.get('SMTP_USERNAME') or 'votre_email@gmail.com'
    #SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD') or 'votre_mot_de_passe'
#
    ## Twilio Configuration (pour SMS)
    #TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID') or 'votre_account_sid'
    #TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN') or 'votre_auth_token'
    #TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER') or '+1234567890'
