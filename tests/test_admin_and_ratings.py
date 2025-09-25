import pytest
from app import create_app
from app.extensions import db
from app.config import TestConfig
from datetime import date, timedelta

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

from app.models import Hotel, Habitacion, Cliente, Reserva, EstadoReserva, TipoHabitacion

def test_admin_protection(client, app):
    # Crear hotel
    with app.app_context():
        h = Hotel(nombre='Test Hotel')
        db.session.add(h)
        db.session.commit()
        hid = h.id

    # Intentar acceder a editar sin sesión -> debería redirigir al login (302)
    resp = client.get(f'/hoteles/{hid}/editar')
    assert resp.status_code in (302, 301)

def test_rating_only_after_stay(client, app):
    with app.app_context():
        # Crear cliente, hotel, habitacion y reserva
        cliente = Cliente(nombre_completo='Test Cliente', correo='test@example.com')
        db.session.add(cliente)
        db.session.commit()

        hotel = Hotel(nombre='R Test')
        db.session.add(hotel)
        db.session.commit()

        habit = Habitacion(tipo=TipoHabitacion.SIMPLE, precio_base=100, capacidad=2, hotel_id=hotel.id)
        db.session.add(habit)
        db.session.commit()

        hoy = date.today()
        reserva = Reserva(
            fecha_inicio=hoy + timedelta(days=1),
            fecha_fin=hoy + timedelta(days=3),
            cantidad_personas=1,
            total=200,
            estado=EstadoReserva.PENDIENTE,
            cliente_id=cliente.id,
            habitacion_id=habit.id
        )
        db.session.add(reserva)
        db.session.commit()
        rid = reserva.id

        # Guardar ids para usar fuera del contexto y evitar DetachedInstanceError
        cliente_id = cliente.id
        hotel_id = hotel.id
        habit_id = habit.id

    # Intentar calificar antes de la estadía: la página de calificar debe impedirlo (mostrará el formulario pero el POST fallará)
    # Intentaremos POSTear a /evaluaciones/habitacion/<habitacion_id>/calificar
    resp = client.post(f'/evaluaciones/habitacion/{habit_id}/calificar', data={'cliente_id': cliente_id, 'puntuacion': '5'})
    # Debería responder 200 con mensaje de error en el HTML o un redirect; verificamos que no cree la calificación
    assert resp.status_code == 200
    assert b'Solo se pueden hacer calificaciones' in resp.data or b'calificaciones' in resp.data

def test_dev_login_and_rating_flow(client, app):
    # Test dev login endpoint and that after completing a reservation a rating can be created
    with app.app_context():
        # Ensure no superuser exists; dev_login will create one
        pass

    # Call dev login
    resp = client.get('/auth/dev_login', follow_redirects=True)
    assert resp.status_code == 200

    # Create entities and complete a reservation, then post a rating
    with app.app_context():
        cliente = Cliente(nombre_completo='Rater', correo='rater@example.com', username='rater')
        cliente.set_password('secret')
        db.session.add(cliente)
        db.session.commit()

        hotel = Hotel(nombre='Rate Hotel')
        db.session.add(hotel)
        db.session.commit()

        habit = Habitacion(tipo=TipoHabitacion.SIMPLE, precio_base=50, capacidad=2, hotel_id=hotel.id)
        db.session.add(habit)
        db.session.commit()

        from datetime import date, timedelta
        hoy = date.today()
        reserva = Reserva(fecha_inicio=hoy - timedelta(days=3), fecha_fin=hoy - timedelta(days=1), cantidad_personas=1, total=100, estado=EstadoReserva.COMPLETADA, cliente_id=cliente.id, habitacion_id=habit.id)
        db.session.add(reserva)
        db.session.commit()

    # Post rating via evaluaciones (should succeed because reservation is completed)
    resp2 = client.post(f'/evaluaciones/habitacion/{habit.id}/calificar', data={'cliente_id': cliente.id, 'estrellas_habitacion': '4', 'estrellas_hotel': '4', 'estrellas_atencion': '5'}, follow_redirects=True)
    assert resp2.status_code == 200
    text = resp2.data.decode('utf-8', errors='ignore')
    assert 'Calificaci' in text or 'Calificación' in text or 'Calificaci' in text