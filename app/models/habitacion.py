# app/models/habitacion.py
from app.extensions import db
from .base import BaseModel
from .enums import TipoHabitacion, EstadoHabitacion

class Habitacion(BaseModel):
    """
    Representa una habitación de un hotel.
    Atributos: tipo, descripcion, precio_base, capacidad, estado.
    Relaciones: reservas, calendario, comentarios, calificaciones, fotos, hotel.
    """
    __tablename__ = "habitaciones"

    tipo = db.Column(db.Enum(TipoHabitacion), nullable=False)
    descripcion = db.Column(db.Text)
    precio_base = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    capacidad = db.Column(db.Integer, nullable=False, default=1)
    estado = db.Column(db.Enum(EstadoHabitacion), default=EstadoHabitacion.ACTIVA, nullable=False)

    hotel_id = db.Column(db.String(36), db.ForeignKey("hoteles.id"), nullable=False)
    hotel = db.relationship("Hotel", back_populates="habitaciones")

    reservas = db.relationship("Reserva", back_populates="habitacion", cascade="all, delete-orphan")
    calendarios = db.relationship("Calendario", back_populates="habitacion", cascade="all, delete-orphan")
    comentarios = db.relationship("Comentario", back_populates="habitacion", cascade="all, delete-orphan")
    calificaciones = db.relationship("Calificacion", back_populates="habitacion", cascade="all, delete-orphan")
    fotos = db.relationship("Foto", back_populates="habitacion", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Habitacion {self.tipo} ({self.id}) - Hotel {self.hotel_id}>"
