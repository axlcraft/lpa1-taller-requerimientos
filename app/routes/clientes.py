# app/routes/clientes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Cliente
from app.extensions import db

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/')
def listar():
    """Lista todos los clientes."""
    clientes = Cliente.query.all()
    return render_template('clientes/listar.html', clientes=clientes)

@clientes_bp.route('/registrar', methods=['GET', 'POST'])
def registrar():
    """Registrar un nuevo cliente."""
    if request.method == 'POST':
        try:
            # Validar que el email no exista
            if Cliente.query.filter_by(correo=request.form['correo']).first():
                flash('Ya existe un cliente con ese correo electrónico', 'error')
                return render_template('clientes/registrar.html')
            
            cliente = Cliente(
                nombre_completo=request.form['nombre_completo'],
                telefono=request.form.get('telefono'),
                correo=request.form['correo'],
                direccion=request.form.get('direccion')
            )
            
            db.session.add(cliente)
            db.session.commit()
            
            flash('Cliente registrado exitosamente', 'success')
            return redirect(url_for('clientes.listar'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar cliente: {str(e)}', 'error')
    
    return render_template('clientes/registrar.html')

@clientes_bp.route('/<cliente_id>')
def detalle(cliente_id):
    """Detalle de un cliente específico."""
    cliente = Cliente.query.get_or_404(cliente_id)
    return render_template('clientes/detalle.html', cliente=cliente)

@clientes_bp.route('/<cliente_id>/editar', methods=['GET', 'POST'])
def editar(cliente_id):
    """Editar un cliente existente."""
    cliente = Cliente.query.get_or_404(cliente_id)
    
    if request.method == 'POST':
        try:
            # Validar que el email no exista en otro cliente
            cliente_existente = Cliente.query.filter_by(correo=request.form['correo']).first()
            if cliente_existente and cliente_existente.id != cliente.id:
                flash('Ya existe otro cliente con ese correo electrónico', 'error')
                return render_template('clientes/editar.html', cliente=cliente)
            
            cliente.nombre_completo = request.form['nombre_completo']
            cliente.telefono = request.form.get('telefono')
            cliente.correo = request.form['correo']
            cliente.direccion = request.form.get('direccion')
            
            db.session.commit()
            flash('Cliente actualizado exitosamente', 'success')
            return redirect(url_for('clientes.detalle', cliente_id=cliente.id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar cliente: {str(e)}', 'error')
    
    return render_template('clientes/editar.html', cliente=cliente)

@clientes_bp.route('/<cliente_id>/eliminar', methods=['POST'])
def eliminar(cliente_id):
    """Eliminar un cliente."""
    cliente = Cliente.query.get_or_404(cliente_id)
    
    try:
        db.session.delete(cliente)
        db.session.commit()
        flash('Cliente eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar cliente: {str(e)}', 'error')
    
    return redirect(url_for('clientes.listar'))
