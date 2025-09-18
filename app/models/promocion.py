# app/models/promocion.py
from app.extensions import db
from .base import BaseModel
from datetime import date

class Promocion(BaseModel):
    """
    Promocion o oferta especial.
    Atributos: nombre, descripcion, descuento, serviciosAdicionales(list), fechaInicio, fechaFin.
    """
    __tablename__ = "promociones"

    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text)
    descuento = db.Column(db.Numeric(5,2), default=0)  # porcentaje o monto según convención
    servicios_adicionales = db.Column(db.Text)  # simple CSV o JSON según preferencia
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)

    hotel_id = db.Column(db.String(36), db.ForeignKey("hoteles.id"), nullable=False)
    hotel = db.relationship("Hotel", back_populates="promociones")

    def servicios_as_list(self):
        """Convierte el campo servicios_adicionales a lista si está en CSV."""
        if not self.servicios_adicionales:
            return []
        return [s.strip() for s in self.servicios_adicionales.split(",")]

    def __repr__(self):
        return f"<Promocion {self.nombre} ({self.id})>"
