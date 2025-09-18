## 🧾 **Requerimientos del Sistema de Reservas Hoteleras**

---

### 1. Registro de Hoteles

* **Rol**: Administrador del sistema
* **Tarea**: Registrar un nuevo hotel
* **Formato**: Formulario de ingreso de datos
* **Requerimiento**:

  > El sistema debe permitir registrar un nuevo hotel con los campos: nombre, dirección, teléfono, correo electrónico, ubicación geográfica, descripción de servicios (como restaurante, piscina, gimnasio), y galería de fotos.

---

### 2. Gestión de Ofertas y Promociones

* **Rol**: Administrador del hotel
* **Tarea**: Configurar ofertas especiales
* **Formato**: Panel de administración de promociones
* **Requerimiento**:

  > El sistema debe permitir al hotel crear, modificar y eliminar promociones o paquetes especiales según temporada, incluyendo descuentos, servicios adicionales (estacionamiento, coworking) y vigencia de la oferta.

---

### 3. Gestión de Habitaciones

* **Rol**: Administrador del hotel
* **Tarea**: Registrar habitaciones del hotel
* **Formato**: Formulario de habitación
* **Requerimientos**:

  > El sistema debe permitir registrar habitaciones con los campos: tipo, descripción, precio, servicios incluidos, capacidad máxima y galería de fotos.
  > El sistema debe asociar un calendario de disponibilidad individual a cada habitación.
  > El sistema debe permitir establecer el estado de cada habitación como activa o inactiva (por mantenimiento, remodelación, limpieza, etc.), impidiendo reservas durante la inactividad.

---

### 4. Gestión de Estados del Hotel

* **Rol**: Administrador del sistema
* **Tarea**: Establecer estado del hotel
* **Formato**: Panel de control del hotel
* **Requerimiento**:

  > El sistema debe permitir definir el estado de un hotel como activo o inactivo (por reformas u otras razones), permitiendo reservas únicamente cuando el hotel esté en estado activo.

---

### 5. Políticas de Pago y Cancelación

* **Rol**: Administrador del hotel
* **Tarea**: Configurar políticas de pago y cancelación
* **Formato**: Panel de políticas por hotel o tipo de habitación
* **Requerimientos**:

  > El sistema debe permitir establecer diferentes políticas de pago (pago completo anticipado o pago al llegar) por hotel.
  > El sistema debe permitir configurar políticas de cancelación específicas por tipo de habitación y temporada.
  > El sistema debe gestionar automáticamente reembolsos o penalidades de acuerdo con la política configurada.

---

### 6. Tarifación Dinámica

* **Rol**: Administrador del hotel
* **Tarea**: Definir precios según condiciones
* **Formato**: Módulo de gestión de tarifas
* **Requerimientos**:

  > El sistema debe permitir establecer precios variables por habitación en función de la temporada, la cantidad de personas (hasta la capacidad máxima), y el calendario de ocupación.
  > El sistema debe soportar calendarios personalizados de temporada alta y baja por hotel y también permitir usar un calendario regional común.

---

### 7. Gestión de Calendarios

* **Rol**: Sistema
* **Tarea**: Visualizar disponibilidad
* **Formato**: Vista de calendario por habitación
* **Requerimiento**:

  > El sistema debe mostrar un calendario detallado por habitación que indique fechas reservadas y disponibles, actualizado en tiempo real tras cada reserva o cancelación.

---

### 8. Registro de Clientes

* **Rol**: Cliente
* **Tarea**: Registrarse en la plataforma
* **Formato**: Formulario de registro de cliente
* **Requerimiento**:

  > El sistema debe permitir registrar clientes con los campos: nombre completo, número de teléfono, correo electrónico y dirección.

---

### 9. Búsqueda de Habitaciones

* **Rol**: Cliente
* **Tarea**: Buscar habitaciones según criterios
* **Formato**: Barra de búsqueda avanzada
* **Requerimiento**:

  > El sistema debe permitir a los clientes buscar habitaciones usando uno o varios filtros: fechas de estadía, ubicación, calificación, precio y servicios.

---

### 10. Detalle de la Habitación

* **Rol**: Cliente
* **Tarea**: Consultar detalles de una habitación
* **Formato**: Ficha de habitación
* **Requerimiento**:

  > El sistema debe mostrar al cliente una ficha con la descripción completa de la habitación, servicios incluidos, fotos, comentarios de huéspedes y calificación promedio.

---

### 11. Reserva y Pago

* **Rol**: Cliente
* **Tarea**: Realizar una reserva y pago
* **Formato**: Proceso guiado paso a paso
* **Requerimientos**:

  > El sistema debe permitir a un cliente confirmar la reserva de una habitación seleccionada.
  > El sistema debe procesar el pago conforme a la política establecida por el hotel.
  > El sistema debe formalizar la reserva únicamente cuando el pago esté confirmado.

---

### 12. Calificaciones y Comentarios

* **Rol**: Cliente
* **Tarea**: Calificar y comentar después de la estadía
* **Formato**: Formulario de evaluación post-estadía
* **Requerimientos**:

  > El sistema debe permitir que los clientes califiquen su experiencia después de la estadía y dejen comentarios.
  > El sistema debe calcular una calificación promedio para cada habitación individual y otra para el hotel en general.
  > El sistema debe mostrar las calificaciones y comentarios a futuros clientes como parte de la ficha de cada habitación y hotel.

---

## 🧭 Consideraciones Adicionales

* **Trazabilidad**: Cada requerimiento debe rastrearse al entrevistado que lo propuso (Luciana o Felipe), para facilitar validaciones futuras.
* **Modificabilidad**: El sistema debe permitir actualizar o eliminar la información de hoteles, habitaciones, promociones y clientes conforme a políticas administrativas.
* **Verificabilidad**: Cada requerimiento tiene un resultado visible o una acción comprobable en el sistema, permitiendo pruebas unitarias y de aceptación.

