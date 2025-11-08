@startuml Componentes_Pedidos

!include <C4/C4_Component>

title Componentes - Servicio de Pedidos

Container_Boundary(pedidos, "Servicio de Pedidos") {
    
    Component(pedido_controller, "Pedido Controller", "TypeScript/NestJS", "Endpoints REST para CRUD de pedidos")
    
    Component(pedido_orchestrator, "Orquestador de Pedidos", "TypeScript", "Coordina flujo de creación y validación")
    
    Component(pedido_repository, "Pedido Repository", "TypeORM", "Acceso a datos de Pedido e ItemPedido")
    
    Component(state_machine, "Máquina de Estados", "TypeScript/XState", "Gestiona transiciones de estado del pedido")
    
    Component(validation_coordinator, "Coordinador de Validaciones", "TypeScript", "Orquesta validaciones síncronas y asíncronas")
    
    Component(alert_manager, "Gestor de Alertas", "TypeScript", "Genera y clasifica alertas")
    
    Component(event_publisher, "Publicador de Eventos", "TypeScript", "Emite eventos de dominio")
    
    Component(dto_mapper, "Mapper DTO", "TypeScript", "Mapea entidades a DTOs")
}

ComponentDb(postgres, "PostgreSQL", "Base de datos")
ComponentQueue(event_bus, "Event Bus", "RabbitMQ")

System_Ext(validacion_svc, "Servicio Validación")
System_Ext(notificacion_svc, "Servicio Notificaciones")
System_Ext(interpretacion_svc, "Servicio Interpretación")

' Flujo de creación
Rel(pedido_controller, dto_mapper, "Valida DTO", "DTO")
Rel(pedido_controller, pedido_orchestrator, "Crea pedido", "Command")
Rel(pedido_orchestrator, pedido_repository, "Persiste", "Entity")
Rel(pedido_repository, postgres, "INSERT", "SQL")

Rel(pedido_orchestrator, validation_coordinator, "Solicita validación", "PedidoId")
Rel(validation_coordinator, validacion_svc, "Valida", "HTTP")
Rel(validation_coordinator, alert_manager, "Resultado validación", "ValidationResult")

Rel(pedido_orchestrator, state_machine, "Transición de estado", "Event")
Rel(state_machine, pedido_repository, "Actualiza estado", "Entity")

Rel(pedido_orchestrator, event_publisher, "Publica evento", "DomainEvent")
Rel(event_publisher, event_bus, "Publica", "AMQP")
Rel(event_bus, notificacion_svc, "Consume", "Event")

' Flujo de consulta
Rel(pedido_controller, pedido_repository, "Consulta", "Query")
Rel(pedido_repository, dto_mapper, "Entity", "Mapping")
Rel(dto_mapper, pedido_controller, "DTO", "Response")

note right of state_machine
  **Estados del Pedido:**
  recibido → interpretado → 
  validado → requiere_revision →
  aprobado → enviado_produccion →
  completado
  
  Maneja transiciones válidas
  y restricciones
end note

note bottom of event_publisher
  **Eventos de Dominio:**
  - PedidoCreado
  - PedidoInterpretado
  - PedidoValidado
  - PedidoAprobado
  - PedidoRechazado
  - PedidoEnviado
end note

@enduml