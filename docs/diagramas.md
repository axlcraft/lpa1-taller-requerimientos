# Diagrama de Clases

```mermaid

classDiagram
    class Hotel {
        +UUID id
        +String nombre
        +String direccion
        +String telefono
        +String correo
        +String ubicacionGeografica
        +String descripcionServicios
        +EstadoHotel estado
    }

    class Habitacion {
        +UUID id
        +TipoHabitacion tipo
        +String descripcion
        +Decimal precioBase
        +Integer capacidad
        +EstadoHabitacion estado
    }

    class Cliente {
        +UUID id
        +String nombreCompleto
        +String telefono
        +String correo
        +String direccion
    }

    class Reserva {
        +UUID id
        +Date fechaInicio
        +Date fechaFin
        +EstadoReserva estado
        +Decimal total
        +Date fechaReserva
        +Integer cantidadPersonas
    }

    class TransaccionPago {
        +UUID id
        +TipoPago tipo
        +Decimal monto
        +Date fechaPago
        +EstadoPago estado
    }

    class PoliticaDeCancelacion {
        +UUID id
        +String nombre
        +String descripcion
        +Decimal penalidad
        +Integer diasAnticipacionReembolso
    }

    class PoliticaDePago {
        +UUID id
        +TipoPago tipo
        +String descripcion
    }

    class Temporada {
        +UUID id
        +String nombre
        +Date fechaInicio
        +Date fechaFin
        +TipoTemporada tipo
    }

    class Promocion {
        +UUID id
        +String nombre
        +String descripcion
        +Decimal descuento
        +List~String~ serviciosAdicionales
        +Date fechaInicio
        +Date fechaFin
    }

    class Comentario {
        +UUID id
        +String contenido
        +Date fecha
    }

    class Calificacion {
        +UUID id
        +Integer puntuacion
        +Date fecha
    }

    class Calendario {
        +UUID id
        +Date fecha
        +EstadoCalendario estado
    }

    class Foto {
        +UUID id
        +String url
        +String descripcion
    }

    %% Relaciones

    Hotel "1" --> "0..*" Habitacion
    Hotel "1" --> "0..*" Promocion
    Hotel "1" --> "1..*" PoliticaDePago
    Hotel "1" --> "0..*" PoliticaDeCancelacion
    Hotel "1" --> "0..*" Temporada
    Hotel "1" --> "0..*" Foto

    Habitacion "1" --> "0..*" Reserva
    Habitacion "1" --> "0..*" Calendario
    Habitacion "1" --> "0..*" Comentario
    Habitacion "1" --> "0..*" Calificacion
    Habitacion "1" --> "0..*" Foto
    Habitacion "1" --> "1" Hotel

    Cliente "1" --> "0..*" Reserva
    Cliente "1" --> "0..*" Comentario
    Cliente "1" --> "0..*" Calificacion

    Reserva "1" --> "1" Cliente
    Reserva "1" --> "1" Habitacion
    Reserva "1" --> "1" TransaccionPago
    Reserva "1" --> "1" PoliticaDeCancelacion

    Comentario "1" --> "1" Cliente
    Comentario "1" --> "1" Habitacion

    Calificacion "1" --> "1" Cliente
    Calificacion "1" --> "1" Habitacion

    Calendario "1" --> "1" Habitacion

```

