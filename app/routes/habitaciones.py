# app/routes/habitaciones.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Habitacion, Hotel, TipoHabitacion, EstadoHabitacion
from app.extensions import db

habitaciones_bp = Blueprint('habitaciones', __name__)

@habitaciones_bp.route('/')
def listar():
    """Lista todas las habitaciones."""
    habitaciones = Habitacion.query.join(Hotel).all()
    return render_template('habitaciones/listar.html', habitaciones=habitaciones)

@habitaciones_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    """Crear una nueva habitación."""
    from app.models.enums import EstadoHotel
    hoteles = Hotel.query.filter_by(estado=EstadoHotel.ACTIVO).all()
    
    if request.method == 'POST':
        try:
            habitacion = Habitacion(
                tipo=TipoHabitacion(request.form['tipo']),
                descripcion=request.form.get('descripcion'),
                precio_base=float(request.form['precio_base']),
                capacidad=int(request.form['capacidad']),
                estado=EstadoHabitacion.ACTIVA,
                hotel_id=request.form['hotel_id']
            )
            
            db.session.add(habitacion)
            db.session.commit()
            
            flash('Habitación creada exitosamente', 'success')
            return redirect(url_for('habitaciones.listar'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear habitación: {str(e)}', 'error')
    
    return render_template('habitaciones/crear.html', 
                         hoteles=hoteles, 
                         tipos=TipoHabitacion)

@habitaciones_bp.route('/<habitacion_id>')
def detalle(habitacion_id):
    """Detalle de una habitación específica."""
    habitacion = Habitacion.query.get_or_404(habitacion_id)
    
    # Calcular calificación promedio
    calificaciones = [c.puntuacion for c in habitacion.calificaciones]
    calificacion_promedio = sum(calificaciones) / len(calificaciones) if calificaciones else 0
    
    return render_template('habitaciones/detalle.html', 
                         habitacion=habitacion,
                         calificacion_promedio=calificacion_promedio)

@habitaciones_bp.route('/<habitacion_id>/editar', methods=['GET', 'POST'])
def editar(habitacion_id):
    """Editar una habitación existente."""
    habitacion = Habitacion.query.get_or_404(habitacion_id)
    from app.models.enums import EstadoHotel
    hoteles = Hotel.query.filter_by(estado=EstadoHotel.ACTIVO).all()
    
    if request.method == 'POST':
        try:
            habitacion.tipo = TipoHabitacion(request.form['tipo'])
            habitacion.descripcion = request.form.get('descripcion')
            habitacion.precio_base = float(request.form['precio_base'])
            habitacion.capacidad = int(request.form['capacidad'])
            
            if 'estado' in request.form:
                habitacion.estado = EstadoHabitacion(request.form['estado'])
            
            habitacion.hotel_id = request.form['hotel_id']
            
            db.session.commit()
            flash('Habitación actualizada exitosamente', 'success')
            return redirect(url_for('habitaciones.detalle', habitacion_id=habitacion.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar habitación: {str(e)}', 'error')
    
    return render_template('habitaciones/editar.html', 
                         habitacion=habitacion, 
                         hoteles=hoteles,
                         tipos=TipoHabitacion,
                         estados=EstadoHabitacion)

@habitaciones_bp.route('/<habitacion_id>/eliminar', methods=['POST'])
def eliminar(habitacion_id):
    """Eliminar una habitación."""
    habitacion = Habitacion.query.get_or_404(habitacion_id)
    
    try:
        db.session.delete(habitacion)
        db.session.commit()
        flash('Habitación eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar habitación: {str(e)}', 'error')
    
    return redirect(url_for('habitaciones.listar'))
