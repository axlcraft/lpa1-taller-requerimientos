# app/models/temporada.py
from app.extensions import db
from .base import BaseModel
from .enums import TipoTemporada
from datetime import date

class Temporada(BaseModel):
    """
    Temporadas (alta, baja, media) que afectan precios.
    Atributos: nombre, fecha_inicio, fecha_fin, tipo.
    """
    __tablename__ = "temporadas"

    nombre = db.Column(db.String(150), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    tipo = db.Column(db.Enum(TipoTemporada), default=TipoTemporada.MEDIA, nullable=False)

    hotel_id = db.Column(db.String(36), db.ForeignKey("hoteles.id"), nullable=False)
    hotel = db.relationship("Hotel", back_populates="temporadas")

    def __repr__(self):
        return f"<Temporada {self.nombre} {self.fecha_inicio} - {self.fecha_fin}>"
