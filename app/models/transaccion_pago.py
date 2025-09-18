# app/models/transaccion_pago.py
from app.extensions import db
from .base import BaseModel
from .enums import TipoPago, EstadoPago
from datetime import datetime

class TransaccionPago(BaseModel):
    """
    Representa una transacción de pago relacionada a una reserva.
    Atributos: tipo, monto, fecha_pago, estado.
    """
    __tablename__ = "transacciones_pago"

    tipo = db.Column(db.Enum(TipoPago), nullable=False)
    monto = db.Column(db.Numeric(12,2), nullable=False, default=0)
    fecha_pago = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.Enum(EstadoPago), nullable=False, default=EstadoPago.PENDIENTE)

    reserva_id = db.Column(db.String(36), db.ForeignKey("reservas.id"))
    reserva = db.relationship("Reserva", back_populates="transaccion_pago")

    def __repr__(self):
        return f"<TransaccionPago {self.tipo} {self.monto} ({self.id})>"
