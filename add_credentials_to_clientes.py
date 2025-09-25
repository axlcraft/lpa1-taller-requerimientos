"""
Script seguro para añadir las columnas `username` y `password_hash` a la tabla `clientes`.
Idempotente y compatible con SQLite/MySQL.

Ejecútalo desde la raíz del proyecto:
    export PYTHONPATH=$(pwd)
    source venv/bin/activate
    python3 add_credentials_to_clientes.py
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
    to_add = []
    if 'username' not in existing:
        to_add.append(('username', 'VARCHAR(80)'))
    if 'password_hash' not in existing:
        to_add.append(('password_hash', 'VARCHAR(200)'))

    if not to_add:
        print('No hay columnas de credenciales faltantes en clientes.')
    else:
        print('Columnas a añadir:', [c[0] for c in to_add])
        for col, col_type in to_add:
            ddl = f"ALTER TABLE clientes ADD COLUMN {col} {col_type}"
            if db.engine.dialect.name in ('mysql', 'mariadb'):
                # permitir NULL y añadir UNIQUE para username manualmente si se desea
                if col == 'username':
                    ddl += ' NULL'
                else:
                    ddl += ' NULL'
            try:
                print('Ejecutando:', ddl)
                with db.engine.begin() as conn:
                    conn.execute(text(ddl))
                print(f'Columna {col} añadida correctamente.')
            except Exception as e:
                print(f'Error al añadir columna {col}:', str(e))

        # Opcional: crear índice/constraint de UNIQUE para username si no existe (MySQL)
        if 'username' in [c[0] for c in to_add] and db.engine.dialect.name in ('mysql', 'mariadb'):
            try:
                print('Intentando crear índice UNIQUE para username (si no existe)...')
                with db.engine.begin() as conn:
                    conn.execute(text("ALTER TABLE clientes ADD UNIQUE INDEX ux_clientes_username (username)"))
                print('Índice UNIQUE creado para username.')
            except Exception as e:
                print('No se pudo crear índice UNIQUE para username (tal vez ya existe):', str(e))

    print('Proceso finalizado.')
