from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from functools import wraps

auth_bp = Blueprint('auth', __name__)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('is_superuser'):
            flash('Acceso denegado. Requiere permisos de superusuario.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Primero verificar si es el superusuario del sistema
        if username == current_app.config['SUPERUSER_USERNAME'] and password == current_app.config['SUPERUSER_PASSWORD']:
            session['is_superuser'] = True
            session['user_id'] = 'admin'  # ID especial para admin
            session['user_name'] = 'Administrador'
            flash('Ingreso exitoso como superusuario', 'success')
            return redirect(url_for('main.index'))
        
        # Si no es admin, intentar login como cliente
        from app.models import Cliente
        cliente = Cliente.query.filter_by(username=username).first()
        if cliente and cliente.check_password(password):
            session['user_id'] = cliente.id
            session['cliente_id'] = cliente.id
            session['user_name'] = cliente.nombre_completo
            # Respect the persistent is_admin flag on the Cliente model
            session['is_superuser'] = bool(cliente.is_admin)
            flash('Ingreso exitoso', 'success')
            return redirect(url_for('main.index'))
        
        # Si ninguna de las dos opciones funciona
        flash('Credenciales inválidas', 'error')
    return render_template('auth/login.html')


@auth_bp.route('/login_client', methods=['GET', 'POST'])
def login_client():
    """Login para clientes usando username/password."""
    from app.models import Cliente
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        cliente = Cliente.query.filter_by(username=username).first()
        if cliente and cliente.check_password(password):
            session['user_id'] = cliente.id
            session['cliente_id'] = cliente.id
            session['user_name'] = cliente.nombre_completo
            # Respect the persistent is_admin flag on the Cliente model
            session['is_superuser'] = bool(cliente.is_admin)
            flash('Ingreso exitoso', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Credenciales inválidas', 'error')
    return render_template('auth/login_client.html')


@auth_bp.route('/dev_login')
def dev_login():
    """Development helper: login quickly as superuser when DEBUG is True.
    Creates or finds a Cliente record with correo == SUPERUSER_USERNAME and sets session as superuser.
    """
    from flask import current_app
    from app.models import Cliente
    if not current_app.config.get('DEBUG'):
        flash('Dev login only available in debug mode.', 'error')
        return redirect(url_for('main.index'))

    username = current_app.config.get('SUPERUSER_USERNAME')
    # Find or create a Cliente with correo=username
    cliente = Cliente.query.filter_by(correo=username).first()
    if not cliente:
        cliente = Cliente(nombre_completo='Dev Superuser', correo=username, username=username)
        cliente.set_password(current_app.config.get('SUPERUSER_PASSWORD', 'admin123'))
        cliente.is_admin = True
        from app.extensions import db
        db.session.add(cliente)
        db.session.commit()

    session['is_superuser'] = True
    session['user_id'] = cliente.id
    session['cliente_id'] = cliente.id
    session['user_name'] = cliente.nombre_completo
    flash('Logged in as dev superuser', 'success')
    return redirect(url_for('main.index'))


@auth_bp.route('/logout')
def logout():
    session.pop('is_superuser', None)
    session.pop('user_id', None)
    session.pop('cliente_id', None)
    session.pop('user_name', None)
    flash('Sesión cerrada', 'info')
    return redirect(url_for('main.index'))
