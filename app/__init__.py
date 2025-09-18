# app/__init__.py
from flask import Flask
from app.extensions import db
from app.config import Config

def create_app():
    """Factory function para crear la aplicación Flask."""
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(flask_app)

    # Función para inyectar variables globales en templates
    @flask_app.context_processor
    def inject_global_vars():
        return {
            'app_name': 'Sistema de Reservas Hoteleras'
        }

    # Registrar blueprints
    try:
        from app.routes.main import main_bp
        flask_app.register_blueprint(main_bp)
    except ImportError as e:
        print(f"Warning: Could not import main blueprint: {e}")

    try:
        from app.routes.hoteles import hoteles_bp
        flask_app.register_blueprint(hoteles_bp, url_prefix='/hoteles')
    except ImportError as e:
        print(f"Warning: Could not import hoteles blueprint: {e}")

    try:
        from app.routes.habitaciones import habitaciones_bp
        flask_app.register_blueprint(habitaciones_bp, url_prefix='/habitaciones')
    except ImportError as e:
        print(f"Warning: Could not import habitaciones blueprint: {e}")

    try:
        from app.routes.clientes import clientes_bp
        flask_app.register_blueprint(clientes_bp, url_prefix='/clientes')
    except ImportError as e:
        print(f"Warning: Could not import clientes blueprint: {e}")

    try:
        from app.routes.reservas import reservas_bp
        flask_app.register_blueprint(reservas_bp, url_prefix='/reservas')
    except ImportError as e:
        print(f"Warning: Could not import reservas blueprint: {e}")

    try:
        from app.routes.evaluaciones import evaluaciones_bp
        flask_app.register_blueprint(evaluaciones_bp, url_prefix='/evaluaciones')
    except ImportError as e:
        print(f"Warning: Could not import evaluaciones blueprint: {e}")

    # Crear tablas
    with flask_app.app_context():
        try:
            # Importar todos los modelos para asegurar que las tablas se creen
            import app.models
            db.create_all()
            print("✅ Tablas de base de datos creadas exitosamente")
        except Exception as e:
            print(f"❌ Error al crear tablas: {e}")

    return flask_app
