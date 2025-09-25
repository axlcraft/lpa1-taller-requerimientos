"""
Script sencillo para crear un superuser de desarrollo en la DB.
Uso:
    source venv/bin/activate
    python3 scripts/create_dev_superuser.py

Este script crea (o actualiza) un usuario en la tabla 'clientes' con correo igual a
Config.SUPERUSER_USERNAME y contraseña en texto plano guardada en un campo 'is_superuser'
(la app usa session['is_superuser'] en runtime; aquí simplemente marca al cliente con correo especial).

Nota: este proyecto no tiene modelo Usuario separado; este script crea un cliente con el correo del superuser
y coloca una flag en una tabla auxiliar 'dev_admins' para identificarlo. Es una solución de desarrollo local.
"""
import os
from app import create_app
from app.extensions import db
from app.config import config

app = create_app('default')

with app.app_context():
    from app.models.cliente import Cliente
    from sqlalchemy.exc import IntegrityError

    username = app.config.get('SUPERUSER_USERNAME', 'admin')
    password = app.config.get('SUPERUSER_PASSWORD', 'admin123')

    # Buscar cliente por correo
    cliente = Cliente.query.filter_by(correo=username).first()
    if not cliente:
        cliente = Cliente(nombre_completo='Superuser', correo=username, telefono='', direccion='')
        cliente.username = username
        cliente.set_password(password)
        cliente.is_admin = True
        db.session.add(cliente)
        try:
            db.session.commit()
            print(f'Creado cliente superuser con correo {username} y marcado is_admin')
        except IntegrityError:
            db.session.rollback()
            cliente = Cliente.query.filter_by(correo=username).first()
    else:
        # Asegurar que tenga credenciales y flag is_admin
        updated = False
        if not cliente.username:
            cliente.username = username
            updated = True
        if not cliente.check_password(password):
            cliente.set_password(password)
            updated = True
        if not cliente.is_admin:
            cliente.is_admin = True
            updated = True
        if updated:
            db.session.add(cliente)
            db.session.commit()
            print(f'Cliente existente actualizado y marcado is_admin: {username}')

    # Guardar flag en un archivo local simple (dev-only)
    marker_path = os.path.join(os.getcwd(), '.dev_superuser')
    with open(marker_path, 'w') as f:
        f.write(str(cliente.id))

    print('Superuser dev marcado. Para login use el correo:', username)
    print('Este script es para desarrollo solamente.')
