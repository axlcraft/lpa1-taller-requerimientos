"""
Script seguro para añadir la columna `is_admin` a la tabla `clientes`.
Funciona similar a `add_missing_calificacion_columns.py` y es idempotente.

Ejecútalo desde la raíz del proyecto:
    python add_is_admin_to_clientes.py
"""
from app import create_app
from app.extensions import db
from sqlalchemy import inspect, text

app = create_app()

with app.app_context():
    inspector = inspect(db.engine)
    if 'clientes' not in inspector.get_table_names():
        print("Tabla 'clientes' no encontrada. Asegúrate de tener las migraciones o el modelo creado.")
        raise SystemExit(1)

    existing = [c['name'] for c in inspector.get_columns('clientes')]
    if 'is_admin' in existing:
        print('La columna is_admin ya existe en clientes. Nada que hacer.')
    else:
        col_type = 'BOOLEAN'
        ddl = f"ALTER TABLE clientes ADD COLUMN is_admin {col_type}"
        if db.engine.dialect.name in ('mysql', 'mariadb'):
            ddl += ' NOT NULL DEFAULT 0'
        try:
            print('Ejecutando:', ddl)
            with db.engine.begin() as conn:
                conn.execute(text(ddl))
            print('Columna is_admin añadida correctamente.')
        except Exception as e:
            print('Error al añadir columna is_admin:', str(e))

        # Para bases SQLite, las columnas booleanas permitirán NULL; normalizamos a False donde sea NULL
        try:
            print('Normalizando valores NULL a 0 para is_admin...')
            update_sql = "UPDATE clientes SET is_admin = 0 WHERE is_admin IS NULL"
            db.session.execute(text(update_sql))
            db.session.commit()
            print('Normalización completada.')
        except Exception as e:
            db.session.rollback()
            print('No se pudo normalizar is_admin:', str(e))

    print('Proceso finalizado.')
