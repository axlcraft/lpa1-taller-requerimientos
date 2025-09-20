from app import create_app
from app.extensions import db
from app.models.hotel import Hotel
from app.models.habitacion import Habitacion
from app.models.enums import EstadoHotel, TipoHabitacion, EstadoHabitacion

# Datos de ciudades y precios
city_data = [
    {"destino": "Aruba", "pasajes": 418, "silver": 134, "gold": 167, "platinum": 191},
    {"destino": "Bahamas", "pasajes": 423, "silver": 112, "gold": 183, "platinum": 202},
    {"destino": "Cancún", "pasajes": 350, "silver": 105, "gold": 142, "platinum": 187},
    {"destino": "Hawaii", "pasajes": 858, "silver": 210, "gold": 247, "platinum": 291},
    {"destino": "Jamaica", "pasajes": 380, "silver": 115, "gold": 134, "platinum": 161},
    {"destino": "Madrid", "pasajes": 496, "silver": 190, "gold": 230, "platinum": 270},
    {"destino": "Miami", "pasajes": 334, "silver": 122, "gold": 151, "platinum": 183},
    {"destino": "Moscu", "pasajes": 634, "silver": 131, "gold": 153, "platinum": 167},
    {"destino": "NewYork", "pasajes": 495, "silver": 104, "gold": 112, "platinum": 210},
    {"destino": "Panamá", "pasajes": 315, "silver": 119, "gold": 138, "platinum": 175},
    {"destino": "Paris", "pasajes": 512, "silver": 210, "gold": 260, "platinum": 290},
    {"destino": "Rome", "pasajes": 478, "silver": 184, "gold": 220, "platinum": 250},
    {"destino": "Seul", "pasajes": 967, "silver": 205, "gold": 245, "platinum": 265},
    {"destino": "Sidney", "pasajes": 1045, "silver": 170, "gold": 199, "platinum": 230},
    {"destino": "Taipei", "pasajes": 912, "silver": 220, "gold": 245, "platinum": 298},
    {"destino": "Tokio", "pasajes": 989, "silver": 189, "gold": 231, "platinum": 255},
]

app = create_app()

