"""
Script para agregar la columna servicios_incluidos a la tabla habitaciones
"""
import sqlite3
from app import create_app
from app.extensions import db
from sqlalchemy import text

def migrate_add_servicios_column():
    """Agregar la columna servicios_incluidos a la tabla habitaciones"""
    app = create_app()
    
    with app.app_context():
        # Usar SQLAlchemy para ejecutar SQL crudo
        try:
            # Verificar si la columna ya existe
            result = db.session.execute(text("PRAGMA table_info(habitaciones)"))
            columns = [row[1] for row in result]
            
            if 'servicios_incluidos' not in columns:
                print("Agregando columna servicios_incluidos a tabla habitaciones...")
                db.session.execute(text("ALTER TABLE habitaciones ADD COLUMN servicios_incluidos TEXT"))
                db.session.commit()
                print("✅ Columna agregada exitosamente")
            else:
                print("La columna servicios_incluidos ya existe")
                
        except Exception as e:
            print(f"Error durante la migración: {e}")

if __name__ == '__main__':
    migrate_add_servicios_column()