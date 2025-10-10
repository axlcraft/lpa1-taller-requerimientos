# app/routes/politicas.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.models import Hotel, PoliticaCancelacion, PoliticaPago
from app.models.enums import TipoPago
from app.extensions import db
from sqlalchemy.exc import IntegrityError

politicas_bp = Blueprint('politicas', __name__, url_prefix='/politicas')

def check_admin():
    """Verificar si el usuario es administrador"""
    return session.get('is_superuser', False)

@politicas_bp.route('/')
def listar():
    """Listar todas las políticas de cancelación y pago"""
    if not check_admin():
        flash('Acceso denegado. Se requieren permisos de administrador.', 'error')
        return redirect(url_for('main.index'))
    
    hoteles = Hotel.query.filter_by(estado='ACTIVO').all()
    
    # Obtener políticas por hotel
    politicas_por_hotel = {}
    for hotel in hoteles:
        politicas_por_hotel[hotel.id] = {
            'hotel': hotel,
            'cancelacion': list(hotel.politicas_cancelacion),
            'pago': list(hotel.politicas_pago)
        }
    
    return render_template('politicas/listar.html', 
                         politicas_por_hotel=politicas_por_hotel,
                         hoteles=hoteles)

@politicas_bp.route('/cancelacion/crear/<hotel_id>', methods=['GET', 'POST'])
def crear_cancelacion(hotel_id):
    """Crear nueva política de cancelación"""
    if not check_admin():
        flash('Acceso denegado. Se requieren permisos de administrador.', 'error')
        return redirect(url_for('main.index'))
    
    hotel = Hotel.query.get_or_404(hotel_id)
    
    if request.method == 'POST':
        try:
            politica = PoliticaCancelacion(
                nombre=request.form['nombre'],
                descripcion=request.form['descripcion'],
                penalidad=float(request.form.get('penalidad', 0)),
                dias_anticipacion_reembolso=int(request.form.get('dias_anticipacion_reembolso', 0)),
                hotel_id=hotel_id
            )
            
            db.session.add(politica)
            db.session.commit()
            flash(f'Política de cancelación "{politica.nombre}" creada exitosamente', 'success')
            return redirect(url_for('politicas.listar'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la política: {str(e)}', 'error')
    
    return render_template('politicas/crear_cancelacion.html', hotel=hotel)

@politicas_bp.route('/pago/crear/<hotel_id>', methods=['GET', 'POST'])
def crear_pago(hotel_id):
    """Crear nueva política de pago"""
    if not check_admin():
        flash('Acceso denegado. Se requieren permisos de administrador.', 'error')
        return redirect(url_for('main.index'))
    
    hotel = Hotel.query.get_or_404(hotel_id)
    
    if request.method == 'POST':
        try:
            politica = PoliticaPago(
                tipo=TipoPago[request.form['tipo']],
                descripcion=request.form['descripcion'],
                hotel_id=hotel_id
            )
            
            db.session.add(politica)
            db.session.commit()
            flash(f'Política de pago "{politica.tipo.value}" creada exitosamente', 'success')
            return redirect(url_for('politicas.listar'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la política: {str(e)}', 'error')
    
    tipos_pago = [tipo for tipo in TipoPago]
    return render_template('politicas/crear_pago.html', hotel=hotel, tipos_pago=tipos_pago)

@politicas_bp.route('/cancelacion/editar/<politica_id>', methods=['GET', 'POST'])
def editar_cancelacion(politica_id):
    """Editar política de cancelación existente"""
    if not check_admin():
        flash('Acceso denegado. Se requieren permisos de administrador.', 'error')
        return redirect(url_for('main.index'))
    
    politica = PoliticaCancelacion.query.get_or_404(politica_id)
    
    if request.method == 'POST':
        try:
            politica.nombre = request.form['nombre']
            politica.descripcion = request.form['descripcion']
            politica.penalidad = float(request.form.get('penalidad', 0))
            politica.dias_anticipacion_reembolso = int(request.form.get('dias_anticipacion_reembolso', 0))
            
            db.session.commit()
            flash(f'Política de cancelación "{politica.nombre}" actualizada exitosamente', 'success')
            return redirect(url_for('politicas.listar'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la política: {str(e)}', 'error')
    
    return render_template('politicas/editar_cancelacion.html', politica=politica)

@politicas_bp.route('/pago/editar/<politica_id>', methods=['GET', 'POST'])
def editar_pago(politica_id):
    """Editar política de pago existente"""
    if not check_admin():
        flash('Acceso denegado. Se requieren permisos de administrador.', 'error')
        return redirect(url_for('main.index'))
    
    politica = PoliticaPago.query.get_or_404(politica_id)
    
    if request.method == 'POST':
        try:
            politica.tipo = TipoPago[request.form['tipo']]
            politica.descripcion = request.form['descripcion']
            
            db.session.commit()
            flash(f'Política de pago actualizada exitosamente', 'success')
            return redirect(url_for('politicas.listar'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la política: {str(e)}', 'error')
    
    tipos_pago = [tipo for tipo in TipoPago]
    return render_template('politicas/editar_pago.html', politica=politica, tipos_pago=tipos_pago)

@politicas_bp.route('/cancelacion/eliminar/<politica_id>', methods=['POST'])
def eliminar_cancelacion(politica_id):
    """Eliminar política de cancelación"""
    if not check_admin():
        return jsonify({'success': False, 'message': 'Acceso denegado'}), 403
    
    try:
        politica = PoliticaCancelacion.query.get_or_404(politica_id)
        nombre = politica.nombre
        
        db.session.delete(politica)
        db.session.commit()
        
        flash(f'Política de cancelación "{nombre}" eliminada exitosamente', 'success')
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error al eliminar: {str(e)}'}), 500

@politicas_bp.route('/pago/eliminar/<politica_id>', methods=['POST'])
def eliminar_pago(politica_id):
    """Eliminar política de pago"""
    if not check_admin():
        return jsonify({'success': False, 'message': 'Acceso denegado'}), 403
    
    try:
        politica = PoliticaPago.query.get_or_404(politica_id)
        tipo = politica.tipo.value
        
        db.session.delete(politica)
        db.session.commit()
        
        flash(f'Política de pago "{tipo}" eliminada exitosamente', 'success')
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error al eliminar: {str(e)}'}), 500