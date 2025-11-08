@startuml
!theme plain
skinparam backgroundColor #FEFEFE
skinparam sequenceMessageAlign center

actor Pasajero
participant "App Pasajero" as AppP
participant "Backend API" as API
participant "Sistema de\nReglas de Negocio" as Rules
participant "Base de Datos" as DB
participant "Servicio de\nPagos" as Payment
participant "App Conductor" as AppC
actor Conductor

== Solicitud de Cancelación ==
Pasajero -> AppP: Presiona "Cancelar viaje"
AppP -> AppP: Mostrar razones de cancelación
Pasajero -> AppP: Selecciona razón:\n"Cambio de planes"
AppP -> API: Solicitar cancelación de viaje\n(tripId: 12345, reason: "Cambio de planes")

API -> DB: Obtener estado del viaje
DB --> API: Estado: "Conductor en camino"\nTiempo transcurrido: 3 minutos

API -> Rules: Validar políticas de cancelación
Rules -> Rules: Verificar tiempo desde aceptación
Rules -> Rules: Calcular cargo por cancelación

alt Cancelación sin cargo (< 2 minutos)
    Rules --> API: Sin cargo por cancelación
    API -> DB: Actualizar estado a "Cancelado"
    API -> DB: Registrar cancelación sin penalización
    
else Cancelación con cargo (> 2 minutos)
    Rules --> API: Cargo por cancelación: $3.000
    API -> Payment: Procesar cargo de cancelación
    Payment -> Payment: Verificar método de pago
    
    alt Pago exitoso
        Payment --> API: Cargo exitoso
        API -> DB: Actualizar estado a "Cancelado"
        API -> DB: Registrar transacción de cancelación
        
    else Pago fallido
        Payment --> API: Error en el pago
        API --> AppP: No se puede cancelar\n(Problema con método de pago)
        AppP --> Pasajero: Mostrar error y actualizar\nmétodo de pago
        note right: El proceso termina aquí\nsi el pago falla
    end
end

== Notificación al Conductor ==
API -> AppC: Notificar cancelación del viaje
AppC -> Conductor: Alerta: "El pasajero ha\ncancelado el viaje"

Conductor -> AppC: Ver detalles de cancelación
AppC -> API: Solicitar compensación por cancelación
API -> Rules: Calcular compensación para conductor
Rules -> Rules: Verificar distancia recorrida\ny tiempo invertido

alt Conductor cerca del punto de recogida (< 500m)
    Rules --> API: Compensación: $2.500
    API -> DB: Registrar compensación
    API -> Payment: Transferir compensación al conductor
    Payment --> API: Transferencia programada
    API --> AppC: Compensación aprobada: $2.500
    
else Conductor lejos del punto de recogida (> 500m)
    Rules --> API: Sin compensación
    API --> AppC: Sin compensación aplicable
end

AppC --> Conductor: Mostrar resultado

== Confirmación al Pasajero ==
API -> DB: Actualizar disponibilidad del conductor
DB --> API: Conductor disponible nuevamente

API --> AppP: Cancelación confirmada
AppP -> AppP: Generar resumen de cancelación

alt Hubo cargo
    AppP -> Pasajero: "Viaje cancelado\nCargo: $3.000\nPuedes solicitar otro viaje"
else Sin cargo
    AppP -> Pasajero: "Viaje cancelado\nSin cargos adicionales\nPuedes solicitar otro viaje"
end

note over Pasajero, Conductor
  El sistema registra la cancelación en el historial
  y puede afectar la calificación del usuario
  si cancela frecuentemente
end note

@enduml