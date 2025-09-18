# app/models/cliente.py
from app.extensions import db
from .base import BaseModel

class Cliente(BaseModel):
    """
    Representa un cliente/usuario registrado.
    Atributos: nombre_completo, telefono, correo, direccion.
    Relaciones: reservas, comentarios, calificaciones.
    """
    __tablename__ = "clientes"

    nombre_completo = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(50))
    correo = db.Column(db.String(200), unique=True)
    direccion = db.Column(db.String(300))

    reservas = db.relationship("Reserva", back_populates="cliente", cascade="all, delete-orphan")
    comentarios = db.relationship("Comentario", back_populates="cliente", cascade="all, delete-orphan")
    calificaciones = db.relationship("Calificacion", back_populates="cliente", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Cliente {self.nombre_completo} ({self.id})>"
