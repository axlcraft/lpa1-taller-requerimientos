#!/usr/bin/env python3
"""
Script para consolidar ciudades similares y eliminar duplicados
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

def consolidate_similar_cities():
    app = create_app()
    
    with app.app_context():
        print("🔍 Consolidando ciudades similares...")
        
        # Mapeo de ciudades similares que deben consolidarse
        consolidacion_map = {
            # Consolidar variaciones de Madrid
            "Madrid, España": "Madrid",
            # Consolidar variaciones de Cancún  
            "Cancún, México": "Cancún",
            # Consolidar variaciones de New York
            "New York, USA": "NewYork",
        }
        
        hoteles_actualizados = 0
        hoteles_eliminados = 0
        habitaciones_eliminadas = 0
        
        print("\n📋 Consolidaciones a realizar:")
        for ciudad_origen, ciudad_destino in consolidacion_map.items():
            hoteles_origen = Hotel.query.filter_by(ubicacion_geografica=ciudad_origen).all()
            hoteles_destino = Hotel.query.filter_by(ubicacion_geografica=ciudad_destino).all()
            
            if hoteles_origen:
                print(f"  {ciudad_origen} → {ciudad_destino} ({len(hoteles_origen)} hoteles)")
                
                # Si la ciudad destino ya tiene 2 hoteles, eliminar los de origen
                if len(hoteles_destino) >= 2:
                    print(f"    ⚠️  {ciudad_destino} ya tiene {len(hoteles_destino)} hoteles, eliminando hoteles de {ciudad_origen}")
                    
                    for hotel in hoteles_origen:
                        print(f"    🗑️  Eliminando: {hotel.nombre}")
                        
                        # Eliminar habitaciones del hotel
                        habitaciones = Habitacion.query.filter_by(hotel_id=hotel.id).all()
                        for habitacion in habitaciones:
                            db.session.delete(habitacion)
                            habitaciones_eliminadas += 1
                        
                        # Eliminar el hotel
                        db.session.delete(hotel)
                        hoteles_eliminados += 1
                
                else:
                    # Actualizar la ubicación de los hoteles
                    for hotel in hoteles_origen:
                        print(f"    📍 Moviendo: {hotel.nombre}")
                        hotel.ubicacion_geografica = ciudad_destino
                        db.session.add(hotel)
                        hoteles_actualizados += 1
        
        # Confirmar cambios
        db.session.commit()
        
        print(f"\n🎉 Consolidación completada!")
        print(f"📍 Hoteles actualizados: {hoteles_actualizados}")
        print(f"🗑️  Hoteles eliminados: {hoteles_eliminados}")
        print(f"🗑️  Habitaciones eliminadas: {habitaciones_eliminadas}")
        
        # Eliminar hoteles duplicados por nombre en la misma ciudad
        print(f"\n🔍 Buscando hoteles duplicados por nombre...")
        
        # Obtener hoteles agrupados por ciudad y nombre
        ciudades = db.session.query(Hotel.ubicacion_geografica).distinct().all()
        
        for (ciudad,) in ciudades:
            # Buscar nombres duplicados en esta ciudad
            nombres_count = db.session.query(
                Hotel.nombre,
                func.count(Hotel.id).label('count')
            ).filter_by(ubicacion_geografica=ciudad).group_by(Hotel.nombre).all()
            
            for nombre, count in nombres_count:
                if count > 1:
                    print(f"  ⚠️  {ciudad}: '{nombre}' aparece {count} veces")
                    
                    # Obtener todos los hoteles con este nombre en esta ciudad
                    hoteles_duplicados = Hotel.query.filter_by(
                        ubicacion_geografica=ciudad,
                        nombre=nombre
                    ).order_by(Hotel.id).all()
                    
                    # Mantener solo el primero, eliminar el resto
                    for hotel in hoteles_duplicados[1:]:
                        print(f"    🗑️  Eliminando duplicado: {hotel.nombre}")
                        
                        # Eliminar habitaciones del hotel
                        habitaciones = Habitacion.query.filter_by(hotel_id=hotel.id).all()
                        for habitacion in habitaciones:
                            db.session.delete(habitacion)
                            habitaciones_eliminadas += 1
                        
                        # Eliminar el hotel
                        db.session.delete(hotel)
                        hoteles_eliminados += 1
        
        # Confirmar cambios finales
        db.session.commit()
        
        # Mostrar estadísticas finales
        print(f"\n📊 Estadísticas finales:")
        total_hoteles = Hotel.query.count()
        total_habitaciones = Habitacion.query.count()
        print(f"📈 Total hoteles: {total_hoteles}")
        print(f"📈 Total habitaciones: {total_habitaciones}")
        
        # Mostrar distribución final por ciudad
        print(f"\n🏙️  Distribución final por ciudad:")
        print("Ciudad → Cantidad de hoteles")
        print("-" * 40)
        ciudades_finales = db.session.query(
            Hotel.ubicacion_geografica,
            func.count(Hotel.id).label('count')
        ).group_by(Hotel.ubicacion_geografica).order_by(Hotel.ubicacion_geografica).all()
        
        for ciudad, count in ciudades_finales:
            print(f"{ciudad} → {count} hoteles")

if __name__ == "__main__":
    consolidate_similar_cities()