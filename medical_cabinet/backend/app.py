import logging
from flask import Flask
from flask_cors import CORS
from config import Config
from models import init_db
from routes.auth import auth_bp
from routes.patients import patients_bp
from routes.professionals import professionals_bp
from routes.appointments import appointments_bp
from routes.devices import devices_bp
from routes.observations import observations_bp
from routes.users import users_bp
from services.fhir_service import fhir_bp
from scripts.populate_db import populate_db  # Importez votre script de peuplement

# Configuration du logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s',
                    handlers=[
                        logging.FileHandler("backend.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialiser la base de données et Bcrypt
    init_db(app)

    # Activer CORS avec des origines spécifiques
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:8000"}})

    # Enregistrer les blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api')
    app.register_blueprint(patients_bp, url_prefix='/api')
    app.register_blueprint(professionals_bp, url_prefix='/api')
    app.register_blueprint(appointments_bp, url_prefix='/api')
    app.register_blueprint(devices_bp, url_prefix='/api')
    app.register_blueprint(observations_bp, url_prefix='/api')
    app.register_blueprint(fhir_bp, url_prefix='/api')  # Blueprint FHIR
    
    populate_db()

    @app.route('/')
    def index():
        return "API du Cabinet Médical"

    return app

# Créez l'application au niveau global
app = create_app()

if __name__ == '__main__':
    logger.info("Démarrage de l'application Flask")
    app.run(debug=True)
