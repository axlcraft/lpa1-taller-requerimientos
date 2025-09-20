# app/config.py
import os
from urllib.parse import quote_plus

class Config:
    """Configuración base para la aplicación."""
    
    # Base de datos
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///hotel_reservas.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Seguridad
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # Configuración adicional para el desarrollo
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True

class DevelopmentConfig(Config):
    """Configuración para desarrollo con MySQL."""
    DEBUG = True
    # Ejemplo de cadena de conexión MySQL:
    # mysql+pymysql://usuario:contraseña@localhost/nombre_base
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL",
        "mysql+pymysql://hoteluser:hotelpass@localhost/hotel_reservas"
    )

class ProductionConfig(Config):
    """Configuración para producción."""
    DEBUG = False
    TEMPLATES_AUTO_RELOAD = False
    
    # Para PostgreSQL en producción
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

class TestConfig(Config):
    """Configuración para testing."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

# Mapeo de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestConfig,
    'default': DevelopmentConfig
}
