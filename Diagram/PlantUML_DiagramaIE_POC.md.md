@startuml
!theme plain

title Diagrama de Entidades - Sistema Multi-Agente

' Entidades principales
entity "Mensaje" as msg {
  * id : string <<PK>>
  --
  fuente : string
  contenido : text
  timestamp : datetime
}

entity "Solicitud" as sol {
  * request_id : string <<PK>>
  --
  canal : string
  texto_original : text
  estado : string
  fecha_creacion : datetime
}

entity "Intención" as int {
  * id : string <<PK>>
  * solicitud_id : string <<FK>>
  --
  tipo_intención : string
  idioma : string
  contexto : string
}

entity "Entidades_Extraídas" as ent {
  * id : string <<PK>>
  * solicitud_id : string <<FK>>
  --
  producto : string
  cantidad : integer
  unidad : string
  cliente : string
  dirección : string
  fecha_entrega : date
  hora_entrega : time
}

entity "Validación" as val {
  * id : string <<PK>>
  * entidades_id : string <<FK>>
  --
  stock_disponible : boolean
  ventana_válida : boolean
  dirección_válida : boolean
  tiempo_suficiente : boolean
  estado : string
  confianza : float
}

entity "Payload_RPA" as pay {
  * id : string <<PK>>
  * solicitud_id : string <<FK>>
  --
  order_id : string
  source : string
  customer_data : json
  items : json
  delivery_info : json
  validations : json
}

entity "Producto" as prod {
  * product_id : string <<PK>>
  --
  nombre : string
  stock : integer
  unidad : string
}

entity "Regla_Negocio" as reg {
  * rule_id : string <<PK>>
  --
  tipo : string
  parámetros : json
  activa : boolean
}

entity "Confirmación" as conf {
  * id : string <<PK>>
  * order_id : string <<FK>>
  --
  estado : string
  mensaje : text
  fecha : datetime
}

' Relaciones
msg ||--|| sol : "genera"
sol ||--|| int : "produce"
sol ||--|| ent : "extrae"
ent ||--|| val : "valida"
sol ||--|| pay : "crea"
pay ||--|| conf : "genera"

val }o--|| prod : "consulta"
val }o--|| reg : "verifica"

@enduml