# backend/models/__init__.py

from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

# Initialisation de PyMongo et Bcrypt
mongo = PyMongo()
bcrypt = Bcrypt()

def init_db(app):
    mongo.init_app(app)
    bcrypt.init_app(app)
