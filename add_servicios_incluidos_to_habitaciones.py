#!/usr/bin/env python3
"""
Script para agregar la columna servicios_incluidos a la tabla habitaciones
"""
import sqlite3
import os

# Obtener la ruta de la base de datos
db_path = os.path.join(os.path.dirname(__file__), 'hotel.db')

def main():
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar si la columna ya existe
        cursor.execute("PRAGMA table_info(habitaciones)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'servicios_incluidos' not in columns:
            print("Agregando columna 'servicios_incluidos' a la tabla habitaciones...")
            cursor.execute("""
                ALTER TABLE habitaciones 
                ADD COLUMN servicios_incluidos TEXT DEFAULT 'Wi-Fi gratuito, Aire acondicionado, TV por cable'
            """)
            conn.commit()
            print("✅ Columna 'servicios_incluidos' agregada exitosamente.")
        else:
            print("✅ La columna 'servicios_incluidos' ya existe.")
        
        # Llenar con datos de ejemplo para habitaciones que no tengan servicios
        cursor.execute("""
            UPDATE habitaciones 
            SET servicios_incluidos = CASE 
                WHEN tipo = 'SUITE' THEN 'Wi-Fi gratuito, Aire acondicionado, TV por cable, Minibar, Jacuzzi, Balcón, Room service 24h'
                WHEN tipo = 'DELUXE' THEN 'Wi-Fi gratuito, Aire acondicionado, TV por cable, Minibar, Balcón, Room service'
                WHEN tipo = 'ESTANDAR' THEN 'Wi-Fi gratuito, Aire acondicionado, TV por cable, Escritorio'
                WHEN tipo = 'ECONOMICA' THEN 'Wi-Fi gratuito, TV básica, Ventilador'
                ELSE 'Wi-Fi gratuito, Aire acondicionado, TV por cable'
            END
            WHERE servicios_incluidos IS NULL OR servicios_incluidos = ''
        """)
        
        conn.commit()
        
        # Verificar que se aplicaron los cambios
        cursor.execute("SELECT COUNT(*) FROM habitaciones WHERE servicios_incluidos IS NOT NULL")
        count = cursor.fetchone()[0]
        print(f"✅ Se actualizaron {count} habitaciones con servicios incluidos.")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Migración completada exitosamente.")
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")

if __name__ == "__main__":
    main()