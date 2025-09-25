# Script para poblar la base de datos con solo dos hoteles únicos por ciudad, sin repetir ciudades
from app import create_app
from app.extensions import db
from app.models.hotel import Hotel
from app.models.habitacion import Habitacion
from app.models.enums import EstadoHotel, TipoHabitacion, EstadoHabitacion

city_data = [
    {"destino": "Aruba", "silver": 134, "gold": 167, "platinum": 191},
    {"destino": "Bahamas", "silver": 112, "gold": 183, "platinum": 202},
    {"destino": "Cancún", "silver": 105, "gold": 142, "platinum": 187},
    {"destino": "Hawaii", "silver": 210, "gold": 247, "platinum": 291},
    {"destino": "Jamaica", "silver": 115, "gold": 134, "platinum": 161},
    {"destino": "Madrid", "silver": 190, "gold": 230, "platinum": 270},
    {"destino": "Miami", "silver": 122, "gold": 151, "platinum": 183},
    {"destino": "Moscu", "silver": 131, "gold": 153, "platinum": 167},
    {"destino": "NewYork", "silver": 104, "gold": 112, "platinum": 210},
    {"destino": "Panamá", "silver": 119, "gold": 138, "platinum": 175},
    {"destino": "Paris", "silver": 210, "gold": 260, "platinum": 290},
    {"destino": "Rome", "silver": 184, "gold": 220, "platinum": 250},
    {"destino": "Seul", "silver": 205, "gold": 245, "platinum": 265},
    {"destino": "Sidney", "silver": 170, "gold": 199, "platinum": 230},
    {"destino": "Taipei", "silver": 220, "gold": 245, "platinum": 298},
    {"destino": "Tokio", "silver": 189, "gold": 231, "platinum": 255},
]

app = create_app()

with app.app_context():
    nombres_elegantes = [
        ["Aruba Royal Palace", "Aruba Ocean Jewel"],
        ["Bahamas Blue Diamond", "Bahamas Luxe Retreat"],
        ["Cancún Sun Majesty", "Cancún Dream Palace"],
        ["Hawaii Paradise Pearl", "Hawaii Golden Wave"],
        ["Jamaica Emerald Bay", "Jamaica Prestige Resort"],
        ["Madrid Imperial Suites", "Madrid Crystal Palace"],
        ["Miami Starlight Hotel", "Miami Velvet Crown"],
        ["Moscu Grand Sapphire", "Moscu Opulent Plaza"],
        ["NewYork Skyline Elite", "NewYork Platinum Tower"],
        ["Panamá Celestial Palace", "Panamá Royal Vista"],
        ["Paris Golden Elegance", "Paris Diamond Chateau"],
        ["Rome Eternal Luxe", "Rome Prestige Villa"],
        ["Seul Aurora Palace", "Seul Noble Retreat"],
        ["Sidney Harbour Jewel", "Sidney Luxe Escape"],
        ["Taipei Infinity Palace", "Taipei Emerald Suites"],
        ["Tokio Imperial Dream", "Tokio Shining Pearl"],
    ]
    descripciones_elegantes = [
        ["Un palacio de lujo frente al mar Caribe, con servicios exclusivos y vistas espectaculares.", "La joya de Aruba, donde el confort y la elegancia se unen en cada detalle."],
        ["El diamante azul de Bahamas, ideal para quienes buscan distinción y relax.", "Retiro de lujo con ambiente tropical y atención personalizada."],
        ["Majestuosidad y sol en el corazón de Cancún, con experiencias únicas.", "Palacio de sueños con diseño moderno y servicios premium."],
        ["Perla paradisíaca en Hawaii, rodeada de naturaleza y sofisticación.", "Ola dorada de confort y exclusividad en Honolulu."],
        ["Bahía esmeralda con ambiente selecto y gastronomía de autor.", "Resort de prestigio con instalaciones de primer nivel."],
        ["Suites imperiales en Madrid, con arquitectura clásica y lujo moderno.", "Palacio de cristal con vistas a la ciudad y atención de excelencia."],
        ["Hotel estelar en Miami, con diseño vanguardista y ambiente glamuroso.", "Corona de terciopelo con servicios de lujo y ubicación privilegiada."],
        ["Gran zafiro de Moscú, con espacios elegantes y ambiente internacional.", "Plaza opulenta con detalles artísticos y confort superior."],
        ["Elite del skyline neoyorquino, con vistas panorámicas y amenities exclusivos.", "Torre platinum con diseño sofisticado y atención personalizada."],
        ["Palacio celestial en Panamá, con lujo y serenidad en cada rincón.", "Vista real con instalaciones modernas y ambiente refinado."],
        ["Elegancia dorada en París, con gastronomía de autor y ambiente romántico.", "Chateau de diamante con historia y distinción."],
        ["Lujosa villa eterna en Roma, con arte y confort en cada espacio.", "Villa de prestigio con jardines privados y servicios premium."],
        ["Palacio aurora en Seúl, con tecnología y lujo en perfecta armonía.", "Retiro noble con diseño minimalista y atención exclusiva."],
        ["Joya del puerto de Sidney, con vistas al mar y ambiente cosmopolita.", "Escape de lujo con instalaciones de vanguardia."],
        ["Palacio infinito en Taipei, con espacios amplios y decoración elegante.", "Suites esmeralda con servicios personalizados y ambiente tranquilo."],
        ["Sueño imperial en Tokio, con cultura y lujo en cada detalle.", "Perla brillante con tecnología avanzada y confort total."],
    ]

    for idx, city in enumerate(city_data):
        destino = city["destino"]
        for i in range(2):
            nombre = nombres_elegantes[idx][i]
            direccion = f"Avenida {i+1} Principal, {destino}"
            telefono = f"+1-555-{str(idx+1).zfill(2)}{str(i+1).zfill(2)}"
            correo = f"elegance{i+1}@{destino.lower()}hotel.com"
            descripcion = descripciones_elegantes[idx][i]
            hotel = Hotel(
                nombre=nombre,
                direccion=direccion,
                telefono=telefono,
                correo=correo,
                ubicacion_geografica=destino,
                descripcion_servicios=descripcion,
                estado=EstadoHotel.ACTIVO
            )
            db.session.add(hotel)
            db.session.flush()
            habitaciones = [
                Habitacion(
                    tipo=TipoHabitacion.SILVER,
                    descripcion=f"Suite Silver: Modernidad y confort en {destino}.",
                    precio_base=city['silver'],
                    capacidad=2,
                    estado=EstadoHabitacion.ACTIVA,
                    hotel_id=hotel.id
                ),
                Habitacion(
                    tipo=TipoHabitacion.GOLD,
                    descripcion=f"Suite Gold: Elegancia y servicios premium en {destino}.",
                    precio_base=city['gold'],
                    capacidad=2,
                    estado=EstadoHabitacion.ACTIVA,
                    hotel_id=hotel.id
                ),
                Habitacion(
                    tipo=TipoHabitacion.PLATINUM,
                    descripcion=f"Suite Platinum: El máximo lujo en {destino}.",
                    precio_base=city['platinum'],
                    capacidad=2,
                    estado=EstadoHabitacion.ACTIVA,
                    hotel_id=hotel.id
                ),
            ]
            db.session.add_all(habitaciones)
    db.session.commit()
    print("✅ 2 hoteles únicos por ciudad insertados correctamente.")
