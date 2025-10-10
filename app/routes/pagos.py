from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import TransaccionPago, EstadoPago, Reserva, TipoPago, EstadoReserva
from app.extensions import db
from datetime import datetime

pagos_bp = Blueprint('pagos', __name__)

@pagos_bp.route('/realizar/<transaccion_id>', methods=['GET', 'POST'])
def realizar(transaccion_id):
    transaccion = TransaccionPago.query.get_or_404(transaccion_id)
    if request.method == 'POST':
        transaccion.banco = request.form.get('banco')
        transaccion.numero_tarjeta = request.form.get('numero_tarjeta')
        transaccion.fecha_vencimiento = request.form.get('fecha_vencimiento')
        transaccion.cvv = request.form.get('cvv')
        transaccion.cuotas = int(request.form.get('cuotas', 1))
        transaccion.estado = EstadoPago.AUTORIZADO
        db.session.commit()
        flash('Pago realizado exitosamente.', 'success')
        return redirect(url_for('reservas.listar'))
    return render_template('pagos/realizar.html', transaccion=transaccion)

@pagos_bp.route('/reserva/<reserva_id>', methods=['GET', 'POST'])
def pagar_reserva(reserva_id):
    """Crear transacción de pago para una reserva y procesar el pago."""
    reserva = Reserva.query.get_or_404(reserva_id)
    
    # Verificar que el cliente autenticado sea el dueño de la reserva (si no es admin)
    if not session.get('is_superuser'):
        cliente_id = session.get('cliente_id')
        if not cliente_id or reserva.cliente_id != cliente_id:
            flash('No tienes permisos para pagar esta reserva', 'error')
            return redirect(url_for('reservas.listar'))
    
    # Verificar que la reserva se pueda pagar
    if reserva.estado == EstadoReserva.CANCELADA:
        flash('No se puede pagar una reserva cancelada', 'error')
        return redirect(url_for('reservas.detalle', reserva_id=reserva.id))
    
    if reserva.estado == EstadoReserva.CONFIRMADA:
        flash('Esta reserva ya está pagada', 'warning')
        return redirect(url_for('reservas.detalle', reserva_id=reserva.id))
    
    # Buscar o crear transacción de pago
    transaccion = TransaccionPago.query.filter_by(reserva_id=reserva_id).first()
    
    if not transaccion:
        # Crear nueva transacción
        transaccion = TransaccionPago(
            reserva_id=reserva_id,
            monto=reserva.total,
            tipo=TipoPago.TARJETA,
            estado=EstadoPago.PENDIENTE,
            fecha_transaccion=datetime.utcnow()
        )
        db.session.add(transaccion)
        db.session.commit()
    
    if request.method == 'POST':
        try:
            # Procesar el pago
            transaccion.banco = request.form.get('banco')
            transaccion.numero_tarjeta = request.form.get('numero_tarjeta')
            transaccion.fecha_vencimiento = request.form.get('fecha_vencimiento')
            transaccion.cvv = request.form.get('cvv')
            transaccion.cuotas = int(request.form.get('cuotas', 1))
            transaccion.estado = EstadoPago.AUTORIZADO
            
            # Actualizar estado de la reserva
            reserva.estado = EstadoReserva.CONFIRMADA
            
            db.session.commit()
            flash('Pago realizado exitosamente. Tu reserva ha sido confirmada.', 'success')
            return redirect(url_for('reservas.detalle', reserva_id=reserva.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al procesar el pago: {str(e)}', 'error')
    
    return render_template('pagos/realizar.html', transaccion=transaccion, reserva=reserva)