with app.app_context():

    # Datos personalizados para hoteles por ciudad
    custom_hotels = {
        "Seul": [
            {"nombre": "Skyview Seoul", "direccion": "Avenida de la Estrella 17, Seul", "telefono": "+1-555-0101", "correo": "info1@skyviewseoul.com"},
            {"nombre": "Seul Luxe Retreat", "direccion": "Calle Han 25, Seul", "telefono": "+1-555-0102", "correo": "info2@seulluxeretreat.com"}
        ],
        "Madrid": [
            {"nombre": "Madrid Royal Suites", "direccion": "Plaza del Sol 12, Madrid", "telefono": "+1-555-0201", "correo": "info1@madridroyalsuites.com"},
            {"nombre": "Palacio de Madrid", "direccion": "Calle Gran Vía 45, Madrid", "telefono": "+1-555-0202", "correo": "info2@palaciodemadrid.com"}
        ],
        "Miami": [
            {"nombre": "Ocean Breeze Miami", "direccion": "Ocean Drive 33, Miami", "telefono": "+1-555-0301", "correo": "info1@oceanbreezemiami.com"},
            {"nombre": "Miami Sunset Hotel", "direccion": "Calle 21 del Mar 78, Miami", "telefono": "+1-555-0302", "correo": "info2@miamisunsethotel.com"}
        ],
        "Bahamas": [
            {"nombre": "Bahama Pearl Resort", "direccion": "Bahama Beach 19, Nassau, Bahamas", "telefono": "+1-555-0401", "correo": "info1@bahamapearlresort.com"},
            {"nombre": "Island Breeze Bahamas", "direccion": "Sunrise Avenue 22, Nassau, Bahamas", "telefono": "+1-555-0402", "correo": "info2@islandbreezebahamas.com"}
        ],
        "Hawaii": [
            {"nombre": "Aloha Breeze Resort", "direccion": "Waikiki Road 11, Honolulu, Hawaii", "telefono": "+1-555-0501", "correo": "info1@alohabreezeresort.com"},
            {"nombre": "Hawaii Sunset Villas", "direccion": "Sunset Bay 44, Honolulu, Hawaii", "telefono": "+1-555-0502", "correo": "info2@hawaiisunsetvillas.com"}
        ],
        "Jamaica": [
            {"nombre": "Jamaica Coral Retreat", "direccion": "Coral Reef Drive 9, Kingston, Jamaica", "telefono": "+1-555-0601", "correo": "info1@jamaicacoralretreat.com"},
            {"nombre": "Sunset Breeze Jamaica", "direccion": "Tropical Avenue 32, Montego Bay, Jamaica", "telefono": "+1-555-0602", "correo": "info2@sunsetbreezejamaica.com"}
        ],
        "Sidney": [
            {"nombre": "Harbourview Sidney", "direccion": "Circular Quay 18, Sidney", "telefono": "+1-555-0701", "correo": "info1@harbourviewsidney.com"},
            {"nombre": "Sidney Luxe Escape", "direccion": "Darling Harbour 9, Sidney", "telefono": "+1-555-0702", "correo": "info2@sidneyluxescape.com"}
        ],
        "Panamá": [
            {"nombre": "Panama Skyline Hotel", "direccion": "Avenida Balboa 55, Panamá", "telefono": "+1-555-0801", "correo": "info1@panamaskylinehotel.com"},
            {"nombre": "Cielo Azul Panamá", "direccion": "Calle 50 Este 12, Panamá", "telefono": "+1-555-0802", "correo": "info2@cieloazulpanama.com"}
        ],
        "Taipei": [
            {"nombre": "Taipei Grand Suites", "direccion": "Zhongxiao Road 13, Taipei", "telefono": "+1-555-0901", "correo": "info1@taipeigrandsuites.com"},
            {"nombre": "Taipei Horizon Hotel", "direccion": "Ren'ai Road 31, Taipei", "telefono": "+1-555-0902", "correo": "info2@taipeihorizonhotel.com"}
        ],
        "Tokio": [
            {"nombre": "Shibuya Heights Hotel", "direccion": "Shibuya Crossing 44, Tokio", "telefono": "+1-555-1001", "correo": "info1@shibuyaheightshotel.com"},
            {"nombre": "Tokyo Dream Suites", "direccion": "Akihabara Street 29, Tokio", "telefono": "+1-555-1002", "correo": "info2@tokyodreamsuites.com"}
        ],
        "NewYork": [
            {"nombre": "Empire City Suites", "direccion": "Broadway 55, New York", "telefono": "+1-555-1101", "correo": "info1@empirecitysuites.com"},
            {"nombre": "New York Skylight Hotel", "direccion": "5th Avenue 18, New York", "telefono": "+1-555-1102", "correo": "info2@newyorkskylighthotel.com"}
        ],
        "Moscu": [
            {"nombre": "Red Square Retreat", "direccion": "Tverskaya Street 28, Moscú", "telefono": "+1-555-1201", "correo": "info1@redsquareretreat.com"},
            {"nombre": "Moscow Elite Hotel", "direccion": "Arbat Street 14, Moscú", "telefono": "+1-555-1202", "correo": "info2@moscowelitehotel.com"}
        ],
        "Rome": [
            {"nombre": "Roma Heritage Hotel", "direccion": "Via del Corso 36, Roma", "telefono": "+1-555-1301", "correo": "info1@romaheritagehotel.com"},
            {"nombre": "Eternal Rome Suites", "direccion": "Piazza Navona 22, Roma", "telefono": "+1-555-1302", "correo": "info2@eternalromesuites.com"}
        ],
        "Aruba": [
            {"nombre": "Aruba Ocean Retreat", "direccion": "Palm Beach 14, Aruba", "telefono": "+1-555-1401", "correo": "info1@arubaoceanretreat.com"},
            {"nombre": "Caribbean Breeze Aruba", "direccion": "Eagle Beach 35, Aruba", "telefono": "+1-555-1402", "correo": "info2@caribbeanbreezearuba.com"}
        ],
        "Cancún": [
            {"nombre": "Cancún Paradise Suites", "direccion": "Boulevard Kukulcán 67, Cancún", "telefono": "+1-555-1501", "correo": "info1@cancunparadisesuites.com"},
            {"nombre": "Cancún Dream Resort", "direccion": "Avenida Tulum 22, Cancún", "telefono": "+1-555-1502", "correo": "info2@cancundreamresort.com"}
        ],
        "Paris": [
            {"nombre": "Parisian Elegance Hotel", "direccion": "Rue de Rivoli 19, París", "telefono": "+1-555-1601", "correo": "info1@parisianelegancehotel.com"},
            {"nombre": "Louvre Luxe Suites", "direccion": "Avenue des Champs-Élysées 42, París", "telefono": "+1-555-1602", "correo": "info2@louvreluxesuites.com"}
        ],
    }

    for city in city_data:
        destino = city["destino"]
        for i in range(2):
            if destino in custom_hotels:
                hotel_info = custom_hotels[destino][i]
                nombre = hotel_info["nombre"]
                direccion = hotel_info["direccion"]
                telefono = hotel_info["telefono"]
                correo = hotel_info["correo"]
            else:
                nombre = f"Hotel {destino} #{i+1}"
                direccion = f"Calle Principal {i+1}, {destino}"
                telefono = f"+1-555-{i+1:04d}"
                correo = f"info{i+1}@{destino.lower()}.com"

            hotel = Hotel(
                nombre=nombre,
                direccion=direccion,
                telefono=telefono,
                correo=correo,
                ubicacion_geografica=destino,
                descripcion_servicios=f"Hotel en {destino} con servicios premium.",
                estado=EstadoHotel.ACTIVO
            )
            db.session.add(hotel)
            db.session.flush()

            habitaciones = [
                Habitacion(
                    tipo=TipoHabitacion.SILVER,
                    descripcion="Habitación Silver",
                    precio_base=city['silver'],
                    capacidad=2,
                    estado=EstadoHabitacion.ACTIVA,
                    hotel_id=hotel.id
                ),
                Habitacion(
                    tipo=TipoHabitacion.GOLD,
                    descripcion="Habitación Gold",
                    precio_base=city['gold'],
                    capacidad=2,
                    estado=EstadoHabitacion.ACTIVA,
                    hotel_id=hotel.id
                ),
                Habitacion(
                    tipo=TipoHabitacion.PLATINUM,
                    descripcion="Habitación Platinum",
                    precio_base=city['platinum'],
                    capacidad=2,
                    estado=EstadoHabitacion.ACTIVA,
                    hotel_id=hotel.id
                ),
                Habitacion(
                    tipo=TipoHabitacion.SILVER,
                    descripcion="Habitación Silver Extra",
                    precio_base=city['silver'],
                    capacidad=2,
                    estado=EstadoHabitacion.ACTIVA,
                    hotel_id=hotel.id
                ),
            ]
            db.session.add_all(habitaciones)
    db.session.commit()
    print("✅ Hoteles y habitaciones insertados correctamente.")
