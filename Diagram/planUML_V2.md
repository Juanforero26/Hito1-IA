@startuml
!theme plain
skinparam backgroundColor #FEFEFE
skinparam sequenceMessageAlign center

actor Pasajero
participant "App Pasajero" as AppP
participant "Backend API" as API
participant "Sistema de\nTarifas" as Pricing
participant "Sistema de\nEmparejamiento" as Match
participant "Base de Datos" as DB
participant "Servicio de\nPagos" as Payment
participant "Servicio de\nNotificaciones" as Notify
participant "App Conductor" as AppC
actor Conductor

== Solicitud de Viaje ==
Pasajero -> AppP: Abre la aplicación
AppP -> API: Autenticar usuario
API -> DB: Verificar sesión activa
DB --> API: Usuario autenticado (id: 5678)
API --> AppP: Sesión válida

Pasajero -> AppP: Ingresa ubicación de recogida
AppP -> API: Validar dirección
API --> AppP: Dirección válida

Pasajero -> AppP: Ingresa destino
AppP -> API: Solicitar estimación
API -> Pricing: Calcular tarifa estimada\n(origen, destino, tipo de servicio)
Pricing -> Pricing: Calcular distancia: 8.5 km\nTiempo estimado: 22 min\nTarifa base + km + tiempo

Pricing --> API: Tarifa estimada: $18.500
API --> AppP: Mostrar estimación
AppP -> Pasajero: Tarifa: $18.500\nTiempo: 22 min

Pasajero -> AppP: Confirmar solicitud
AppP -> API: Crear solicitud de viaje\n(userId: 5678, origen, destino)
API -> DB: Guardar solicitud con estado "Buscando"
DB --> API: Viaje creado (tripId: 12345)

== Búsqueda y Asignación de Conductor ==
API -> Match: Buscar conductores disponibles\n(ubicación, radio: 5 km)
Match -> DB: Consultar conductores activos cercanos
DB --> Match: Lista: [Conductor A (1.2 km),\nConductor B (2.5 km), Conductor C (3.1 km)]

Match -> Match: Aplicar algoritmo de selección:\n- Distancia\n- Calificación\n- Tiempo sin viaje

Match --> API: Conductor seleccionado: Conductor A\n(driverId: 9012, distancia: 1.2 km, ETA: 4 min)

API -> DB: Asignar conductor al viaje
DB --> API: Asignación exitosa

API -> AppC: Notificar nueva solicitud de viaje
AppC -> Conductor: Alerta: Nuevo viaje disponible\n(Ganancia estimada: $16.000)

Conductor -> AppC: Aceptar viaje
AppC -> API: Confirmar aceptación (tripId: 12345)
API -> DB: Actualizar estado a "Aceptado"

== Confirmación al Pasajero ==
API -> DB: Obtener datos del conductor
DB --> API: Nombre: Juan Pérez\nCalificación: 4.8\nPlaca: ABC-123\nModelo: Chevrolet Spark 2020

API -> Notify: Enviar notificación de confirmación
Notify -> AppP: Push notification
AppP -> Pasajero: Conductor asignado!\nJuan Pérez - ⭐4.8\nPlaca: ABC-123\nLlega en 4 minutos

== Conductor en Camino ==
Conductor -> AppC: Iniciar navegación hacia recogida
AppC -> API: Actualizar ubicación cada 5 segundos
API -> DB: Guardar ubicación en tiempo real

loop Actualización en tiempo real
    API -> AppP: Enviar ubicación del conductor
    AppP -> Pasajero: Mostrar conductor en mapa\n(ETA actualizado)
end

Conductor -> AppC: Llegué al punto de recogida
AppC -> API: Notificar llegada
API -> DB: Actualizar estado a "En punto de recogida"
API -> Notify: Enviar notificación de llegada
Notify -> AppP: Push notification
AppP -> Pasajero: ¡Tu conductor ha llegado!

== Inicio del Viaje ==
Pasajero -> Pasajero: Abordar el vehículo
Conductor -> AppC: Verificar pasajero e iniciar viaje
AppC -> API: Cambiar estado a "En curso"\n(tripId: 12345, timestamp inicio)
API -> DB: Actualizar estado y hora de inicio
DB --> API: Estado actualizado

API -> AppP: Viaje iniciado
AppP -> Pasajero: Viaje en curso\nCompartir viaje en tiempo real

loop Durante el viaje
    AppC -> API: Enviar ubicación GPS
    API -> AppP: Actualizar ruta en mapa
end

== Finalización del Viaje ==
Conductor -> AppC: Llegar al destino
Conductor -> AppC: Finalizar viaje
AppC -> API: Completar viaje\n(tripId: 12345, timestamp fin)

API -> DB: Registrar finalización
API -> Pricing: Calcular tarifa final\n(distancia real: 8.7 km, tiempo real: 24 min)

Pricing -> Pricing: Tarifa base: $5.000\nPor km: $1.200 × 8.7 = $10.440\nPor tiempo: $150 × 24 = $3.600\nTotal: $19.040

Pricing --> API: Tarifa final: $19.040

== Procesamiento de Pago ==
API -> Payment: Procesar pago\n(userId: 5678, monto: $19.040)
Payment -> Payment: Cargo a tarjeta terminada en 4567

alt Pago exitoso
    Payment --> API: Transacción aprobada\n(transactionId: TXN-789)
    API -> DB: Registrar pago exitoso
    API -> DB: Calcular comisión de plataforma (25%)\nPago al conductor: $14.280
    
else Pago fallido
    Payment --> API: Pago rechazado
    API -> DB: Marcar pago pendiente
    API -> Notify: Notificar problema de pago
    Notify -> AppP: Actualiza tu método de pago
end

== Calificación y Cierre ==
API -> AppP: Viaje completado - Tarifa: $19.040
AppP -> Pasajero: Solicitar calificación del conductor

Pasajero -> AppP: Calificar conductor (5 estrellas)\nPropina: $2.000\nComentario: "Excelente servicio"

AppP -> API: Enviar calificación y propina
API -> DB: Guardar calificación del conductor
API -> DB: Procesar propina adicional

API -> Payment: Procesar propina ($2.000)
Payment --> API: Propina procesada

API -> AppC: Nueva calificación recibida
AppC -> Conductor: Calificación: ⭐⭐⭐⭐⭐\nPropina: $2.000\nGanancia total: $16.280

API -> DB: Liberar conductor (estado: Disponible)
API -> DB: Cerrar viaje completamente

AppP -> Pasajero: Gracias por viajar con nosotros!\nRecibo enviado al correo

note over Pasajero, Conductor
  Viaje completado exitosamente
  Duración: 24 minutos
  Distancia: 8.7 km
  Calificación: 5 estrellas
end note

@enduml