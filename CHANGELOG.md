# Changelog

## Unreleased

- Centraliza las calificaciones en el blueprint `evaluaciones` y evita enviar calificaciones desde `reservas.detalle`.
- Agrega `estrellas_hotel`, `estrellas_habitacion` y `estrellas_atencion` como campos de `Calificacion` y armoniza rutas.
- UI: mejora visual de estrellas en páginas de detalle de hotel y habitación.
- Autenticación: registro de cliente con username/password y login para clientes.
- Superusuario: login separado para superuser; añadido `dev_login` para desarrollo (solo DEBUG).
- Rutas protegidas: `@admin_required` aplicado a editar/eliminar de hoteles y clientes.
- Tests: se agregaron tests pytest para validaciones de permisos y flujo de calificación.
- Scripts: `scripts/create_dev_superuser.py` para marcar/crear superuser de desarrollo.
