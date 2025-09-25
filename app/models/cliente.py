# app/models/cliente.py
from app.extensions import db
from .base import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash

class Cliente(BaseModel):
    @property
    def descuento_reservas(self):
        cantidad = len(self.reservas)
        if cantidad >= 8:
            return 0.50
        elif cantidad >= 5:
            return 0.25
        elif cantidad >= 3:
            return 0.17
        else:
            return 0.0

    """
    Representa un cliente/usuario registrado.
    Atributos: nombre_completo, telefono, correo, direccion, username y password_hash.
    Relaciones: reservas, comentarios, calificaciones.
    """
    __tablename__ = "clientes"

    nombre_completo = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(50))
    correo = db.Column(db.String(200), unique=True)
    direccion = db.Column(db.String(300))

    # Credenciales de acceso para clientes
    username = db.Column(db.String(80), unique=True, nullable=True)
    password_hash = db.Column(db.String(200), nullable=True)
    # Flag para determinar si el cliente es administrador (superusuario)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    reservas = db.relationship("Reserva", back_populates="cliente", cascade="all, delete-orphan")
    comentarios = db.relationship("Comentario", back_populates="cliente", cascade="all, delete-orphan")
    calificaciones = db.relationship("Calificacion", back_populates="cliente", cascade="all, delete-orphan")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Cliente {self.nombre_completo} ({self.id})>"
