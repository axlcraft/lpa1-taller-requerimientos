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
    """Búsqueda de habitaciones con filtros y desplegable de ciudades."""
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    ciudad = request.args.get('ciudad', '')
    ubicacion = request.args.get('ubicacion', '')
    precio_max = request.args.get('precio_max', type=float)

    # Obtener ciudades únicas con hoteles activos
    from app.models.enums import EstadoHotel, EstadoHabitacion
    ciudades = [h.ubicacion_geografica for h in Hotel.query.filter_by(estado=EstadoHotel.ACTIVO).distinct(Hotel.ubicacion_geografica).all()]

    # Construir query base
    query = db.session.query(Habitacion).join(Hotel)

    # Filtrar por ciudad si se selecciona
    if ciudad:
        query = query.filter(Hotel.ubicacion_geografica == ciudad)

    # Aplicar filtros
    if ubicacion:
        query = query.filter(
            or_(
                Hotel.nombre.contains(ubicacion),
                Hotel.ubicacion_geografica.contains(ubicacion),
                Hotel.direccion.contains(ubicacion)
            )
        )

    if precio_max:
        query = query.filter(Habitacion.precio_base <= precio_max)

    query = query.filter(
        Habitacion.estado == EstadoHabitacion.ACTIVA,
        Hotel.estado == EstadoHotel.ACTIVO
    )

    habitaciones = query.all()

    return render_template('buscar.html', 
                         habitaciones=habitaciones,
                         fecha_inicio=fecha_inicio,
                         fecha_fin=fecha_fin,
                         ciudad=ciudad,
                         ciudades=ciudades,
                         ubicacion=ubicacion,
                         precio_max=precio_max)

@main_bp.route('/habitacion/<habitacion_id>')
def detalle_habitacion(habitacion_id):
    """Detalle de una habitación específica."""
    habitacion = Habitacion.query.get_or_404(habitacion_id)
    
    # Calcular calificación promedio
    calificaciones = [c.puntuacion for c in habitacion.calificaciones]
    calificacion_promedio = sum(calificaciones) / len(calificaciones) if calificaciones else 0
    
    return render_template('detalle_habitacion.html', 
                         habitacion=habitacion,
                         calificacion_promedio=calificacion_promedio)
