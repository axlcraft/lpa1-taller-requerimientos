# app/models/calificacion.py
from app.extensions import db
from .base import BaseModel
from datetime import datetime

class Calificacion(BaseModel):
    """
    Calificacion numérica (puntuacion) por cliente sobre una habitación.
    """
    __tablename__ = "calificaciones"

    estrellas_hotel = db.Column(db.Integer, nullable=False)
    estrellas_habitacion = db.Column(db.Integer, nullable=False)
    estrellas_atencion = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    cliente_id = db.Column(db.String(36), db.ForeignKey("clientes.id"), nullable=False)
    cliente = db.relationship("Cliente", back_populates="calificaciones")

    habitacion_id = db.Column(db.String(36), db.ForeignKey("habitaciones.id"), nullable=False)
    habitacion = db.relationship("Habitacion", back_populates="calificaciones")

    hotel_id = db.Column(db.String(36), db.ForeignKey("hoteles.id"), nullable=False)
    hotel = db.relationship("Hotel", back_populates="calificaciones")

    def __repr__(self):
        return f"<Calificacion hotel={self.estrellas_hotel} hab={self.estrellas_habitacion} atencion={self.estrellas_atencion}>"
