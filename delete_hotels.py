from app import create_app
from app.extensions import db
from app.models.hotel import Hotel

app = create_app()

with app.app_context():
    deleted_1 = db.session.query(Hotel).filter(Hotel.nombre.like('%#1%')).delete(synchronize_session=False)
    deleted_2 = db.session.query(Hotel).filter(Hotel.nombre.like('%#2%')).delete(synchronize_session=False)
    deleted_3 = db.session.query(Hotel).filter(Hotel.nombre.like('%#3%')).delete(synchronize_session=False)
    db.session.commit()
    print(f"Hoteles eliminados: #1={deleted_1}, #2={deleted_2}, #3={deleted_3}")
