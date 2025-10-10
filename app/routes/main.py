# app/routes/main.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Hotel, Habitacion, Cliente
from app.extensions import db
from sqlalchemy import or_

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página principal con búsqueda de habitaciones y ciudades desplegables."""
    from app.models.enums import EstadoHotel, EstadoHabitacion, EstadoReserva
    hoteles_destacados = Hotel.query.filter_by(estado=EstadoHotel.ACTIVO).limit(6).all()
    num_hoteles = Hotel.query.filter_by(estado=EstadoHotel.ACTIVO).count()
    num_habitaciones = Habitacion.query.filter_by(estado=EstadoHabitacion.ACTIVA).count()
    num_clientes = Cliente.query.count()
    from app.models import Reserva
    num_reservas = Reserva.query.count()
    ciudades = [h.ubicacion_geografica for h in Hotel.query.filter_by(estado=EstadoHotel.ACTIVO).distinct(Hotel.ubicacion_geografica).all()]
    hoteles_por_ciudad = {}
    for ciudad in ciudades:
        hoteles = Hotel.query.filter_by(estado=EstadoHotel.ACTIVO, ubicacion_geografica=ciudad).all()
        hoteles_por_ciudad[ciudad] = [
            {
                'id': h.id,
                'nombre': h.nombre,
                'direccion': h.direccion,
                'telefono': h.telefono,
                'correo': h.correo
            } for h in hoteles
        ]
    return render_template('index.html', hoteles=hoteles_destacados, num_hoteles=num_hoteles, num_habitaciones=num_habitaciones, num_clientes=num_clientes, num_reservas=num_reservas, ciudades=ciudades, hoteles_por_ciudad=hoteles_por_ciudad)

@main_bp.route('/buscar')
def buscar():
    """Página de búsqueda de habitaciones con filtros avanzados"""
    from app.models.enums import EstadoHotel, EstadoHabitacion
    from sqlalchemy import and_
    from datetime import datetime
    
    # Obtener todas las ciudades para el dropdown
    ciudades = db.session.query(Hotel.ubicacion_geografica.distinct()).order_by(Hotel.ubicacion_geografica).all()
    ciudades = [ciudad[0] for ciudad in ciudades if ciudad[0]]
    
    # Obtener parámetros de búsqueda avanzada
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    ciudad = request.args.get('ciudad')
    capacidad = request.args.get('capacidad', type=int)
    precio_min = request.args.get('precio_min', type=float)
    precio_max = request.args.get('precio_max', type=float)
    tipo = request.args.get('tipo')
    calificacion_min = request.args.get('calificacion_min', type=float)
    servicios_seleccionados = request.args.getlist('servicios')
    hotel_filter = request.args.get('hotel_filter')  # Nuevo filtro por hotel específico
    
    # Construir consulta base
    query = db.session.query(Habitacion).join(Hotel).filter(
        and_(
            Habitacion.estado == EstadoHabitacion.ACTIVA,
            Hotel.estado == EstadoHotel.ACTIVO
        )
    )
    
    # Aplicar filtros
    if ciudad:
        query = query.filter(Hotel.ubicacion_geografica == ciudad)
    
    if hotel_filter:
        query = query.filter(Hotel.id == hotel_filter)
    
    if capacidad:
        query = query.filter(Habitacion.capacidad >= capacidad)
    
    if precio_min is not None:
        query = query.filter(Habitacion.precio_base >= precio_min)
    
    if precio_max is not None:
        query = query.filter(Habitacion.precio_base <= precio_max)
    
    if tipo:
        query = query.filter(Habitacion.tipo.ilike(f'%{tipo}%'))
    
    # Filtro de servicios incluidos
    if servicios_seleccionados:
        for servicio in servicios_seleccionados:
            query = query.filter(Habitacion.servicios_incluidos.ilike(f'%{servicio}%'))
    
    # Ejecutar consulta
    habitaciones = query.order_by(Habitacion.precio_base).all()
    
    # Calcular calificación promedio para cada habitación
    habitaciones_con_calificacion = []
    for hab in habitaciones:
        calificaciones_vals = []
        for c in hab.calificaciones:
            val = getattr(c, 'estrellas_habitacion', None) or getattr(c, 'puntuacion', None)
            if val is not None:
                calificaciones_vals.append(val)
        calificacion_promedio = sum(calificaciones_vals) / len(calificaciones_vals) if calificaciones_vals else 0
        
        # Filtro de calificación mínima
        if calificacion_min is None or calificacion_promedio >= calificacion_min:
            habitaciones_con_calificacion.append({
                'habitacion': hab,
                'calificacion_promedio': calificacion_promedio
            })
    
    return render_template('buscar.html', 
                         habitaciones=habitaciones_con_calificacion,
                         ciudades=ciudades,
                         fecha_inicio=fecha_inicio,
                         fecha_fin=fecha_fin,
                         ciudad=ciudad,
                         capacidad=capacidad,
                         precio_min=precio_min,
                         precio_max=precio_max,
                         tipo=tipo,
                         calificacion_min=calificacion_min,
                         servicios_seleccionados=servicios_seleccionados,
                         hotel_filter=hotel_filter)

@main_bp.route('/habitacion/<habitacion_id>')
def detalle_habitacion(habitacion_id):
    """Detalle de una habitación específica."""
    habitacion = Habitacion.query.get_or_404(habitacion_id)
    
    # Calcular calificación promedio usando el campo moderno 'estrellas_habitacion'
    calificaciones_vals = []
    for c in habitacion.calificaciones:
        val = getattr(c, 'estrellas_habitacion', None) or getattr(c, 'puntuacion', None)
        if val is not None:
            calificaciones_vals.append(val)
    calificacion_promedio = sum(calificaciones_vals) / len(calificaciones_vals) if calificaciones_vals else 0
    
    return render_template('detalle_habitacion.html', 
                         habitacion=habitacion,
                         calificacion_promedio=calificacion_promedio)
