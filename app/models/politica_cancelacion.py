# app/models/politica_cancelacion.py
from app.extensions import db
from .base import BaseModel

class PoliticaCancelacion(BaseModel):
    """
    Politica de cancelación aplicable a reservas.
    Atributos: nombre, descripcion, penalidad (monto o porcentaje), dias_anticipacion_reembolso.
    """
    __tablename__ = "politicas_cancelacion"

    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)
    penalidad = db.Column(db.Numeric(10,2), default=0)  # puede interpretarse como monto fijo
    dias_anticipacion_reembolso = db.Column(db.Integer, default=0)

    hotel_id = db.Column(db.String(36), db.ForeignKey("hoteles.id"), nullable=False)
    hotel = db.relationship("Hotel", back_populates="politicas_cancelacion")

    reservas = db.relationship("Reserva", back_populates="politica_cancelacion")

    def __repr__(self):
        return f"<PoliticaCancelacion {self.nombre} ({self.id})>"
