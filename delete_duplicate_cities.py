# Script para eliminar ciudades duplicadas por nombre
from app import create_app
from app.extensions import db
from app.models.hotel import Hotel

app = create_app()

with app.app_context():
    hotels = Hotel.query.all()
    seen_cities = set()
    removed = 0
    for hotel in hotels:
        city = hotel.ubicacion_geografica
        if city in seen_cities:
            db.session.delete(hotel)
            removed += 1
        else:
            seen_cities.add(city)
    db.session.commit()
    print(f"Ciudades duplicadas eliminadas: {removed}")
