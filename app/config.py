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
    # Evitar que SQLAlchemy expire objetos después de commit en el session (útil para tests)
    SQLALCHEMY_SESSION_OPTIONS = {
        'expire_on_commit': False
    }
    
    # Seguridad
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # Configuración adicional para el desarrollo
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    # Credenciales de superusuario (para desarrollo). Cambiar en producción.
    SUPERUSER_USERNAME = os.environ.get('SUPERUSER_USERNAME', 'admin')
    SUPERUSER_PASSWORD = os.environ.get('SUPERUSER_PASSWORD', 'admin123')

class DevelopmentConfig(Config):
    """Configuración para desarrollo con SQLite."""
    DEBUG = True
    # Usar SQLite por defecto para desarrollo local
    # Para MySQL, configurar DEV_DATABASE_URL:
    # mysql+pymysql://usuario:contraseña@localhost/nombre_base
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL",
        "sqlite:///hotel_reservas.db"
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
