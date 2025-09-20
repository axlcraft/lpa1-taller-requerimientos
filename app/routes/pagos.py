from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import TransaccionPago, EstadoPago
from app.extensions import db

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
