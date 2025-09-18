# app/models/reserva.py
from app.extensions import db
from .base import BaseModel
from .enums import EstadoReserva
from datetime import datetime

class Reserva(BaseModel):
    """
    Reserva hecha por un cliente sobre una habitación.
    Atributos: fecha_inicio, fecha_fin, estado, total, fecha_reserva, cantidad_personas.
    Relaciones: cliente, habitacion, transaccion_pago, politica_cancelacion.
    """
    __tablename__ = "reservas"

    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    estado = db.Column(db.Enum(EstadoReserva), default=EstadoReserva.PENDIENTE, nullable=False)
    total = db.Column(db.Numeric(12,2), nullable=False, default=0)
    fecha_reserva = db.Column(db.DateTime, default=datetime.utcnow)
    cantidad_personas = db.Column(db.Integer, nullable=False, default=1)

    cliente_id = db.Column(db.String(36), db.ForeignKey("clientes.id"), nullable=False)
    cliente = db.relationship("Cliente", back_populates="reservas")

    habitacion_id = db.Column(db.String(36), db.ForeignKey("habitaciones.id"), nullable=False)
    habitacion = db.relationship("Habitacion", back_populates="reservas")

    transaccion_pago = db.relationship("TransaccionPago", back_populates="reserva", uselist=False)
    politica_cancelacion_id = db.Column(db.String(36), db.ForeignKey("politicas_cancelacion.id"))
    politica_cancelacion = db.relationship("PoliticaCancelacion", back_populates="reservas")

    def __repr__(self):
        return f"<Reserva {self.id} cliente={self.cliente_id} habitacion={self.habitacion_id}>"
