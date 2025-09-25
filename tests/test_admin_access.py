import pytest
from app import create_app
from app.extensions import db


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


def test_create_pages_require_admin(client, app):
    # Ensure anonymous cannot access create pages
    resp_hotel = client.get('/hoteles/crear')
    resp_habit = client.get('/habitaciones/crear')

    assert resp_hotel.status_code in (301, 302)
    assert resp_habit.status_code in (301, 302)

    # Now simulate a logged-in non-admin client by setting cliente_id only
    with client.session_transaction() as sess:
        sess['cliente_id'] = 'fake-client-id'
        sess['is_superuser'] = False

    resp_hotel2 = client.get('/hoteles/crear')
    resp_habit2 = client.get('/habitaciones/crear')

    # Should still redirect to login because not superuser
    assert resp_hotel2.status_code in (301, 302)
    assert resp_habit2.status_code in (301, 302)

    # Now simulate an admin session
    with client.session_transaction() as sess:
        sess['is_superuser'] = True

    resp_hotel3 = client.get('/hoteles/crear')
    resp_habit3 = client.get('/habitaciones/crear')

    # Admin should be able to access the pages (200)
    assert resp_hotel3.status_code == 200
    assert resp_habit3.status_code == 200
