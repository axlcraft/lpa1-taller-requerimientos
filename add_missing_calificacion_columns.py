"""
Script seguro para añadir columnas faltantes en la tabla `calificaciones`.
Usa el inspector de SQLAlchemy para detectar columnas ya existentes y ejecuta
ALTER TABLE ADD COLUMN sólo cuando haga falta. Compatible con SQLite y MySQL.

Ejecútalo desde la raíz del proyecto:
    python add_missing_calificacion_columns.py
"""
from app import create_app
from app.extensions import db
from sqlalchemy import inspect, text

app = create_app()

REQUIRED_COLUMNS = {
    'estrellas_hotel': 'INTEGER',
    'estrellas_habitacion': 'INTEGER',
    'estrellas_atencion': 'INTEGER',
    'hotel_id': 'VARCHAR(36)',
}

with app.app_context():
    inspector = inspect(db.engine)
    if 'calificaciones' not in inspector.get_table_names():
        print("Tabla 'calificaciones' no encontrada. Asegúrate de tener las migraciones o el modelo creado.")
        raise SystemExit(1)

    existing = [c['name'] for c in inspector.get_columns('calificaciones')]
    to_add = [col for col in REQUIRED_COLUMNS.keys() if col not in existing]

    if not to_add:
        print('No hay columnas faltantes en calificaciones.')
    else:
        print('Columnas a añadir:', to_add)
        for col in to_add:
            col_type = REQUIRED_COLUMNS[col]
            # Añadimos columnas como NULLABLE para no romper filas existentes.
            ddl = f"ALTER TABLE calificaciones ADD COLUMN {col} {col_type}"
            # Para MySQL/MariaDB, asegurar DEFAULT NULL explícito evita problemas en algunos motores
            if db.engine.dialect.name in ('mysql', 'mariadb'):
                ddl += ' NULL'
            try:
                print('Ejecutando:', ddl)
                # Usar una conexión para ejecutar DDL con SQLAlchemy moderno
                with db.engine.begin() as conn:
                    conn.execute(text(ddl))
                print(f'Columna {col} añadida correctamente.')
            except Exception as e:
                print(f'Error al añadir columna {col}:', str(e))

        # Opcional: inicializar valores nulos a 3 (valor medio) si se desea
        try:
            print('Inicializando valores NULL a 3 para las columnas recién creadas...')
            # Solo inicializar las columnas de estrellas a 3. No tocar hotel_id aquí.
            stars = [c for c in to_add if c.startswith('estrellas')]
            if stars:
                set_clause = ', '.join([f"{c}=COALESCE({c}, 3)" for c in stars])
                where_clause = ' OR '.join([f"{c} IS NULL" for c in stars])
                update_sql = f"UPDATE calificaciones SET {set_clause} WHERE {where_clause}"
                db.session.execute(text(update_sql))
                db.session.commit()
                print('Inicialización de estrellas completada.')

            # Si añadimos hotel_id, intentar rellenarla desde la relación habitacion -> hotel
            if 'hotel_id' in to_add:
                try:
                    print('Rellenando hotel_id desde habitaciones (si es posible)...')
                    # Actualiza calificaciones.hotel_id con habitaciones.hotel_id usando subconsulta
                    backfill_sql = (
                        "UPDATE calificaciones c "
                        "JOIN habitaciones h ON h.id = c.habitacion_id "
                        "SET c.hotel_id = h.hotel_id WHERE c.hotel_id IS NULL"
                    )
                    # Si el motor no soporta JOIN en UPDATE (SQLite), usar una forma alternativa
                    if db.engine.dialect.name in ('sqlite',):
                        backfill_sql = (
                            "UPDATE calificaciones SET hotel_id = ("
                            "SELECT hotel_id FROM habitaciones WHERE habitaciones.id = calificaciones.habitacion_id) "
                            "WHERE hotel_id IS NULL"
                        )
                    db.session.execute(text(backfill_sql))
                    db.session.commit()
                    print('Backfill de hotel_id completado.')
                except Exception as e:
                    db.session.rollback()
                    print('No se pudo rellenar hotel_id automáticamente:', str(e))
        except Exception as e:
            db.session.rollback()
            print('Error al inicializar valores de columnas:', str(e))

    print('Proceso finalizado.')
