# app/models/foto.py
from app.extensions import db
from .base import BaseModel

class Foto(BaseModel):
    """
    Foto asociada a hotel o habitación.
    - url: ubicación de la imagen.
    - descripcion: texto opcional.
    """
    __tablename__ = "fotos"

    url = db.Column(db.String(500), nullable=False)
    descripcion = db.Column(db.String(300))

    hotel_id = db.Column(db.String(36), db.ForeignKey("hoteles.id"), nullable=True)
    hotel = db.relationship("Hotel", back_populates="fotos")

    habitacion_id = db.Column(db.String(36), db.ForeignKey("habitaciones.id"), nullable=True)
    habitacion = db.relationship("Habitacion", back_populates="fotos")

    def __repr__(self):
        return f"<Foto {self.url} ({self.id})>"
