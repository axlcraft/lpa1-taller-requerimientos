# init_db.py
"""
Script para inicializar la base de datos del sistema de reservas hoteleras.
Crea todas las tablas según los modelos definidos y opcionalmente carga datos de ejemplo.
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.extensions import db
from app.models import *  # Importar todos los modelos
from datetime import datetime, timedelta
import uuid

def init_database(with_sample_data=False):
    """
    Inicializa la base de datos creando todas las tablas.
    
    Args:
        with_sample_data (bool): Si True, carga datos de ejemplo
    """
    app = create_app()
    
    with app.app_context():
        try:
            print("🗄️  Creando base de datos...")
            
            # Asegurar que el directorio instance existe
            os.makedirs('instance', exist_ok=True)
            
            # Crear todas las tablas
            db.create_all()
            print("✅ Tablas creadas exitosamente")
            
            if with_sample_data:
                print("📝 Cargando datos de ejemplo...")
                load_sample_data()
                print("✅ Datos de ejemplo cargados")
            
            print("🎉 Base de datos inicializada correctamente")
            
        except Exception as e:
            print(f"❌ Error al crear tablas: {e}")
            raise

def load_sample_data():
    """Carga datos de ejemplo en la base de datos."""
    from app.models.hotel import Hotel
    from app.models.habitacion import Habitacion
    from app.models.cliente import Cliente
    from app.models.enums import TipoHabitacion, EstadoHotel, EstadoHabitacion
    
    # Crear hoteles de ejemplo
    hoteles = [
        Hotel(
            nombre="Hotel Paradise",
            descripcion_servicios="Lujoso resort con vista al mar, piscina, spa, restaurante gourmet",
            direccion="Av. Costera 123, Cancún",
            telefono="+52-998-123-4567",
            correo="info@hotelparadise.com",
            ubicacion_geografica="Cancún, México",
            estado=EstadoHotel.ACTIVO
        ),
        Hotel(
            nombre="Mountain View Resort",
            descripcion_servicios="Hotel boutique en las montañas, vistas panorámicas, senderismo",
            direccion="Calle Alta Vista 456, Bariloche",
            telefono="+54-294-987-6543",
            correo="reservas@mountainview.com",
            ubicacion_geografica="Bariloche, Argentina",
            estado=EstadoHotel.ACTIVO
        ),
        Hotel(
            nombre="City Business Hotel",
            descripcion_servicios="Hotel ejecutivo en el centro de la ciudad, centro de negocios, WiFi",
            direccion="Av. Empresarial 789, Ciudad",
            telefono="+1-555-0123",
            correo="contact@citybusiness.com",
            ubicacion_geografica="Centro de la Ciudad",
            estado=EstadoHotel.ACTIVO
        )
    ]
    
    for hotel in hoteles:
        db.session.add(hotel)
    
    db.session.commit()
    
    # Crear habitaciones para cada hotel
    tipos_habitaciones = [TipoHabitacion.SIMPLE, TipoHabitacion.DOBLE, TipoHabitacion.SUITE]
    precios = [150.00, 250.00, 450.00]
    capacidades = [1, 2, 4]
    
    for hotel in hoteles:
        for i, tipo in enumerate(tipos_habitaciones):
            for num_hab in range(1, 6):  # 5 habitaciones de cada tipo por hotel
                habitacion = Habitacion(
                    tipo=tipo,
                    precio_base=precios[i],
                    capacidad=capacidades[i],
                    descripcion=f"Habitación {tipo.value} con todas las comodidades. Número {i+1}0{num_hab}",
                    estado=EstadoHabitacion.ACTIVA,
                    hotel_id=hotel.id
                )
                db.session.add(habitacion)
    
    # Crear clientes de ejemplo
    clientes = [
        Cliente(
            nombre_completo="Juan Pérez",
            correo="juan.perez@email.com",
            telefono="+1-555-1234",
            direccion="Calle Principal 123"
        ),
        Cliente(
            nombre_completo="María García",
            correo="maria.garcia@email.com",
            telefono="+1-555-5678",
            direccion="Av. Central 456"
        ),
        Cliente(
            nombre_completo="Carlos López",
            correo="carlos.lopez@email.com",
            telefono="+1-555-9012",
            direccion="Plaza Mayor 789"
        )
    ]
    
    for cliente in clientes:
        db.session.add(cliente)
    
    db.session.commit()
    print(f"✅ Creados {len(hoteles)} hoteles, {len(hoteles) * 15} habitaciones y {len(clientes)} clientes")

def drop_all_tables():
    """Elimina todas las tablas de la base de datos."""
    app = create_app()
    
    with app.app_context():
        print("⚠️  Eliminando todas las tablas...")
        db.drop_all()
        print("✅ Tablas eliminadas")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Inicializar base de datos del sistema de reservas")
    parser.add_argument("--with-sample-data", action="store_true", 
                       help="Cargar datos de ejemplo")
    parser.add_argument("--drop", action="store_true",
                       help="Eliminar todas las tablas antes de crearlas")
    
    args = parser.parse_args()
    
    if args.drop:
        drop_all_tables()
    
    init_database(with_sample_data=args.with_sample_data)