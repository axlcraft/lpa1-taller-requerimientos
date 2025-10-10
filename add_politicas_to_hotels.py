#!/usr/bin/env python
# add_politicas_to_hotels.py
import sys
import random
sys.path.append('/home/axl/HOTELSI/lpa1-taller-requerimientos')

from app import create_app
from app.models import Hotel, PoliticaPago, PoliticaCancelacion
from app.models.enums import TipoPago
from app.extensions import db
from decimal import Decimal

# Definir diferentes tipos de políticas para variar entre hoteles
POLITICAS_PAGO_TEMPLATES = [
    {
        "tipos": [TipoPago.TARJETA, TipoPago.TRANSFERENCIA],
        "descripciones": {
            TipoPago.TARJETA: "Aceptamos todas las tarjetas de crédito principales (Visa, MasterCard, American Express). Pago seguro con encriptación SSL.",
            TipoPago.TRANSFERENCIA: "Transferencia bancaria nacional e internacional. Proporcione el comprobante de pago para confirmación."
        }
    },
    {
        "tipos": [TipoPago.TARJETA, TipoPago.TRANSFERENCIA, TipoPago.EFECTIVO],
        "descripciones": {
            TipoPago.TARJETA: "Tarjetas de débito y crédito aceptadas. Procesamiento instantáneo.",
            TipoPago.TRANSFERENCIA: "Transferencias bancarias con confirmación en 24-48 horas.",
            TipoPago.EFECTIVO: "Pago en efectivo disponible solo al momento del check-in en el hotel."
        }
    },
    {
        "tipos": [TipoPago.TARJETA, TipoPago.OTRO],
        "descripciones": {
            TipoPago.TARJETA: "Tarjetas internacionales aceptadas. Soporte para Apple Pay y Google Pay.",
            TipoPago.OTRO: "PayPal, criptomonedas y otros métodos de pago digital disponibles previa consulta."
        }
    },
    {
        "tipos": [TipoPago.TARJETA],
        "descripciones": {
            TipoPago.TARJETA: "Exclusivamente tarjetas de crédito premium. Amex Centurion, Visa Infinite y MasterCard World Elite."
        }
    }
]

POLITICAS_CANCELACION_TEMPLATES = [
    {
        "nombre": "Política Estándar",
        "descripcion": "Cancelación gratuita hasta 48 horas antes del check-in. Después de este período se cobrará una noche de penalidad.",
        "penalidad": Decimal("0.00"),
        "dias_anticipacion": 2
    },
    {
        "nombre": "Política Flexible",
        "descripcion": "Cancelación gratuita hasta 24 horas antes. Ideal para huéspedes que requieren flexibilidad en sus planes de viaje.",
        "penalidad": Decimal("0.00"),
        "dias_anticipacion": 1
    },
    {
        "nombre": "Política Estricta",
        "descripcion": "Cancelación gratuita hasta 7 días antes del check-in. Después de este período se cobrará el 50% del valor total de la reserva.",
        "penalidad": Decimal("50.00"),  # Interpretado como porcentaje
        "dias_anticipacion": 7
    },
    {
        "nombre": "Política Premium",
        "descripcion": "Cancelación gratuita hasta 72 horas antes. Para estancias de lujo con servicios especializados que requieren preparación anticipada.",
        "penalidad": Decimal("25.00"),
        "dias_anticipacion": 3
    },
    {
        "nombre": "No Reembolsable",
        "descripcion": "Tarifa no reembolsable. No se permiten cancelaciones una vez confirmada la reserva. Precio especial para huéspedes seguros de su viaje.",
        "penalidad": Decimal("100.00"),
        "dias_anticipacion": 0
    },
    {
        "nombre": "Política Súper Flexible",
        "descripcion": "Cancelación gratuita hasta el mismo día del check-in (hasta las 14:00). Perfecta para viajeros de negocios con itinerarios cambiantes.",
        "penalidad": Decimal("0.00"),
        "dias_anticipacion": 0
    }
]

def create_politicas_for_hotels():
    """Crear políticas de pago y cancelación para todos los hoteles."""
    app = create_app()
    
    with app.app_context():
        hoteles = Hotel.query.all()
        print(f"📊 Creando políticas para {len(hoteles)} hoteles...")
        
        for i, hotel in enumerate(hoteles):
            print(f"\n🏨 {hotel.nombre}")
            
            # Seleccionar una plantilla de políticas de pago aleatoria
            pago_template = random.choice(POLITICAS_PAGO_TEMPLATES)
            
            # Crear políticas de pago para este hotel
            for tipo in pago_template["tipos"]:
                politica_pago = PoliticaPago(
                    tipo=tipo,
                    descripcion=pago_template["descripciones"][tipo],
                    hotel_id=hotel.id
                )
                db.session.add(politica_pago)
                print(f"  💳 Política de pago: {tipo.value}")
            
            # Seleccionar 1-3 políticas de cancelación aleatorias para variar
            num_politicas_cancel = random.randint(1, 3)
            politicas_seleccionadas = random.sample(POLITICAS_CANCELACION_TEMPLATES, num_politicas_cancel)
            
            for politica_template in politicas_seleccionadas:
                politica_cancelacion = PoliticaCancelacion(
                    nombre=politica_template["nombre"],
                    descripcion=politica_template["descripcion"],
                    penalidad=politica_template["penalidad"],
                    dias_anticipacion_reembolso=politica_template["dias_anticipacion"],
                    hotel_id=hotel.id
                )
                db.session.add(politica_cancelacion)
                print(f"  📋 Política de cancelación: {politica_template['nombre']}")
        
        # Guardar todos los cambios
        try:
            db.session.commit()
            print(f"\n✅ Políticas creadas exitosamente para todos los hoteles!")
            
            # Mostrar estadísticas finales
            total_pago = PoliticaPago.query.count()
            total_cancelacion = PoliticaCancelacion.query.count()
            print(f"📈 Estadísticas:")
            print(f"  - Políticas de pago creadas: {total_pago}")
            print(f"  - Políticas de cancelación creadas: {total_cancelacion}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error al crear políticas: {e}")
            return False
    
    return True

if __name__ == "__main__":
    success = create_politicas_for_hotels()
    if success:
        print("\n🎉 ¡Proceso completado exitosamente!")
    else:
        print("\n💥 Proceso falló. Revise los errores arriba.")