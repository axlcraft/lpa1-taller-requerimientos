#!/usr/bin/env python3
"""
Script simple para poblar la base de datos con hoteles y habitaciones
"""
import os
import sys

# Agregar el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models.hotel import Hotel
from app.models.habitacion import Habitacion
from app.models.enums import EstadoHotel, TipoHabitacion, EstadoHabitacion

def populate_data():
    app = create_app()
    
    with app.app_context():
        print("🏨 Poblando base de datos con hoteles y habitaciones...")
        
        # Datos de hoteles
        hoteles_data = [
            {
                "nombre": "Hotel Luxury Madrid",
                "direccion": "Gran Vía 123, Madrid, España",
                "telefono": "+34-91-555-0123",
                "correo": "info@luxurymadrid.com",
                "ubicacion_geografica": "Madrid, España",
                "descripcion_servicios": "Hotel de 5 estrellas en el corazón de Madrid con spa, restaurante gourmet y vistas panorámicas de la ciudad.",
            },
            {
                "nombre": "Beach Resort Cancún",
                "direccion": "Zona Hotelera Km 14.5, Cancún, México",
                "telefono": "+52-998-555-0456",
                "correo": "reservas@beachcancun.com",
                "ubicacion_geografica": "Cancún, México",
                "descripcion_servicios": "Resort todo incluido frente al mar Caribe con múltiples restaurantes, piscinas y actividades acuáticas.",
            },
            {
                "nombre": "City Plaza Hotel",
                "direccion": "Times Square 456, New York, USA",
                "telefono": "+1-212-555-0789",
                "correo": "contact@cityplazany.com",
                "ubicacion_geografica": "New York, USA",
                "descripcion_servicios": "Hotel boutique en Times Square con habitaciones modernas, gimnasio y bar en la azotea.",
            },
            {
                "nombre": "Mountain View Resort",
                "direccion": "Av. Libertador 789, Bariloche, Argentina",
                "telefono": "+54-294-555-0321",
                "correo": "info@mountainviewbariloche.com",
                "ubicacion_geografica": "Bariloche, Argentina",
                "descripcion_servicios": "Resort con vistas panorámicas a los lagos y montañas, spa, y actividades de aventura.",
            }
        ]
        
        for hotel_data in hoteles_data:
            # Verificar si el hotel ya existe
            existing_hotel = Hotel.query.filter_by(nombre=hotel_data["nombre"]).first()
            if existing_hotel:
                print(f"⚠️  Hotel '{hotel_data['nombre']}' ya existe, saltando...")
                continue
                
            hotel = Hotel(
                nombre=hotel_data["nombre"],
                direccion=hotel_data["direccion"],
                telefono=hotel_data["telefono"],
                correo=hotel_data["correo"],
                ubicacion_geografica=hotel_data["ubicacion_geografica"],
                descripcion_servicios=hotel_data["descripcion_servicios"],
                estado=EstadoHotel.ACTIVO
            )
            
            db.session.add(hotel)
            db.session.flush()  # Para obtener el ID del hotel
            
            print(f"✅ Creado hotel: {hotel.nombre}")
            
            # Crear habitaciones para cada hotel
            habitaciones_data = [
                {
                    "tipo": TipoHabitacion.SILVER,
                    "descripcion": f"Habitación Silver - Cómoda y elegante en {hotel.nombre}",
                    "precio_base": 120,
                    "capacidad": 2
                },
                {
                    "tipo": TipoHabitacion.GOLD,
                    "descripcion": f"Habitación Gold - Lujo y comodidad en {hotel.nombre}",
                    "precio_base": 180,
                    "capacidad": 2
                },
                {
                    "tipo": TipoHabitacion.PLATINUM,
                    "descripcion": f"Suite Platinum - Máximo lujo en {hotel.nombre}",
                    "precio_base": 250,
                    "capacidad": 4
                }
            ]
            
            for hab_data in habitaciones_data:
                habitacion = Habitacion(
                    tipo=hab_data["tipo"],
                    descripcion=hab_data["descripcion"],
                    precio_base=hab_data["precio_base"],
                    capacidad=hab_data["capacidad"],
                    estado=EstadoHabitacion.ACTIVA,
                    hotel_id=hotel.id
                )
                db.session.add(habitacion)
            
            print(f"  📋 Creadas 3 habitaciones para {hotel.nombre}")
        
        # Confirmar cambios
        db.session.commit()
        
        # Mostrar estadísticas
        total_hoteles = Hotel.query.count()
        total_habitaciones = Habitacion.query.count()
        
        print(f"\n🎉 ¡Población completada!")
        print(f"📊 Total hoteles en DB: {total_hoteles}")
        print(f"📊 Total habitaciones en DB: {total_habitaciones}")

if __name__ == "__main__":
    populate_data()