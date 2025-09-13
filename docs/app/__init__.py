# app/__init__.py
from flask import Flask
from .config import Config
from .extensions import db

def create_app(config_object=Config):
    """Application factory for Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Inicializar extensiones
    db.init_app(app)

    # registrar blueprints, comandos, etc.
    with app.app_context():
        # importar modelos para que SQLAlchemy los registre
        from .models import *  # noqa: F401,F403
        db.create_all()  # solo para desarrollo; en producción usar migraciones

    return app
