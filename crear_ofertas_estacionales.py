"""
Script para crear ofertas y temporadas estacionales automáticamente
"""
from app import create_app
from app.extensions import db
from app.models import Hotel, Temporada, Promocion
from app.models.enums import TipoTemporada, EstadoHotel
from datetime import date, datetime

def crear_temporadas_y_ofertas():
    """Crear temporadas estacionales y ofertas asociadas"""
    app = create_app()
    
    with app.app_context():
        hoteles = Hotel.query.filter_by(estado=EstadoHotel.ACTIVO).all()
        
        if not hoteles:
            print("❌ No hay hoteles activos para crear temporadas")
            return
        
        # Definir temporadas estacionales para 2025
        temporadas_2025 = [
            {
                'nombre': 'Temporada Navideña 2024-2025',
                'fecha_inicio': date(2024, 12, 15),
                'fecha_fin': date(2025, 1, 15),
                'tipo': TipoTemporada.ALTA,
                'promocion': {
                    'nombre': 'Especial Año Nuevo - Reserva Anticipada',
                    'descripcion': 'Descuento especial por reservar con anticipación para las fiestas navideñas',
                    'descuento_porcentaje': 15,
                    'fecha_inicio': date(2024, 11, 1),
                    'fecha_fin': date(2024, 12, 20)
                }
            },
            {
                'nombre': 'Verano Premium 2025',
                'fecha_inicio': date(2025, 6, 15),
                'fecha_fin': date(2025, 8, 31),
                'tipo': TipoTemporada.ALTA,
                'promocion': {
                    'nombre': 'Escapada de Verano - 3 Noches por 2',
                    'descripcion': 'Paga 2 noches y disfruta de 3 en nuestros mejores hoteles durante el verano',
                    'descuento_porcentaje': 25,
                    'fecha_inicio': date(2025, 5, 1),
                    'fecha_fin': date(2025, 7, 15)
                }
            },
            {
                'nombre': 'Primavera Romántica 2025',
                'fecha_inicio': date(2025, 3, 20),
                'fecha_fin': date(2025, 6, 14),
                'tipo': TipoTemporada.MEDIA,
                'promocion': {
                    'nombre': 'Romance de Primavera',
                    'descripcion': 'Oferta especial para parejas: cena romántica incluida y late check-out',
                    'descuento_porcentaje': 18,
                    'fecha_inicio': date(2025, 3, 1),
                    'fecha_fin': date(2025, 5, 31)
                }
            },
            {
                'nombre': 'Otoño Dorado 2025',
                'fecha_inicio': date(2025, 9, 21),
                'fecha_fin': date(2025, 12, 14),
                'tipo': TipoTemporada.MEDIA,
                'promocion': {
                    'nombre': 'Colores de Otoño - Estadía Extendida',
                    'descripcion': 'Disfruta del clima perfecto del otoño con descuentos en estadías largas',
                    'descuento_porcentaje': 20,
                    'fecha_inicio': date(2025, 9, 1),
                    'fecha_fin': date(2025, 11, 30)
                }
            },
            {
                'nombre': 'Invierno Tranquilo 2025',
                'fecha_inicio': date(2025, 1, 16),
                'fecha_fin': date(2025, 3, 19),
                'tipo': TipoTemporada.BAJA,
                'promocion': {
                    'nombre': 'Oferta de Invierno - Máximo Ahorro',
                    'descripcion': 'Aprovecha los mejores precios del año durante la temporada baja',
                    'descuento_porcentaje': 35,
                    'fecha_inicio': date(2025, 1, 15),
                    'fecha_fin': date(2025, 3, 15)
                }
            }
        ]
        
        contador_temporadas = 0
        contador_promociones = 0
        
        for hotel in hoteles:
            print(f"🏨 Configurando temporadas para: {hotel.nombre}")
            
            for temp_data in temporadas_2025:
                # Verificar si ya existe esta temporada para este hotel
                temporada_existente = Temporada.query.filter_by(
                    hotel_id=hotel.id,
                    nombre=temp_data['nombre']
                ).first()
                
                if not temporada_existente:
                    # Crear temporada
                    temporada = Temporada(
                        nombre=temp_data['nombre'],
                        fecha_inicio=temp_data['fecha_inicio'],
                        fecha_fin=temp_data['fecha_fin'],
                        tipo=temp_data['tipo'],
                        hotel_id=hotel.id
                    )
                    db.session.add(temporada)
                    contador_temporadas += 1
                    print(f"  ✅ Temporada creada: {temp_data['nombre']}")
                
                # Verificar si ya existe esta promoción para este hotel
                promocion_existente = Promocion.query.filter_by(
                    hotel_id=hotel.id,
                    nombre=temp_data['promocion']['nombre']
                ).first()
                
                if not promocion_existente:
                    # Crear promoción asociada
                    promocion = Promocion(
                        nombre=temp_data['promocion']['nombre'],
                        descripcion=temp_data['promocion']['descripcion'],
                        descuento=temp_data['promocion']['descuento_porcentaje'],
                        fecha_inicio=temp_data['promocion']['fecha_inicio'],
                        fecha_fin=temp_data['promocion']['fecha_fin'],
                        hotel_id=hotel.id
                    )
                    db.session.add(promocion)
                    contador_promociones += 1
                    print(f"  ✅ Promoción creada: {temp_data['promocion']['nombre']} ({temp_data['promocion']['descuento_porcentaje']}% descuento)")
        
        try:
            db.session.commit()
            print(f"\n🎉 ¡Configuración completada exitosamente!")
            print(f"📅 Temporadas creadas: {contador_temporadas}")
            print(f"🏷️  Promociones creadas: {contador_promociones}")
            print(f"🏨 Hoteles configurados: {len(hoteles)}")
            
            # Mostrar resumen de ofertas activas
            ofertas_activas = Promocion.query.filter(
                Promocion.fecha_fin >= date.today()
            ).count()
            print(f"✨ Ofertas actualmente disponibles: {ofertas_activas}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al guardar en la base de datos: {e}")

if __name__ == '__main__':
    crear_temporadas_y_ofertas()