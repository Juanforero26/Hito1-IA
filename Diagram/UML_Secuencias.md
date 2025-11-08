@startuml Flujo_Interpretacion_Pedido

title Flujo Completo - Interpretación y Validación de Pedido

actor Cliente
participant "WhatsApp API" as WA
participant "Webhook Handler" as WH
participant "Message Queue" as MQ
participant "Servicio\nInterpretación" as SI
participant "LLM Provider" as LLM
participant "Servicio\nNormalización" as SN
participant "Servicio\nPedidos" as SP
participant "PostgreSQL" as DB
participant "Servicio\nValidación" as SV
participant "Servicio\nNotificaciones" as SNOT
participant "Dashboard Web" as DASH
actor Empleado

== Fase 1: Recepción ==

Cliente -> WA: Envía mensaje:\n"Necesito 80 panes franceses\ny 5 docenas de pandebono\npara mañana a las 7am"
activate WA

WA -> WH: POST /webhook\n{message, from, timestamp}
activate WH

WH -> WH: Valida firma\nExtrae metadata
WH -> MQ: Publica mensaje\n{texto, canal, metadata}
activate MQ
WH --> WA: 200 OK
deactivate WH
deactivate WA

== Fase 2: Interpretación ==

MQ -> SI: Consume mensaje
activate SI

SI -> SI: Preprocesa texto:\n- Limpia caracteres\n- Normaliza espacios\n- Detecta idioma

SI -> LLM: POST /v1/chat/completions\nPrompt + texto
activate LLM
note right
  Prompt:
  "Extrae del siguiente pedido:
  - Productos mencionados
  - Cantidades
  - Fecha de entrega
  Responde en JSON estructurado"
end note

LLM --> SI: JSON:\n{\n  "productos": [...],\n  "fecha": "2025-11-06",\n  "hora": "07:00"\n}
deactivate LLM

loop Para cada producto extraído

  SI -> SN: POST /normalize\n{texto: "panes franceses"}
  activate SN
  
  SN -> DB: SELECT * FROM Producto\nWHERE 'panes franceses' % ANY(sinonimos)
  activate DB
  DB --> SN: [{id, nombre_estandar, codigo}]
  deactivate DB
  
  SN -> SN: Calcula similitud:\nsimilarity("panes franceses", "Pan Francés") = 0.92
  
  SN --> SI: {\n  producto_id: "uuid-123",\n  nombre_normalizado: "Pan Francés",\n  confianza: 0.92\n}
  deactivate SN
  
end

SI -> SI: Calcula confianza global:\npromedio ponderado = 0.89

SI -> SP: POST /pedidos\n{\n  texto_original,\n  entidades_extraidas,\n  confianza: 0.89\n}
activate SP

== Fase 3: Persistencia ==

SP -> SP: Crea entidad Pedido\nEstado: 'recibido'

SP -> DB: BEGIN TRANSACTION
activate DB

SP -> DB: INSERT INTO Pedido\n(texto_original, estado, ...)
DB --> SP: pedido_id

loop Para cada item extraído
  SP -> DB: INSERT INTO ItemPedido\n(pedido_id, texto_producto_original,\nproducto_id, cantidad, ...)
  DB --> SP: item_id
end

SP -> SP: Transición estado:\n'recibido' → 'interpretado'

SP -> DB: UPDATE Pedido\nSET estado='interpretado'
SP -> DB: COMMIT TRANSACTION
deactivate DB

SP --> SI: {pedido_id, status: "created"}
deactivate SI

== Fase 4: Validación ==

SP -> SV: POST /validate\n{pedido_id}
activate SV

SV -> DB: SELECT * FROM ItemPedido\nWHERE pedido_id = ?
activate DB
SV -> DB: SELECT * FROM Producto\nWHERE id IN (...)
DB --> SV: [items], [productos]
deactivate DB

SV -> SV: Valida stock:\nPan Francés: solicitado=80, stock=200 ✓

SV -> SV: Valida ventana entrega:\nFecha: 2025-11-06 (24h adelante) ✓\nHora: 07:00 (dentro de 6am-6pm) ✓

SV -> SV: Valida cantidades:\nPan: 80 (usual: 20-200) ✓\nPandebono: 60 (usual: 12-100) ✓

SV --> SP: {\n  valido: true,\n  validaciones: {...},\n  alertas: []\n}
deactivate SV

SP -> SP: Transición estado:\n'interpretado' → 'validado'

SP -> DB: UPDATE Pedido\nSET estado='validado',\nvalidaciones={...}
activate DB
deactivate DB

== Fase 5: Notificación ==

SP -> MQ: Publica evento:\nPedidoValidado {pedido_id}
activate MQ

MQ -> SNOT: Consume evento
activate SNOT

SNOT -> DB: SELECT * FROM Pedido\nWHERE id = ?
activate DB
DB --> SNOT: {pedido con items}
deactivate DB

SNOT -> SNOT: Genera mensaje:\n"✅ Pedido recibido:\n- Pan Francés: 80 uds\n- Pandebono: 60 uds\nEntrega: 06/11 a las 7:00am"

SNOT -> WA: POST /messages\n{to, message}
activate WA
WA -> Cliente: Confirmación
deactivate WA

SNOT -> MQ: ACK mensaje
deactivate MQ
deactivate SNOT

SP --> MQ: ACK
deactivate MQ

== Fase 6: Revisión Humana (si aplica) ==

alt Pedido requiere revisión
  
  SP -> DASH: WebSocket: NuevoPedidoAlerta\n{pedido_id}
  activate DASH
  
  DASH -> Empleado: Notificación push:\n"⚠️ Nuevo pedido requiere revisión"
  
  Empleado -> DASH: Abre pedido
  DASH -> SP: GET /pedidos/{id}
  SP -> DB: SELECT con JOIN
  activate DB
  DB --> SP: Pedido completo
  deactivate DB
  SP --> DASH: {pedido, items, alertas}
  
  DASH -> Empleado: Muestra dashboard:\n- Texto original\n- Interpretación\n- Alertas
  
  Empleado -> DASH: Click "Aprobar"
  DASH -> SP: PATCH /pedidos/{id}/aprobar
  
  SP -> SP: Transición:\n'validado' → 'aprobado'
  SP -> DB: UPDATE Pedido\nSET estado='aprobado'
  activate DB
  deactivate DB
  
  SP --> DASH: 200 OK
  deactivate DASH
  
end

deactivate SP

@enduml