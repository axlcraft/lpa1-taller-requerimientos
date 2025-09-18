# app/models/comentario.py
from app.extensions import db
from .base import BaseModel
from datetime import datetime

class Comentario(BaseModel):
    """
    Comentario dejado por un cliente sobre una habitación.
    Relacionado a Cliente y Habitacion.
    """
    __tablename__ = "comentarios"

    contenido = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    cliente_id = db.Column(db.String(36), db.ForeignKey("clientes.id"), nullable=False)
    cliente = db.relationship("Cliente", back_populates="comentarios")

    habitacion_id = db.Column(db.String(36), db.ForeignKey("habitaciones.id"), nullable=False)
    habitacion = db.relationship("Habitacion", back_populates="comentarios")

    def __repr__(self):
        return f"<Comentario {self.id} cliente={self.cliente_id} habitacion={self.habitacion_id}>"
