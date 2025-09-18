# app/models/calificacion.py
from app.extensions import db
from .base import BaseModel
from datetime import datetime

class Calificacion(BaseModel):
    """
    Calificacion numérica (puntuacion) por cliente sobre una habitación.
    """
    __tablename__ = "calificaciones"

    puntuacion = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    cliente_id = db.Column(db.String(36), db.ForeignKey("clientes.id"), nullable=False)
    cliente = db.relationship("Cliente", back_populates="calificaciones")

    habitacion_id = db.Column(db.String(36), db.ForeignKey("habitaciones.id"), nullable=False)
    habitacion = db.relationship("Habitacion", back_populates="calificaciones")

    def __repr__(self):
        return f"<Calificacion {self.puntuacion} habitacion={self.habitacion_id}>"
