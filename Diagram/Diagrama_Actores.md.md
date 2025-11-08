@startuml Jerarquia_Actores

title Jerarquía de Actores - Sistema de Reconocimiento de Pedidos

' Actores abstractos
actor "Cliente" as Cliente <<abstract>>
actor "Usuario\nInterno" as UsuarioInt <<abstract>>
actor "Sistema\nExterno" as SistExt <<abstract>>

' Clientes concretos
actor "Cliente\nRegistrado" as ClienteReg
actor "Cliente\nNo Registrado" as ClienteNoReg

' Usuarios internos
actor "Empleado\nPanadería" as Empleado
actor "Administrador\nSistema" as Admin

' Sistemas externos
actor "Sistema de\nDistribución" as SistDist
actor "Servicio de\nNotificaciones" as ServNotif
actor "API de\nWhatsApp" as WhatsAppAPI

' Actores de tiempo
actor "Scheduler" as Scheduler <<Timer>>

' Relaciones de generalización
ClienteReg -up-|> Cliente
ClienteNoReg -up-|> Cliente

Empleado -up-|> UsuarioInt
Admin -up-|> UsuarioInt

SistDist -up-|> SistExt
ServNotif -up-|> SistExt
WhatsAppAPI -up-|> SistExt

' Notas descriptivas
note right of ClienteReg
  **Características:**
  - ID único en sistema
  - Perfil completo
  - Historial de pedidos
  - Preferencias guardadas
  - Direcciones validadas
  --
  **Ventajas:**
  - Proceso más rápido
  - Menor validación
  - Autocompletado
  - Modificaciones simples
end note

note right of ClienteNoReg
  **Características:**
  - Sin ID en sistema
  - Primera interacción
  - Datos sin validar
  --
  **Limitaciones:**
  - Requiere datos completos
  - Validación exhaustiva
  - No puede modificar pedidos
  - No accede a historial
end note

note right of Empleado
  **Responsabilidades:**
  - Revisar pedidos con alertas
  - Corregir interpretaciones
  - Aprobar/rechazar pedidos
  - Registrar clientes nuevos
  - Dar soporte
end note

note right of Admin
  **Responsabilidades:**
  - Configurar catálogo
  - Gestionar reglas de negocio
  - Acceder a analytics
  - Administrar usuarios
  - Configurar integraciones
end note

note bottom of Scheduler
  **Tareas Programadas:**
  - Validación de stock (cada 1h)
  - Detección de anomalías
  - Recordatorios de entrega
  - Limpieza de datos temporales
end note

@enduml