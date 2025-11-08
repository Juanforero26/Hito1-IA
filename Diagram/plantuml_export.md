@startuml
title Diagrama de Secuencia - App de Transporte tipo Uber

actor Pasajero
participant "App Móvil" as App
participant "Servidor Backend" as Backend
participant "Motor de Asignación de Conductores" as Matching
participant "Conductor"
participant "Pasarela de Pago" as Pago

== Solicitud de viaje ==
Pasajero -> App : Ingresa destino y solicita viaje
App -> Backend : Enviar solicitud de viaje (ubicación, destino)
Backend -> Matching : Buscar conductor disponible
Matching -> Conductor : Notificar solicitud de viaje
Conductor -> Matching : Aceptar o rechazar viaje
Matching -> Backend : Confirmar conductor asignado
Backend -> App : Enviar información del conductor y ETA
App -> Pasajero : Mostrar detalles del conductor y tiempo estimado

== Inicio del viaje ==
Conductor -> Backend : Confirmar inicio del viaje
Backend -> App : Actualizar estado del viaje a “En curso”
App -> Pasajero : Notificar que el viaje ha comenzado

== Finalización del viaje ==
Conductor -> Backend : Confirmar finalización del viaje
Backend -> App : Enviar tarifa calculada
App -> Pasajero : Mostrar costo del viaje

== Pago ==
App -> Pago : Solicitar cargo automático
Pago -> Backend : Confirmar pago exitoso
Backend -> App : Enviar recibo electrónico
App -> Pasajero : Mostrar confirmación de pago y opción de calificación
Pasajero -> Backend : Enviar calificación del conductor
Backend -> Conductor : Registrar calificación y cerrar viaje

@enduml