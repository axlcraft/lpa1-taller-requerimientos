# app/routes/evaluaciones.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Comentario, Calificacion, Cliente, Habitacion, Reserva, EstadoReserva
from app.extensions import db
from datetime import datetime

evaluaciones_bp = Blueprint('evaluaciones', __name__)

@evaluaciones_bp.route('/habitacion/<habitacion_id>/comentar', methods=['GET', 'POST'])
def comentar(habitacion_id):
    """Crear un comentario para una habitación."""
    habitacion = Habitacion.query.get_or_404(habitacion_id)
    clientes = Cliente.query.all()
    
    if request.method == 'POST':
        try:
            cliente_id = request.form['cliente_id']
            
            # Verificar si el cliente tuvo una reserva completada en esta habitación
            reserva_completada = Reserva.query.filter_by(
                cliente_id=cliente_id,
                habitacion_id=habitacion_id,
                estado=EstadoReserva.COMPLETADA
            ).first()
            
            if not reserva_completada:
                flash('Solo se pueden hacer comentarios después de completar una estadía', 'error')
                return render_template('evaluaciones/comentar.html', habitacion=habitacion, clientes=clientes)
            
            comentario = Comentario(
                contenido=request.form['contenido'],
                cliente_id=cliente_id,
                habitacion_id=habitacion_id
            )
            
            db.session.add(comentario)
            db.session.commit()
            
            flash('Comentario agregado exitosamente', 'success')
            return redirect(url_for('main.detalle_habitacion', habitacion_id=habitacion_id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar comentario: {str(e)}', 'error')
    
    return render_template('evaluaciones/comentar.html', habitacion=habitacion, clientes=clientes)

@evaluaciones_bp.route('/habitacion/<habitacion_id>/calificar', methods=['GET', 'POST'])
def calificar(habitacion_id):
    """Crear una calificación para una habitación."""
    habitacion = Habitacion.query.get_or_404(habitacion_id)
    clientes = Cliente.query.all()
    
    if request.method == 'POST':
        try:
            cliente_id = request.form['cliente_id']
            puntuacion = int(request.form['puntuacion'])
            
            # Validar puntuación
            if puntuacion < 1 or puntuacion > 5:
                flash('La calificación debe estar entre 1 y 5', 'error')
                return render_template('evaluaciones/calificar.html', habitacion=habitacion, clientes=clientes)
            
            # Verificar si el cliente tuvo una reserva completada en esta habitación
            reserva_completada = Reserva.query.filter_by(
                cliente_id=cliente_id,
                habitacion_id=habitacion_id,
                estado=EstadoReserva.COMPLETADA
            ).first()
            
            if not reserva_completada:
                flash('Solo se pueden hacer calificaciones después de completar una estadía', 'error')
                return render_template('evaluaciones/calificar.html', habitacion=habitacion, clientes=clientes)
            
            # Verificar si ya existe una calificación de este cliente para esta habitación
            calificacion_existente = Calificacion.query.filter_by(
                cliente_id=cliente_id,
                habitacion_id=habitacion_id
            ).first()
            
            if calificacion_existente:
                # Actualizar calificación existente
                calificacion_existente.puntuacion = puntuacion
                calificacion_existente.fecha = datetime.utcnow()
                flash('Calificación actualizada exitosamente', 'success')
            else:
                # Crear nueva calificación
                calificacion = Calificacion(
                    puntuacion=puntuacion,
                    cliente_id=cliente_id,
                    habitacion_id=habitacion_id
                )
                db.session.add(calificacion)
                flash('Calificación agregada exitosamente', 'success')
            
            db.session.commit()
            return redirect(url_for('main.detalle_habitacion', habitacion_id=habitacion_id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar calificación: {str(e)}', 'error')
    
    return render_template('evaluaciones/calificar.html', habitacion=habitacion, clientes=clientes)

@evaluaciones_bp.route('/comentario/<comentario_id>/eliminar', methods=['POST'])
def eliminar_comentario(comentario_id):
    """Eliminar un comentario."""
    comentario = Comentario.query.get_or_404(comentario_id)
    habitacion_id = comentario.habitacion_id
    
    try:
        db.session.delete(comentario)
        db.session.commit()
        flash('Comentario eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar comentario: {str(e)}', 'error')
    
    return redirect(url_for('main.detalle_habitacion', habitacion_id=habitacion_id))
