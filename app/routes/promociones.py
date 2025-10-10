from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import Promocion, Hotel
from app.extensions import db
from datetime import datetime

promociones_bp = Blueprint('promociones', __name__)

@promociones_bp.route('/')
def listar():
    """Listar todas las promociones."""
    promociones = Promocion.query.join(Promocion.hotel).all()
    return render_template('promociones/listar.html', promociones=promociones)

@promociones_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    """Crear una nueva promoción."""
    if not session.get('is_superuser'):
        flash('No tienes permisos para crear promociones', 'error')
        return redirect(url_for('promociones.listar'))
    
    if request.method == 'POST':
        try:
            promocion = Promocion(
                nombre=request.form.get('nombre'),
                descripcion=request.form.get('descripcion'),
                descuento=float(request.form.get('descuento', 0)),
                servicios_adicionales=request.form.get('servicios_adicionales'),
                fecha_inicio=datetime.strptime(request.form.get('fecha_inicio'), '%Y-%m-%d').date(),
                fecha_fin=datetime.strptime(request.form.get('fecha_fin'), '%Y-%m-%d').date(),
                hotel_id=request.form.get('hotel_id')
            )
            
            db.session.add(promocion)
            db.session.commit()
            flash('Promoción creada exitosamente', 'success')
            return redirect(url_for('promociones.listar'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear promoción: {str(e)}', 'error')
    
    hoteles = Hotel.query.all()
    return render_template('promociones/crear.html', hoteles=hoteles)

@promociones_bp.route('/<promocion_id>')
def detalle(promocion_id):
    """Ver detalles de una promoción."""
    from datetime import date
    promocion = Promocion.query.get_or_404(promocion_id)
    return render_template('promociones/detalle.html', promocion=promocion, today=date.today())

@promociones_bp.route('/<promocion_id>/editar', methods=['GET', 'POST'])
def editar(promocion_id):
    """Editar una promoción existente."""
    if not session.get('is_superuser'):
        flash('No tienes permisos para editar promociones', 'error')
        return redirect(url_for('promociones.detalle', promocion_id=promocion_id))
    
    promocion = Promocion.query.get_or_404(promocion_id)
    
    if request.method == 'POST':
        try:
            promocion.nombre = request.form.get('nombre')
            promocion.descripcion = request.form.get('descripcion')
            promocion.descuento = float(request.form.get('descuento', 0))
            promocion.servicios_adicionales = request.form.get('servicios_adicionales')
            promocion.fecha_inicio = datetime.strptime(request.form.get('fecha_inicio'), '%Y-%m-%d').date()
            promocion.fecha_fin = datetime.strptime(request.form.get('fecha_fin'), '%Y-%m-%d').date()
            promocion.hotel_id = request.form.get('hotel_id')
            
            db.session.commit()
            flash('Promoción actualizada exitosamente', 'success')
            return redirect(url_for('promociones.detalle', promocion_id=promocion.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar promoción: {str(e)}', 'error')
    
    hoteles = Hotel.query.all()
    return render_template('promociones/editar.html', promocion=promocion, hoteles=hoteles)

@promociones_bp.route('/<promocion_id>/eliminar', methods=['POST'])
def eliminar(promocion_id):
    """Eliminar una promoción."""
    if not session.get('is_superuser'):
        flash('No tienes permisos para eliminar promociones', 'error')
        return redirect(url_for('promociones.listar'))
    
    promocion = Promocion.query.get_or_404(promocion_id)
    
    try:
        db.session.delete(promocion)
        db.session.commit()
        flash('Promoción eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar promoción: {str(e)}', 'error')
    
    return redirect(url_for('promociones.listar'))