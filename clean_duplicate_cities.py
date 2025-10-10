#!/usr/bin/env python3
"""
Script para eliminar hoteles con ciudades duplicadas
"""
import os
import sys

# Agregar el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models.hotel import Hotel
from app.models.habitacion import Habitacion
from sqlalchemy import func

def clean_duplicate_cities():
    app = create_app()
    
    with app.app_context():
        print("🔍 Analizando ciudades duplicadas...")
        
        # Obtener ciudades con conteo
        ciudades_count = db.session.query(
            Hotel.ubicacion_geografica,
            func.count(Hotel.id).label('count')
        ).group_by(Hotel.ubicacion_geografica).all()
        
        print("\n📊 Estadísticas actuales:")
        print("Ciudad → Cantidad de hoteles")
        print("-" * 40)
        
        ciudades_duplicadas = []
        for ciudad, count in ciudades_count:
            print(f"{ciudad} → {count} hoteles")
            if count > 2:  # Más de 2 hoteles por ciudad
                ciudades_duplicadas.append((ciudad, count))
        
        if not ciudades_duplicadas:
            print("\n✅ No hay ciudades con más de 2 hoteles.")
            return
        
        print(f"\n⚠️  Encontradas {len(ciudades_duplicadas)} ciudades con más de 2 hoteles:")
        
        hoteles_eliminados = 0
        habitaciones_eliminadas = 0
        
        for ciudad, count in ciudades_duplicadas:
            print(f"\n🏙️  Procesando: {ciudad} (tiene {count} hoteles)")
            
            # Obtener todos los hoteles de esta ciudad, ordenados por ID
            hoteles_ciudad = Hotel.query.filter_by(
                ubicacion_geografica=ciudad
            ).order_by(Hotel.id).all()
            
            # Mantener solo los primeros 2 hoteles, eliminar el resto
            hoteles_a_eliminar = hoteles_ciudad[2:]  # Desde el tercer hotel en adelante
            
            for hotel in hoteles_a_eliminar:
                print(f"  🗑️  Eliminando hotel: {hotel.nombre}")
                
                # Eliminar habitaciones del hotel
                habitaciones = Habitacion.query.filter_by(hotel_id=hotel.id).all()
                for habitacion in habitaciones:
                    db.session.delete(habitacion)
                    habitaciones_eliminadas += 1
                
                # Eliminar el hotel
                db.session.delete(hotel)
                hoteles_eliminados += 1
        
        # Confirmar cambios
        db.session.commit()
        
        print(f"\n🎉 Limpieza completada!")
        print(f"🗑️  Hoteles eliminados: {hoteles_eliminados}")
        print(f"🗑️  Habitaciones eliminadas: {habitaciones_eliminadas}")
        
        # Mostrar estadísticas finales
        print(f"\n📊 Estadísticas finales:")
        total_hoteles = Hotel.query.count()
        total_habitaciones = Habitacion.query.count()
        print(f"📈 Total hoteles restantes: {total_hoteles}")
        print(f"📈 Total habitaciones restantes: {total_habitaciones}")
        
        # Mostrar distribución final por ciudad
        print(f"\n🏙️  Distribución final por ciudad:")
        print("Ciudad → Cantidad de hoteles")
        print("-" * 40)
        ciudades_finales = db.session.query(
            Hotel.ubicacion_geografica,
            func.count(Hotel.id).label('count')
        ).group_by(Hotel.ubicacion_geografica).all()
        
        for ciudad, count in ciudades_finales:
            print(f"{ciudad} → {count} hoteles")

if __name__ == "__main__":
    clean_duplicate_cities()