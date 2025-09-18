# app/config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///hotel_reservas.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # Configuración adicional para el desarrollo
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
