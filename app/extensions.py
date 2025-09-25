# app/extensions.py
from flask_sqlalchemy import SQLAlchemy

# Crear la extensión SQLAlchemy indicando que no expire objetos al hacer commit.
# Esto evita DetachedInstanceError en tests que utilizan objetos fuera de la sesión.
db = SQLAlchemy(session_options={"expire_on_commit": False})
