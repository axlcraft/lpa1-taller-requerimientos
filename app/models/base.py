# app/models/base.py
import uuid
from datetime import datetime
from app.extensions import db

def generate_uuid():
    """Genera un UUID4 como string."""
    return str(uuid.uuid4())

class BaseModel(db.Model):
    """Modelo base con id UUID y timestamps."""
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def as_dict(self):
        """Devuelve un dict simple del modelo."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
