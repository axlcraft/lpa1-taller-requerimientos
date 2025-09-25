# Script para eliminar hoteles duplicados por nombre y ciudad
from app import create_app
from app.extensions import db
from app.models.hotel import Hotel

app = create_app()

with app.app_context():
    hotels = Hotel.query.all()
    seen = set()
    removed = 0
    for hotel in hotels:
        key = (hotel.nombre, hotel.ubicacion_geografica)
        if key in seen:
            db.session.delete(hotel)
            removed += 1
        else:
            seen.add(key)
    db.session.commit()
    print(f"Hoteles duplicados eliminados: {removed}")
