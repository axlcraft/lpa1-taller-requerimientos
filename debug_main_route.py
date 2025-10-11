#!/usr/bin/env python3
"""Debug script para verificar la ruta principal"""

from app import create_app
from app.models import Hotel, Habitacion, Cliente, Reserva
from app.models.enums import EstadoHotel, EstadoHabitacion
from app.extensions import db

app = create_app()

with app.app_context():
    print("=== DEBUGGING RUTA PRINCIPAL ===\n")
    
    # Obtener datos como lo hace la ruta principal
    hoteles_destacados = Hotel.query.filter_by(estado=EstadoHotel.ACTIVO).limit(6).all()
    num_hoteles = Hotel.query.filter_by(estado=EstadoHotel.ACTIVO).count()
    num_habitaciones = Habitacion.query.filter_by(estado=EstadoHabitacion.ACTIVA).count()
    num_clientes = Cliente.query.count()
    num_reservas = Reserva.query.count()
    
    print(f"Hoteles destacados encontrados: {len(hoteles_destacados)}")
    print(f"Total hoteles activos: {num_hoteles}")
    print(f"Total habitaciones activas: {num_habitaciones}")
    print(f"Total clientes: {num_clientes}")
    print(f"Total reservas: {num_reservas}\n")
    
    if hoteles_destacados:
        print("=== HOTELES DESTACADOS ===")
        for i, hotel in enumerate(hoteles_destacados, 1):
            print(f"{i}. {hotel.nombre}")
            print(f"   Ubicación: {hotel.ubicacion_geografica}")
            print(f"   Estado: {hotel.estado}")
            print(f"   Descripción: {hotel.descripcion_servicios[:50] if hotel.descripcion_servicios else 'Sin descripción'}...")
            print(f"   Num habitaciones: {len(hotel.habitaciones)}")
            print()
    else:
        print("❌ No se encontraron hoteles destacados")
    
    # Obtener ciudades
    ciudades = [h.ubicacion_geografica for h in Hotel.query.filter_by(estado=EstadoHotel.ACTIVO).distinct(Hotel.ubicacion_geografica).all()]
    print(f"=== CIUDADES DISPONIBLES ({len(ciudades)}) ===")
    for ciudad in ciudades:
        print(f"- {ciudad}")
    
    # Verificar hoteles por ciudad
    hoteles_por_ciudad = {}
    for ciudad in ciudades[:3]:  # Solo las primeras 3 para no llenar la salida
        hoteles = Hotel.query.filter_by(estado=EstadoHotel.ACTIVO, ubicacion_geografica=ciudad).all()
        hoteles_por_ciudad[ciudad] = len(hoteles)
        print(f"\n=== HOTELES EN {ciudad.upper()} ===")
        for hotel in hoteles[:3]:  # Solo los primeros 3
            print(f"- {hotel.nombre}")