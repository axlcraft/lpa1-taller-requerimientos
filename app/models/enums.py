# app/models/enums.py
from enum import Enum

class EstadoHotel(Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"

class EstadoHabitacion(Enum):
    ACTIVA = "activa"
    INACTIVA = "inactiva"

class EstadoReserva(Enum):
    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    COMPLETADA = "completada"

class EstadoPago(Enum):
    PENDIENTE = "pendiente"
    AUTORIZADO = "autorizado"
    RECHAZADO = "rechazado"
    REEMBOLSADO = "reembolsado"

class TipoPago(Enum):
    TARJETA = "tarjeta"
    TRANSFERENCIA = "transferencia"
    EFECTIVO = "efectivo"
    OTRO = "otro"

class TipoHabitacion(Enum):
    SIMPLE = "simple"
    DOBLE = "doble"
    SUITE = "suite"
    OTRO = "otro"

class TipoTemporada(Enum):
    ALTA = "alta"
    BAJA = "baja"
    MEDIA = "media"

class EstadoCalendario(Enum):
    OCUPADO = "ocupado"
    DISPONIBLE = "disponible"
    BLOQUEADO = "bloqueado"
