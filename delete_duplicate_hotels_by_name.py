# Script para eliminar hoteles duplicados por nombre
from app import create_app
from app.extensions import db
from app.models.hotel import Hotel

app = create_app()

with app.app_context():
    hotels = Hotel.query.all()
    seen_names = set()
    removed = 0
    for hotel in hotels:
        if hotel.nombre in seen_names:
            db.session.delete(hotel)
            removed += 1
        else:
            seen_names.add(hotel.nombre)
    db.session.commit()
    print(f"Hoteles con nombre duplicado eliminados: {removed}")
