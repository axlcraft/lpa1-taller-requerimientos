# 📄 **Documento SRS – Sistema de Reservas Hoteleras**

---

## 1. Información General

### 1.1. Título del Proyecto

**Sistema de Gestión de Reservas para Hoteles**

### 1.2. Fecha del Documento

**12 de septiembre de 2025**

### 1.3. Autores

* Joaquín – Ingeniero de Sistemas
* Luciana – Administradora Turística
* Felipe – Asistente de Administración

### 1.4. Descripción General

Este documento especifica los requerimientos funcionales y no funcionales para el desarrollo de un sistema de gestión de reservas de hoteles. El sistema permitirá registrar hoteles, habitaciones, promociones, clientes, gestionar reservas, aplicar políticas de pago y cancelación, administrar calendarios, y ofrecer al cliente una experiencia de búsqueda, reserva y evaluación completa.

---

## 2. Alcance del Sistema

El sistema estará orientado a la administración de hoteles a nivel nacional e internacional, centralizando los procesos de registro de hoteles, habitaciones, gestión de reservas, políticas de cancelación y pagos, control de disponibilidad mediante calendarios, visualización de promociones, gestión de estados (activos/inactivos), reembolsos y evaluaciones por parte de los clientes. Permitirá a los usuarios buscar habitaciones disponibles por filtros como fechas, ubicación, precio y calificación.

---

## 3. Glosario de Términos

| Término             | Definición                                                                  |
| ------------------- | --------------------------------------------------------------------------- |
| Hotel Activo        | Hotel disponible para realizar reservas.                                    |
| Hotel Inactivo      | Hotel no disponible temporalmente por mantenimiento, reformas, etc.         |
| Temporada Alta/Baja | Períodos definidos por el hotel o región que afectan precios y promociones. |
| Reserva Formalizada | Reserva completada con éxito tras confirmación de pago.                     |
| Cliente             | Persona registrada en el sistema que puede buscar y reservar habitaciones.  |
| Comentario          | Opinión del cliente sobre su estadía, publicada tras la reserva.            |

---

## 4. Requerimientos Funcionales

### RF01 - Registro de Hoteles

> El sistema debe permitir registrar un nuevo hotel con nombre, dirección, teléfono, correo electrónico, ubicación geográfica, descripción de servicios y fotos.

### RF02 - Registro de Habitaciones

> El sistema debe permitir registrar habitaciones con tipo, descripción, precio, servicios, capacidad máxima y galería de fotos.

### RF03 - Calendario de Habitaciones

> El sistema debe asociar un calendario de disponibilidad a cada habitación, indicando fechas ocupadas y libres.

### RF04 - Gestión de Estados

> El sistema debe permitir cambiar el estado de hoteles y habitaciones a “activo” o “inactivo” para controlar la disponibilidad de reservas.

### RF05 - Gestión de Promociones

> El sistema debe permitir a los hoteles registrar, modificar y eliminar promociones según temporada, con vigencia y servicios incluidos.

### RF06 - Gestión de Políticas de Pago

> El sistema debe permitir configurar políticas de pago por hotel (pago anticipado o al llegar).

### RF07 - Gestión de Cancelaciones

> El sistema debe permitir configurar políticas de cancelación y aplicar penalidades o reembolsos según criterios definidos por cada hotel.

### RF08 - Registro de Clientes

> El sistema debe permitir registrar clientes con nombre completo, teléfono, correo electrónico y dirección.

### RF09 - Búsqueda de Habitaciones

> El sistema debe permitir al cliente buscar habitaciones usando filtros de fecha, ubicación, calificación y precio.

### RF10 - Visualización de Detalles

> El sistema debe mostrar los detalles de cada habitación: descripción, fotos, servicios incluidos, calificaciones y comentarios.

### RF11 - Proceso de Reserva

> El sistema debe permitir que un cliente seleccione una habitación y realice una reserva mediante confirmación de pago.

### RF12 - Calificaciones y Comentarios

> El sistema debe permitir que el cliente califique su experiencia y deje comentarios tras su estadía.

### RF13 - Cálculo de Calificaciones

> El sistema debe calcular y mostrar la calificación promedio por habitación y por hotel.

### RF14 - Tarifación Dinámica

> El sistema debe ajustar el precio de la habitación según la temporada y número de personas (sin superar la capacidad máxima).

### RF15 - Calendario Regional

> El sistema debe permitir que los hoteles se alineen opcionalmente a un calendario regional de temporadas altas y bajas.

---

## 5. Requerimientos No Funcionales

### RNF01 - Usabilidad

> El sistema debe contar con una interfaz intuitiva y accesible para clientes y administradores, cumpliendo estándares UX.

### RNF02 - Seguridad

> El sistema debe encriptar la información sensible de los clientes (ej. contraseñas y datos de pago) y cumplir con normas de protección de datos.

### RNF03 - Rendimiento

> El sistema debe permitir realizar búsquedas de habitaciones con tiempos de respuesta menores a 2 segundos bajo condiciones normales de carga.

### RNF04 - Disponibilidad

> El sistema debe estar disponible el 99.9% del tiempo, con tiempos de mantenimiento programado informados con 24 horas de anticipación.

### RNF05 - Escalabilidad

> El sistema debe permitir escalar horizontalmente para soportar múltiples hoteles en distintos países sin afectar el rendimiento.

### RNF06 - Mantenibilidad

> El código del sistema debe estar documentado y modularizado para facilitar futuras modificaciones o integraciones.

### RNF07 - Multilenguaje

> El sistema debe permitir cambiar el idioma entre español e inglés desde la interfaz del usuario.

---

## 6. Casos de Uso (Resumen)

| ID   | Nombre del Caso de Uso             | Actores       | Descripción                                               |
| ---- | ---------------------------------- | ------------- | --------------------------------------------------------- |
| CU01 | Registrar Hotel                    | Administrador | Permite dar de alta un nuevo hotel.                       |
| CU02 | Registrar Habitación               | Administrador | Registra habitaciones dentro de un hotel.                 |
| CU03 | Buscar Habitación                  | Cliente       | Permite encontrar habitaciones disponibles según filtros. |
| CU04 | Ver Detalles de Habitación         | Cliente       | Muestra información completa de una habitación.           |
| CU05 | Realizar Reserva                   | Cliente       | Permite reservar una habitación seleccionada.             |
| CU06 | Calificar Estancia                 | Cliente       | Envía una calificación y comentario tras el check-out.    |
| CU07 | Configurar Promociones             | Hotel         | Define descuentos y paquetes especiales.                  |
| CU08 | Establecer Política de Cancelación | Hotel         | Define condiciones de cancelación y reembolsos.           |

---

## 7. Supuestos y Dependencias

* Se supone que todos los hoteles tienen acceso a internet para gestionar sus datos.
* El sistema usará pasarelas de pago externas para procesar transacciones (ej. Stripe, PayPal).
* Se integrará con un sistema de autenticación para seguridad (OAuth o similar).
* Las temporadas altas y bajas pueden definirse tanto por el hotel como por una entidad turística regional.

---

## 8. Requisitos de Aprobación

* El sistema se considerará completo cuando:

  * El 100% de los requerimientos funcionales estén implementados y probados.
  * El sistema pase las pruebas de aceptación definidas por los usuarios (UAT).
  * Las funcionalidades estén desplegadas en ambiente productivo y documentadas.

