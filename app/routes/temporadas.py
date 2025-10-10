# app/routes/temporadas.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models import Hotel, Temporada, Habitacion, Promocion
from app.models.enums import TipoTemporada, EstadoHotel, EstadoHabitacion
from app.extensions import db
from datetime import datetime, date
from decimal import Decimal

temporadas_bp = Blueprint('temporadas', __name__, url_prefix='/temporadas')

def check_admin():
    """Verificar si el usuario es administrador"""
    return session.get('is_superuser', False)

@temporadas_bp.route('/')
def listar():
    """Listar todas las temporadas y sistema de tarifación"""
    if not check_admin():
        flash('Acceso denegado. Se requieren permisos de administrador.', 'error')
        return redirect(url_for('main.index'))
    
    hoteles = Hotel.query.filter_by(estado=EstadoHotel.ACTIVO).all()
    
    # Obtener temporadas por hotel
    temporadas_por_hotel = {}
    for hotel in hoteles:
        temporadas_por_hotel[hotel.id] = {
            'hotel': hotel,
            'temporadas': list(hotel.temporadas),
            'promociones_activas': Promocion.query.filter_by(hotel_id=hotel.id).filter(
                Promocion.fecha_fin >= date.today()
            ).all()
        }
    
    return render_template('temporadas/listar.html', 
                         temporadas_por_hotel=temporadas_por_hotel,
                         hoteles=hoteles)

