# app/models/politica_pago.py
from ..extensions import db
from .base import BaseModel
from .enums import TipoPago

class PoliticaDePago(BaseModel):
    """
    PoliticaDePago describe las formas válidas de pago del hotel.
    Atributos: tipo, descripcion.
    """
    __tablename__ = "politicas_pago"

    tipo = db.Column(db.Enum(TipoPago), nullable=False)
    descripcion = db.Column(db.Text)

    hotel_id = db.Column(db.String(36), db.ForeignKey("hoteles.id"), nullable=False)
    hotel = db.relationship("Hotel", back_populates="politicas_pago")

    def __repr__(self):
        return f"<PoliticaDePago {self.tipo} ({self.id})>"
