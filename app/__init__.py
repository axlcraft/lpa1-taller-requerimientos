# app/__init__.py
from flask import Flask
from app.extensions import db
from app.config import config
import os

def create_app(config_name=None):
    """Factory function para crear la aplicación Flask."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    flask_app = Flask(__name__)
    flask_app.config.from_object(config.get(config_name, config['default']))

    # Inicializar extensiones
    db.init_app(flask_app)
    # Evitar que los objetos expiren después de commit (mejora ergonomía en tests)
    with flask_app.app_context():
        try:
            db.session.expire_on_commit = False
        except Exception:
            # En algunos entornos el session puede no estar creado aún; ignorar silenciosamente
            pass

    # Función para inyectar variables globales en templates
    @flask_app.context_processor
    def inject_global_vars():
        return {
            'app_name': 'LuxeStay Premier',
            'app_tagline': 'Experiencias Hoteleras de Lujo'
        }

    # Filtro personalizado para fechas en español
    @flask_app.template_filter('fecha_es')
    def fecha_es(date, format_str='%d de %B de %Y'):
        """Formatea una fecha con nombres de mes en español."""
        if not date:
            return ''
        
        # Diccionario de meses en español
        meses_es = {
            'January': 'enero', 'February': 'febrero', 'March': 'marzo',
            'April': 'abril', 'May': 'mayo', 'June': 'junio',
            'July': 'julio', 'August': 'agosto', 'September': 'septiembre',
            'October': 'octubre', 'November': 'noviembre', 'December': 'diciembre'
        }
        
        # Formatear la fecha primero en inglés
        fecha_str = date.strftime(format_str)
        
        # Reemplazar nombres de mes en inglés por español
        for mes_en, mes_es in meses_es.items():
            fecha_str = fecha_str.replace(mes_en, mes_es)
        
        return fecha_str

    # Registrar blueprints
    try:
        from app.routes.main import main_bp
        flask_app.register_blueprint(main_bp)
    except ImportError as e:
        print(f"Warning: Could not import main blueprint: {e}")

    try:
        from app.routes.auth import auth_bp
        flask_app.register_blueprint(auth_bp, url_prefix='/auth')
    except ImportError as e:
        print(f"Warning: Could not import auth blueprint: {e}")

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
        from app.routes.pagos import pagos_bp
        flask_app.register_blueprint(pagos_bp, url_prefix='/pagos')
    except ImportError as e:
        print(f"Warning: Could not import pagos blueprint: {e}")

    try:
        from app.routes.evaluaciones import evaluaciones_bp
        flask_app.register_blueprint(evaluaciones_bp, url_prefix='/evaluaciones')
    except ImportError as e:
        print(f"Warning: Could not import evaluaciones blueprint: {e}")

    try:
        from app.routes.promociones import promociones_bp
        flask_app.register_blueprint(promociones_bp, url_prefix='/promociones')
    except ImportError as e:
        print(f"Warning: Could not import promociones blueprint: {e}")

    try:
        from app.routes.politicas import politicas_bp
        flask_app.register_blueprint(politicas_bp, url_prefix='/politicas')
    except ImportError as e:
        print(f"Warning: Could not import politicas blueprint: {e}")

    try:
        from app.routes.temporadas import temporadas_bp
        flask_app.register_blueprint(temporadas_bp, url_prefix='/temporadas')
    except ImportError as e:
        print(f"Warning: Could not import temporadas blueprint: {e}")

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
