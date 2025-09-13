# app/models/__init__.py
# Importa todos los modelos para que flask_sqlalchemy los registre.
from .base import BaseModel  # noqa: F401
from .enums import *  # noqa: F401,F403
from .hotel import Hotel  # noqa: F401
from .habitacion import Habitacion  # noqa: F401
from .cliente import Cliente  # noqa: F401
from .reserva import Reserva  # noqa: F401
from .transaccion_pago import TransaccionPago  # noqa: F401
from .politica_cancelacion import PoliticaDeCancelacion  # noqa: F401
from .politica_pago import PoliticaDePago  # noqa: F401
from .temporada import Temporada  # noqa: F401
from .promocion import Promocion  # noqa: F401
from .comentario import Comentario  # noqa: F401
from .calificacion import Calificacion  # noqa: F401
from .calendario import Calendario  # noqa: F401
from .foto import Foto  # noqa: F401
