# Base de Datos - Sistema de Reservas Hoteleras

## Descripción
Este proyecto utiliza SQLAlchemy como ORM y SQLite como base de datos por defecto para desarrollo. La estructura está preparada para funcionar con PostgreSQL u otras bases de datos SQL en producción.

## Configuración de Base de Datos

### SQLite (Desarrollo - Por defecto)
```
SQLALCHEMY_DATABASE_URI = sqlite:///instance/hotel_reservas.db
```

### PostgreSQL (Producción)
```bash
# Configurar variable de entorno
export DATABASE_URL="postgresql://usuario:contraseña@host:puerto/nombre_db"
```

### MySQL (Opcional)
```bash
export DATABASE_URL="mysql://usuario:contraseña@host:puerto/nombre_db"
```

## Inicialización de la Base de Datos

### Comandos Disponibles

```bash
# Crear tablas sin datos
python init_db.py

# Crear tablas con datos de ejemplo
python init_db.py --with-sample-data

# Recrear base de datos (elimina datos existentes)
python init_db.py --drop --with-sample-data
```

### Datos de Ejemplo Incluidos

Al usar `--with-sample-data`, se crearán:

**Hoteles (3):**
- Hotel Paradise (Cancún, México)
- Mountain View Resort (Bariloche, Argentina)
- City Business Hotel (Centro de la Ciudad)

**Habitaciones (45):**
- 15 habitaciones por hotel
- 3 tipos: Simple, Doble, Suite
- 5 habitaciones de cada tipo por hotel

**Clientes (3):**
- Juan Pérez
- María García
- Carlos López

## Estructura de la Base de Datos

### Tablas Principales

1. **hoteles** - Información de hoteles
2. **habitaciones** - Habitaciones por hotel
3. **clientes** - Clientes registrados
4. **reservas** - Reservas realizadas
5. **comentarios** - Comentarios de clientes
6. **calificaciones** - Calificaciones de habitaciones
7. **fotos** - Imágenes de hoteles/habitaciones
8. **promociones** - Promociones por hotel
9. **politicas_pago** - Políticas de pago
10. **politicas_cancelacion** - Políticas de cancelación
11. **temporadas** - Temporadas y precios especiales
12. **calendarios** - Disponibilidad de habitaciones
13. **transacciones_pago** - Transacciones de pago

### Relaciones Principales

- Hotel 1:N Habitaciones
- Hotel 1:N Promociones  
- Cliente 1:N Reservas
- Habitacion 1:N Reservas
- Habitacion 1:N Comentarios
- Habitacion 1:N Calificaciones

## Uso en Código

```python
from app import create_app
from app.extensions import db
from app.models import Hotel, Habitacion, Cliente, Reserva

app = create_app()

with app.app_context():
    # Obtener todos los hoteles activos
    hoteles = Hotel.query.filter_by(estado='activo').all()
    
    # Buscar habitaciones disponibles
    habitaciones = Habitacion.query.filter_by(estado='activa').all()
    
    # Crear nueva reserva
    reserva = Reserva(
        cliente_id="uuid-del-cliente",
        habitacion_id="uuid-de-la-habitacion",
        fecha_inicio="2024-01-15",
        fecha_fin="2024-01-20"
    )
    db.session.add(reserva)
    db.session.commit()
```

## Variables de Entorno

```bash
# Configuración de la aplicación
FLASK_ENV=development          # development, production, testing
FLASK_DEBUG=True              # True/False
DATABASE_URL=sqlite:///app.db  # URL de conexión a BD
SECRET_KEY=tu-clave-secreta    # Clave secreta para sesiones

# Para desarrollo local
DEV_DATABASE_URL=sqlite:///instance/hotel_reservas.db
```

## Comandos Útiles

```bash
# Verificar estructura de tablas
python -c "from app import create_app; from app.extensions import db; app = create_app(); app.app_context().push(); print([table.name for table in db.metadata.tables.values()])"

# Contar registros
python -c "from app import create_app; from app.extensions import db; from app.models import Hotel; app = create_app(); app.app_context().push(); print(f'Hoteles: {Hotel.query.count()}')"

# Backup de base de datos SQLite
cp instance/hotel_reservas.db backups/backup_$(date +%Y%m%d_%H%M%S).db
```

## Migración de Base de Datos

Para cambios en el esquema de la base de datos, se recomienda usar Flask-Migrate:

```bash
# Instalar Flask-Migrate
pip install Flask-Migrate

# Inicializar migraciones
flask db init

# Crear migración
flask db migrate -m "Descripción del cambio"

# Aplicar migración
flask db upgrade
```

## Troubleshooting

### Error: "unable to open database file"
- Verificar que el directorio `instance` existe
- Verificar permisos de escritura
- Usar ruta absoluta si es necesario

### Error: "no such table"
- Ejecutar `python init_db.py` para crear tablas
- Verificar que los modelos estén importados correctamente

### Error: "FOREIGN KEY constraint failed"
- Verificar que los IDs referenciados existen
- Revisar el orden de inserción de datos