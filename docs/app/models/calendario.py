# app/models/calendario.py
from ..extensions import db
from .base import BaseModel
from .enums import EstadoCalendario
from datetime import date

class Calendario(BaseModel):
    """
    Calendario por habitación.
    Representa un día particular, su estado (ocupado/disponible/bloqueado), etc.
    """
    __tablename__ = "calendarios"

    fecha = db.Column(db.Date, nullable=False)
    estado = db.Column(db.Enum(EstadoCalendario), default=EstadoCalendario.DISPONIBLE, nullable=False)

    habitacion_id = db.Column(db.String(36), db.ForeignKey("habitaciones.id"), nullable=False)
    habitacion = db.relationship("Habitacion", back_populates="calendarios")

    def __repr__(self):
        return f"<Calendario {self.fecha} estado={self.estado}>"
