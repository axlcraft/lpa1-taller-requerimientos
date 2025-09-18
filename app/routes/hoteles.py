# app/routes/hoteles.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Hotel, EstadoHotel
from app.extensions import db

hoteles_bp = Blueprint('hoteles', __name__)

@hoteles_bp.route('/')
def listar():
    """Lista todos los hoteles."""
    hoteles = Hotel.query.all()
    return render_template('hoteles/listar.html', hoteles=hoteles)

@hoteles_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    """Crear un nuevo hotel."""
    if request.method == 'POST':
        try:
            hotel = Hotel(
                nombre=request.form['nombre'],
                direccion=request.form.get('direccion'),
                telefono=request.form.get('telefono'),
                correo=request.form.get('correo'),
                ubicacion_geografica=request.form.get('ubicacion_geografica'),
                descripcion_servicios=request.form.get('descripcion_servicios'),
                estado=EstadoHotel.ACTIVO
            )
            
            db.session.add(hotel)
            db.session.commit()
            
            flash('Hotel creado exitosamente', 'success')
            return redirect(url_for('hoteles.listar'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear hotel: {str(e)}', 'error')
    
    return render_template('hoteles/crear.html')

@hoteles_bp.route('/<hotel_id>')
def detalle(hotel_id):
    """Detalle de un hotel específico."""
    hotel = Hotel.query.get_or_404(hotel_id)
    return render_template('hoteles/detalle.html', hotel=hotel)

@hoteles_bp.route('/<hotel_id>/editar', methods=['GET', 'POST'])
def editar(hotel_id):
    """Editar un hotel existente."""
    hotel = Hotel.query.get_or_404(hotel_id)
    
    if request.method == 'POST':
        try:
            hotel.nombre = request.form['nombre']
            hotel.direccion = request.form.get('direccion')
            hotel.telefono = request.form.get('telefono')
            hotel.correo = request.form.get('correo')
            hotel.ubicacion_geografica = request.form.get('ubicacion_geografica')
            hotel.descripcion_servicios = request.form.get('descripcion_servicios')
            
            if 'estado' in request.form:
                hotel.estado = EstadoHotel(request.form['estado'])
            
            db.session.commit()
            flash('Hotel actualizado exitosamente', 'success')
            return redirect(url_for('hoteles.detalle', hotel_id=hotel.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar hotel: {str(e)}', 'error')
    
    return render_template('hoteles/editar.html', hotel=hotel, estados=EstadoHotel)

@hoteles_bp.route('/<hotel_id>/eliminar', methods=['POST'])
def eliminar(hotel_id):
    """Eliminar un hotel."""
    hotel = Hotel.query.get_or_404(hotel_id)
    
    try:
        db.session.delete(hotel)
        db.session.commit()
        flash('Hotel eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar hotel: {str(e)}', 'error')
    
    return redirect(url_for('hoteles.listar'))
