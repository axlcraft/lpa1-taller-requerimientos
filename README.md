# Sistema de Agencia de Viajes

![commits](https://badgen.net/github/commits/UR-CC/lp2-taller1?icon=github) 
![last_commit](https://img.shields.io/github/last-commit/UR-CC/lp2-taller1)

- ver [badgen](https://badgen.net/) o [shields](https://shields.io/) para otros tipos de _badges_

## Autor

- [@estudiante](https://www.github.com/estudiante)

## Descripción del Proyecto

Este proyecto implementa un **Sistema de Gestión de Reservas para Hoteles** desarrollado en Flask. El sistema permite:

- **Gestión de Hoteles**: Registro, edición y administración de hoteles con estados activos/inactivos
- **Gestión de Habitaciones**: Creación y administración de habitaciones con diferentes tipos, precios y capacidades
- **Registro de Clientes**: Sistema de registro y gestión de clientes
- **Reservas**: Proceso completo de reservas con gestión de pagos y estados
- **Evaluaciones**: Sistema de comentarios y calificaciones por parte de los clientes
- **Búsqueda**: Funcionalidad de búsqueda avanzada con múltiples filtros

El sistema está diseñado siguiendo patrones de diseño modernos, utiliza SQLAlchemy para el manejo de la base de datos y Bootstrap para una interfaz responsive y atractiva.

## Documentación

Revisar la documentación en [`./docs`](./docs)

- [Requerimientos](./docs/requerimientos.md)
- [SRS: Software Requirements Specification](./docs/srs.md)

### Diseño

![Diagrama de Clases](./docs/diagramas.md)

### Tárifas

|destino|pasajes|silver|gold|platinum|
|:---|---:|---:|---:|---:|
|Aruba|418|134|167|191|
|Bahamas|423|112|183|202|
|Cancún|350|105|142|187|
|Hawaii|858|210|247|291|
|Jamaica|380|115|134|161|
|Madrid|496|190|230|270|
|Miami|334|122|151|183|
|Moscu|634|131|153|167|
|NewYork|495|104|112|210|
|Panamá|315|119|138|175|
|Paris|512|210|260|290|
|Rome|478|184|220|250|
|Seul|967|205|245|265|
|Sidney|1045|170|199|230|
|Taipei|912|220|245|298|
|Tokio|989|189|231|255|

## Instalación

Siga estos pasos para configurar y ejecutar el sistema de reservas hoteleras en su entorno local:

1. **Clonar el proyecto**
```bash
git clone https://github.com/UR-CC/lpa1-taller-requerimientos.git
cd lpa1-taller-requerimientos
```

2. **Crear y activar entorno virtual**

En Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

En macOS/Linux:
```bash
python -m venv venv
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno (opcional)**
```bash
# Para configuraciones personalizadas
set DATABASE_URL=sqlite:///hotel_reservas.db
set SECRET_KEY=tu-clave-secreta-segura
```
    
## Ejecución

Una vez completada la instalación, puede ejecutar el sistema siguiendo estos pasos:

1. **Asegúrese de que el entorno virtual esté activo**
```bash
# En Windows
venv\Scripts\activate

# En macOS/Linux
source venv/bin/activate
```

2. **Ejecutar la aplicación**
```bash
python app.py
```

3. **Acceder al sistema**

El sistema estará disponible en: http://localhost:5000

**Funcionalidades disponibles:**
- Página principal con búsqueda de habitaciones
- Gestión de hoteles (crear, editar, listar)
- Gestión de habitaciones por hotel
- Registro y gestión de clientes
- Sistema de reservas con procesamiento de pagos
- Sistema de evaluaciones y comentarios

**Nota:** La base de datos SQLite se crea automáticamente al iniciar la aplicación por primera vez.

