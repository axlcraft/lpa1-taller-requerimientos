# app/models/hotel.py
from app.extensions import db
from .base import BaseModel
from .enums import EstadoHotel

class Hotel(BaseModel):
    """
    Representa un hotel.
    - name, direccion, telefono, correo, ubicacionGeografica, descripcionServicios, estado.
    - Relación 1..* con Habitacion, Promocion, PoliticaDePago, PoliticaDeCancelacion, Temporada, Foto.
    """
    __tablename__ = "hoteles"

    nombre = db.Column(db.String(200), nullable=False)
    direccion = db.Column(db.String(300))
    telefono = db.Column(db.String(50))
    correo = db.Column(db.String(200))
    ubicacion_geografica = db.Column(db.String(200))
    descripcion_servicios = db.Column(db.Text)
    estado = db.Column(db.Enum(EstadoHotel), default=EstadoHotel.ACTIVO, nullable=False)

    # Relaciones
    habitaciones = db.relationship("Habitacion", back_populates="hotel", cascade="all, delete-orphan")
    promociones = db.relationship("Promocion", back_populates="hotel", cascade="all, delete-orphan")
    politicas_pago = db.relationship("PoliticaPago", back_populates="hotel", cascade="all, delete-orphan")
    politicas_cancelacion = db.relationship("PoliticaCancelacion", back_populates="hotel", cascade="all, delete-orphan")
    temporadas = db.relationship("Temporada", back_populates="hotel", cascade="all, delete-orphan")
    fotos = db.relationship("Foto", back_populates="hotel", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Hotel {self.nombre} ({self.id})>"
