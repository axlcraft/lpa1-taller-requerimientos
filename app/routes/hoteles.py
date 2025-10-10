# app/routes/hoteles.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Hotel, EstadoHotel
from app.extensions import db
from app.routes.auth import admin_required

hoteles_bp = Blueprint('hoteles', __name__)

@hoteles_bp.route('/')
def listar():
    """Lista todos los hoteles con filtros por ciudad y estado."""
    ciudad = request.args.get('ciudad')
    estado = request.args.get('estado')
    query = Hotel.query
    if ciudad:
        query = query.filter(Hotel.ubicacion_geografica == ciudad)
    if estado:
        query = query.filter(Hotel.estado == EstadoHotel[estado.upper()])
    hoteles = query.all()

    # Agrupar hoteles por ciudad para el desplegable
    hoteles_por_ciudad = {}
    for hotel in Hotel.query.all():
        ciudad_hotel = hotel.ubicacion_geografica
        if ciudad_hotel not in hoteles_por_ciudad:
            hoteles_por_ciudad[ciudad_hotel] = []
        hoteles_por_ciudad[ciudad_hotel].append(hotel)
    
    # Obtener lista de ciudades únicas desde el diccionario
    ciudades = list(hoteles_por_ciudad.keys())
    
    return render_template('hoteles/listar.html', 
                         hoteles=hoteles, 
                         ciudades=ciudades, 
                         hoteles_por_ciudad=hoteles_por_ciudad,
                         ciudad_sel=ciudad, 
                         estado_sel=estado)

@hoteles_bp.route('/crear', methods=['GET', 'POST'])
@admin_required
def crear():
    """Crear un nuevo hotel."""
    if request.method == 'POST':
        try:
            estado_form = request.form.get('estado', 'activo')
            hotel = Hotel(
                nombre=request.form['nombre'],
                direccion=request.form.get('direccion'),
                telefono=request.form.get('telefono'),
                correo=request.form.get('correo'),
                ubicacion_geografica=request.form.get('ubicacion_geografica'),
                descripcion_servicios=request.form.get('descripcion_servicios'),
                estado=EstadoHotel(estado_form)
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
    """Detalle de un hotel específico con habitaciones disponibles y promociones."""
    from datetime import date
    hotel = Hotel.query.get_or_404(hotel_id)
    habitaciones_disponibles = [h for h in hotel.habitaciones if h.estado.name == 'ACTIVA']
    
    # Calcular calificación promedio del hotel
    calificaciones_objs = hotel.calificaciones or []
    estrellas_hotel = [c.estrellas_hotel for c in calificaciones_objs if c.estrellas_hotel is not None]
    promedio_hotel = sum(estrellas_hotel) / len(estrellas_hotel) if estrellas_hotel else 0

    # Obtener promociones del hotel ordenadas por estado (activas primero)
    promociones = hotel.promociones
    today = date.today()
    
    # Separar promociones por estado para mejor presentación
    promociones_activas = [p for p in promociones if p.fecha_inicio <= today <= p.fecha_fin]
    promociones_futuras = [p for p in promociones if p.fecha_inicio > today]
    promociones_expiradas = [p for p in promociones if p.fecha_fin < today]

    return render_template('hoteles/detalle.html', 
                         hotel=hotel, 
                         habitaciones=habitaciones_disponibles, 
                         promedio_hotel=promedio_hotel, 
                         calificaciones=calificaciones_objs,
                         promociones_activas=promociones_activas,
                         promociones_futuras=promociones_futuras, 
                         promociones_expiradas=promociones_expiradas,
                         today=today)

@hoteles_bp.route('/<hotel_id>/editar', methods=['GET', 'POST'])
@admin_required
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
@admin_required
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
