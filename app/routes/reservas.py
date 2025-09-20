

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Reserva, Cliente, Habitacion, EstadoReserva, TransaccionPago, TipoPago, EstadoPago, Hotel
from app.extensions import db
from datetime import datetime, date

reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('/listar')
def listar():
    """Lista todas las reservas."""
    reservas = Reserva.query.join(Cliente).join(Habitacion).all()
    return render_template('reservas/listar.html', reservas=reservas)

@reservas_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    """Crear una nueva reserva para una habitación."""
    from app.models.enums import EstadoHotel, EstadoHabitacion
    habitaciones = Habitacion.query.join(Habitacion.hotel).filter(Habitacion.estado==EstadoHabitacion.ACTIVA, Hotel.estado==EstadoHotel.ACTIVO).all()
    clientes = Cliente.query.all()
    
    if request.method == 'POST':
        try:
            if request.form['cliente_id'] == 'no_registrado':
                flash('DEBES REGISTRARTE PARA PODER RESERVAR...', 'error')
                return render_template('reservas/crear.html', habitaciones=habitaciones, clientes=clientes, tipos_pago=TipoPago)

            habitacion = Habitacion.query.get_or_404(request.form['habitacion_id'])
            fecha_inicio = datetime.strptime(request.form['fecha_inicio'], '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(request.form['fecha_fin'], '%Y-%m-%d').date()

            # Validaciones básicas
            if fecha_inicio >= fecha_fin:
                flash('La fecha de fin debe ser posterior a la fecha de inicio', 'error')
                return render_template('reservas/crear.html', habitaciones=habitaciones, clientes=clientes, tipos_pago=TipoPago)

            if fecha_inicio < date.today():
                flash('No se pueden hacer reservas para fechas pasadas', 'error')
                return render_template('reservas/crear.html', habitaciones=habitaciones, clientes=clientes, tipos_pago=TipoPago)

            cantidad_personas = int(request.form['cantidad_personas'])
            if cantidad_personas > habitacion.capacidad:
                flash(f'La habitación solo tiene capacidad para {habitacion.capacidad} personas', 'error')
                return render_template('reservas/crear.html', habitaciones=habitaciones, clientes=clientes, tipos_pago=TipoPago)

            # Calcular total (precio base * días)
            dias = (fecha_fin - fecha_inicio).days
            total = float(habitacion.precio_base) * dias

            # Crear la reserva
            reserva = Reserva(
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                cantidad_personas=cantidad_personas,
                total=total,
                estado=EstadoReserva.PENDIENTE,
                cliente_id=request.form['cliente_id'],
                habitacion_id=habitacion.id
            )

            db.session.add(reserva)
            db.session.flush()  # Para obtener el ID
            
            # Crear transacción de pago
            transaccion = TransaccionPago(
                tipo=TipoPago(request.form.get('tipo_pago', 'tarjeta')),
                monto=total,
                estado=EstadoPago.PENDIENTE,
                reserva_id=reserva.id
            )
            
            db.session.add(transaccion)
            db.session.commit()
            
            flash('Reserva creada exitosamente', 'success')
            return redirect(url_for('reservas.detalle', reserva_id=reserva.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear reserva: {str(e)}', 'error')
    
    return render_template('reservas/crear.html', 
                         habitaciones=habitaciones,
                         clientes=clientes,
                         tipos_pago=TipoPago)

@reservas_bp.route('/<reserva_id>')
def detalle(reserva_id):
    """Detalle de una reserva específica."""
    reserva = Reserva.query.get_or_404(reserva_id)
    return render_template('reservas/detalle.html', reserva=reserva)



@reservas_bp.route('/<reserva_id>/editar', methods=['GET', 'POST'])
def editar(reserva_id):
    """Editar una reserva existente."""
    from app.models.enums import EstadoHotel, EstadoHabitacion
    reserva = Reserva.query.get_or_404(reserva_id)
    habitaciones = Habitacion.query.join(Habitacion.hotel).filter(Habitacion.estado==EstadoHabitacion.ACTIVA, Hotel.estado==EstadoHotel.ACTIVO).all()
    clientes = Cliente.query.all()
    if request.method == 'POST':
        try:
            habitacion = Habitacion.query.get_or_404(request.form['habitacion_id'])
            fecha_inicio = datetime.strptime(request.form['fecha_inicio'], '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(request.form['fecha_fin'], '%Y-%m-%d').date()
            cantidad_personas = int(request.form['cantidad_personas'])
            if fecha_inicio >= fecha_fin:
                flash('La fecha de fin debe ser posterior a la fecha de inicio', 'error')
                return render_template('reservas/editar.html', reserva=reserva, habitaciones=habitaciones, clientes=clientes)
            if fecha_inicio < date.today():
                flash('No se pueden hacer reservas para fechas pasadas', 'error')
                return render_template('reservas/editar.html', reserva=reserva, habitaciones=habitaciones, clientes=clientes)
            if cantidad_personas > habitacion.capacidad:
                flash(f'La habitación solo tiene capacidad para {habitacion.capacidad} personas', 'error')
                return render_template('reservas/editar.html', reserva=reserva, habitaciones=habitaciones, clientes=clientes)
            reserva.habitacion_id = habitacion.id
            reserva.cliente_id = request.form['cliente_id']
            reserva.fecha_inicio = fecha_inicio
            reserva.fecha_fin = fecha_fin
            reserva.cantidad_personas = cantidad_personas
            dias = (fecha_fin - fecha_inicio).days
            reserva.total = float(habitacion.precio_base) * dias
            db.session.commit()
            flash('Reserva actualizada exitosamente', 'success')
            return redirect(url_for('reservas.detalle', reserva_id=reserva.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar reserva: {str(e)}', 'error')
    return render_template('reservas/editar.html', reserva=reserva, habitaciones=habitaciones, clientes=clientes)

@reservas_bp.route('/<reserva_id>/completar', methods=['POST'])
def completar(reserva_id):
    """Marcar una reserva como completada."""
    reserva = Reserva.query.get_or_404(reserva_id)
    
    try:
        reserva.estado = EstadoReserva.COMPLETADA
        db.session.commit()
        flash('Reserva marcada como completada', 'success')
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error al completar reserva: {str(e)}', 'error')
    
    return redirect(url_for('reservas.detalle', reserva_id=reserva.id))