@temporadas_bp.route('/crear/<hotel_id>', methods=['GET', 'POST'])
def crear(hotel_id):
    """Crear nueva temporada"""
    if not check_admin():
        flash('Acceso denegado. Se requieren permisos de administrador.', 'error')
        return redirect(url_for('main.index'))
    
    hotel = Hotel.query.get_or_404(hotel_id)
    
    if request.method == 'POST':
        try:
            temporada = Temporada(
                nombre=request.form['nombre'],
                fecha_inicio=datetime.strptime(request.form['fecha_inicio'], '%Y-%m-%d').date(),
                fecha_fin=datetime.strptime(request.form['fecha_fin'], '%Y-%m-%d').date(),
                tipo=TipoTemporada[request.form['tipo']],
                hotel_id=hotel_id
            )
            
            # Validar que las fechas sean coherentes
            if temporada.fecha_inicio > temporada.fecha_fin:
                flash('La fecha de inicio no puede ser posterior a la fecha de fin', 'error')
                return render_template('temporadas/crear.html', hotel=hotel, tipos_temporada=TipoTemporada)
            
            db.session.add(temporada)
            db.session.commit()
            flash(f'Temporada "{temporada.nombre}" creada exitosamente', 'success')
            return redirect(url_for('temporadas.listar'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la temporada: {str(e)}', 'error')
    
    tipos_temporada = [tipo for tipo in TipoTemporada]
    return render_template('temporadas/crear.html', hotel=hotel, tipos_temporada=tipos_temporada)

@temporadas_bp.route('/editar/<temporada_id>', methods=['GET', 'POST'])
def editar(temporada_id):
    """Editar temporada existente"""
    if not check_admin():
        flash('Acceso denegado. Se requieren permisos de administrador.', 'error')
        return redirect(url_for('main.index'))
    
    temporada = Temporada.query.get_or_404(temporada_id)
    
    if request.method == 'POST':
        try:
            temporada.nombre = request.form['nombre']
            temporada.fecha_inicio = datetime.strptime(request.form['fecha_inicio'], '%Y-%m-%d').date()
            temporada.fecha_fin = datetime.strptime(request.form['fecha_fin'], '%Y-%m-%d').date()
            temporada.tipo = TipoTemporada[request.form['tipo']]
            
            # Validar fechas
            if temporada.fecha_inicio > temporada.fecha_fin:
                flash('La fecha de inicio no puede ser posterior a la fecha de fin', 'error')
                return render_template('temporadas/editar.html', temporada=temporada, tipos_temporada=TipoTemporada)
            
            db.session.commit()
            flash(f'Temporada "{temporada.nombre}" actualizada exitosamente', 'success')
            return redirect(url_for('temporadas.listar'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la temporada: {str(e)}', 'error')
    
    tipos_temporada = [tipo for tipo in TipoTemporada]
    return render_template('temporadas/editar.html', temporada=temporada, tipos_temporada=tipos_temporada)

@temporadas_bp.route('/eliminar/<temporada_id>', methods=['POST'])
def eliminar(temporada_id):
    """Eliminar temporada"""
    if not check_admin():
        return jsonify({'success': False, 'message': 'Acceso denegado'}), 403
    
    try:
        temporada = Temporada.query.get_or_404(temporada_id)
        nombre = temporada.nombre
        
        db.session.delete(temporada)
        db.session.commit()
        
        flash(f'Temporada "{nombre}" eliminada exitosamente', 'success')
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error al eliminar: {str(e)}'}), 500

@temporadas_bp.route('/calcular-precio', methods=['POST'])
def calcular_precio():
    """API para calcular precio dinámico de habitación basado en temporada y promociones"""
    data = request.get_json()
    habitacion_id = data.get('habitacion_id')
    fecha_checkin = datetime.strptime(data.get('fecha_checkin'), '%Y-%m-%d').date()
    fecha_checkout = datetime.strptime(data.get('fecha_checkout'), '%Y-%m-%d').date()
    
    try:
        habitacion = Habitacion.query.get_or_404(habitacion_id)
        hotel = habitacion.hotel
        
        precio_base = float(habitacion.precio_base)
        precio_final = precio_base
        
        # 1. Aplicar modificador de temporada
        temporada_aplicable = None
        for temporada in hotel.temporadas:
            if temporada.fecha_inicio <= fecha_checkin <= temporada.fecha_fin:
                temporada_aplicable = temporada
                break
        
        modificador_temporada = 1.0
        if temporada_aplicable:
            if temporada_aplicable.tipo == TipoTemporada.ALTA:
                modificador_temporada = 1.5  # +50%
            elif temporada_aplicable.tipo == TipoTemporada.MEDIA:
                modificador_temporada = 1.2  # +20%
            elif temporada_aplicable.tipo == TipoTemporada.BAJA:
                modificador_temporada = 0.8  # -20%
        
        precio_con_temporada = precio_base * modificador_temporada
        
        # 2. Aplicar promociones activas
        promocion_aplicable = None
        mejor_descuento = 0
        
        for promocion in hotel.promociones:
            if (promocion.fecha_inicio <= fecha_checkin <= promocion.fecha_fin and 
                float(promocion.descuento) > mejor_descuento):
                promocion_aplicable = promocion
                mejor_descuento = float(promocion.descuento)
        
        descuento_total = mejor_descuento / 100.0 if promocion_aplicable else 0
        precio_final = precio_con_temporada * (1 - descuento_total)
        
        # Calcular noches
        noches = (fecha_checkout - fecha_checkin).days
        precio_total = precio_final * noches
        
        return jsonify({
            'success': True,
            'precio_base': precio_base,
            'precio_con_temporada': round(precio_con_temporada, 2),
            'precio_por_noche': round(precio_final, 2),
            'precio_total': round(precio_total, 2),
            'noches': noches,
            'temporada': {
                'nombre': temporada_aplicable.nombre if temporada_aplicable else 'Temporada Regular',
                'tipo': temporada_aplicable.tipo.value if temporada_aplicable else 'Regular',
                'modificador': modificador_temporada
            },
            'promocion': {
                'nombre': promocion_aplicable.nombre if promocion_aplicable else None,
                'descuento': mejor_descuento
            } if promocion_aplicable else None
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@temporadas_bp.route('/simulador/<hotel_id>')
def simulador(hotel_id):
    """Simulador de precios dinámicos"""
    if not check_admin():
        flash('Acceso denegado. Se requieren permisos de administrador.', 'error')
        return redirect(url_for('main.index'))
    
    hotel = Hotel.query.get_or_404(hotel_id)
    habitaciones = Habitacion.query.filter_by(hotel_id=hotel_id, estado=EstadoHabitacion.ACTIVA).all()
    
    return render_template('temporadas/simulador.html', hotel=hotel, habitaciones=habitaciones)