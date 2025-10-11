#!/usr/bin/env python3
"""
Script para limpiar promociones vencidas y crear nuevas promociones futuras
"""

from app import create_app
from app.models.promocion import Promocion
from app.models.hotel import Hotel
from app.extensions import db
from datetime import datetime, date, timedelta
import random

def main():
    app = create_app()
    
    with app.app_context():
        print("🧹 LIMPIEZA Y RENOVACIÓN DE PROMOCIONES")
        print("=" * 50)
        
        # 1. ELIMINAR PROMOCIONES VENCIDAS (más de 7 días)
        hoy = date.today()
        una_semana_atras = hoy - timedelta(days=7)
        
        promociones_vencidas = Promocion.query.filter(
            Promocion.fecha_fin < una_semana_atras
        ).all()
        
        print(f"📊 Encontradas {len(promociones_vencidas)} promociones vencidas (+7 días)")
        
        if promociones_vencidas:
            print("🗑️ Eliminando promociones vencidas...")
            for promo in promociones_vencidas:
                db.session.delete(promo)
            
            db.session.commit()
            print(f"✅ {len(promociones_vencidas)} promociones eliminadas")
        
        # 2. CREAR NUEVAS PROMOCIONES FUTURAS
        print("\n🎯 Creando nuevas promociones futuras...")
        
        # Obtener todos los hoteles
        hoteles = Hotel.query.all()
        
        if not hoteles:
            print("❌ No hay hoteles disponibles para crear promociones")
            return
        
        # Plantillas de promociones por temporada
        promociones_plantillas = [
            # Promociones de Navidad y Fin de Año
            {
                'nombre': 'Especial Navidad 2025 - Reserva Anticipada',
                'descripcion': 'Celebra las fiestas navideñas con nosotros. Incluye cena especial de Nochebuena y Año Nuevo.',
                'descuento': 25,
                'fecha_inicio': date(2025, 12, 15),
                'fecha_fin': date(2026, 1, 5)
            },
            {
                'nombre': 'Fin de Año VIP 2025',
                'descripcion': 'Paquete premium para recibir el 2026. Incluye champagne de bienvenida y vista a fuegos artificiales.',
                'descuento': 30,
                'fecha_inicio': date(2025, 12, 28),
                'fecha_fin': date(2026, 1, 2)
            },
            
            # Promociones de Verano 2026
            {
                'nombre': 'Escapada de Verano 2026 - 5 Noches por 4',
                'descripcion': 'Disfruta del verano con una noche gratis. Perfecto para vacaciones familiares.',
                'descuento': 20,
                'fecha_inicio': date(2026, 6, 1),
                'fecha_fin': date(2026, 8, 31)
            },
            {
                'nombre': 'Playa y Sol - Oferta Anticipada',
                'descripcion': 'Reserva tu verano con anticipación y ahorra. Incluye desayuno buffet y acceso a playa.',
                'descuento': 15,
                'fecha_inicio': date(2026, 5, 15),
                'fecha_fin': date(2026, 9, 15)
            },
            
            # Promociones de Primavera 2026
            {
                'nombre': 'Romance de Primavera 2026',
                'descripcion': 'Escapada romántica en primavera. Incluye cena a la luz de las velas y spa para parejas.',
                'descuento': 22,
                'fecha_inicio': date(2026, 3, 20),
                'fecha_fin': date(2026, 6, 20)
            },
            {
                'nombre': 'Semana Santa Familiar 2026',
                'descripcion': 'Vacaciones perfectas para toda la familia. Actividades para niños incluidas.',
                'descuento': 18,
                'fecha_inicio': date(2026, 3, 25),
                'fecha_fin': date(2026, 4, 15)
            },
            
            # Promociones de Otoño 2026
            {
                'nombre': 'Otoño Dorado 2026',
                'descripcion': 'Disfruta de la tranquilidad del otoño con precios especiales.',
                'descuento': 20,
                'fecha_inicio': date(2026, 9, 20),
                'fecha_fin': date(2026, 12, 20)
            },
            
            # Promociones de Invierno 2026
            {
                'nombre': 'Oferta de Invierno 2026 - Máximo Confort',
                'descripcion': 'Escapa del frío con nuestras tarifas especiales de invierno. Spa y wellness incluido.',
                'descuento': 25,
                'fecha_inicio': date(2025, 12, 1),
                'fecha_fin': date(2026, 3, 31)
            }
        ]
        
        # Crear promociones para una muestra representativa de hoteles
        hoteles_seleccionados = random.sample(hoteles, min(len(hoteles), 25))  # Máximo 25 hoteles
        promociones_creadas = 0
        
        for plantilla in promociones_plantillas:
            # Asignar cada promoción a 3-5 hoteles aleatorios
            hoteles_para_promo = random.sample(
                hoteles_seleccionados, 
                random.randint(3, min(5, len(hoteles_seleccionados)))
            )
            
            for hotel in hoteles_para_promo:
                # Verificar que no exista una promoción igual para este hotel
                promo_existente = Promocion.query.filter(
                    Promocion.nombre == plantilla['nombre'],
                    Promocion.hotel_id == hotel.id
                ).first()
                
                if not promo_existente:
                    nueva_promocion = Promocion(
                        nombre=plantilla['nombre'],
                        descripcion=plantilla['descripcion'],
                        descuento=plantilla['descuento'],
                        fecha_inicio=plantilla['fecha_inicio'],
                        fecha_fin=plantilla['fecha_fin'],
                        hotel=hotel
                    )
                    
                    db.session.add(nueva_promocion)
                    promociones_creadas += 1
        
        # Guardar todas las promociones nuevas
        db.session.commit()
        
        print(f"✅ {promociones_creadas} nuevas promociones futuras creadas")
        
        # 3. MOSTRAR RESUMEN FINAL
        print("\n📊 RESUMEN FINAL:")
        print("=" * 30)
        
        total_promociones = Promocion.query.count()
        vigentes = Promocion.query.filter(
            Promocion.fecha_inicio <= hoy,
            Promocion.fecha_fin >= hoy
        ).count()
        
        futuras = Promocion.query.filter(
            Promocion.fecha_inicio > hoy
        ).count()
        
        print(f"├── Total promociones: {total_promociones}")
        print(f"├── Promociones vigentes: {vigentes}")
        print(f"└── Promociones futuras: {futuras}")
        
        # Mostrar algunas promociones futuras como ejemplo
        print(f"\n🎯 PRÓXIMAS PROMOCIONES:")
        promociones_futuras = Promocion.query.filter(
            Promocion.fecha_inicio > hoy
        ).order_by(Promocion.fecha_inicio).limit(5).all()
        
        for i, promo in enumerate(promociones_futuras, 1):
            print(f"   {i}. {promo.nombre}")
            print(f"      📅 {promo.fecha_inicio} - {promo.fecha_fin}")
            print(f"      💰 {promo.descuento}% descuento")
            print(f"      🏨 {promo.hotel.nombre}")
            print()
        
        print("🎉 ¡Limpieza y renovación completada exitosamente!")

if __name__ == "__main__":
    main()