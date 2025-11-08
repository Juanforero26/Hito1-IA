# pip install diagrams
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import ECS, Lambda
from diagrams.aws.database import RDS, Dynamodb, ElastiCache
from diagrams.aws.network import APIGateway, Route53
from diagrams.aws.storage import S3
from diagrams.aws.security import Cognito
from diagrams.aws.integration import SQS, SNS, Appsync, Eventbridge
from diagrams.aws.devtools import Codepipeline
from diagrams.aws.management import Cloudwatch
from diagrams.onprem.client import Users
from diagrams.onprem.network import Internet
from diagrams.generic.blank import Blank

with Diagram("Arquitectura App de Transporte - AWS", show=False, direction="TB"):

    # Capa de usuario
    passenger = Users("Pasajero\n(App Móvil)")
    driver = Users("Conductor\n(App Móvil)")
    internet = Internet("Internet")

    # DNS
    dns = Route53("Route 53")

    # Capa API Gateway y auth
    api_gateway = APIGateway("API Gateway\nREST")
    auth = Cognito("Autenticación")
    app_sync = Appsync("AppSync\n(WebSocket)")

    # Backend
    with Cluster("Backend de Aplicación"):
        trip_service = ECS("Gestión de Viajes")
        matching_service = ECS("Motor de\nAsignación")
        user_service = Lambda("Gestión de\nUsuarios")
        payment_service = ECS("Gestión de\nPagos")

    # Datos
    with Cluster("Capa de Datos"):
        user_db = RDS("RDS: Usuarios")
        trips_db = Dynamodb("DynamoDB: Viajes")
        cache = ElastiCache("Cache: Conductores\nDisponibles")
        storage = S3("S3: Multimedia")

    # Integraciones y eventos
    with Cluster("Integraciones"):
        event_bridge = Eventbridge("EventBridge")
        queue = SQS("SQS: Cola de\nEventos")
        notifier = SNS("SNS: Push\nNotifications")
    
    # Externos
    payment_gateway = APIGateway("Pasarela\nPago")
    monitoring = Cloudwatch("CloudWatch")

    # Flujo principal: Solicitud de viaje
    passenger >> internet >> dns >> api_gateway
    driver >> internet >> dns >> app_sync
    
    api_gateway >> Edge(label="Auth") >> auth
    auth >> api_gateway
    api_gateway >> Edge(label="Solicitud viaje") >> trip_service
    
    # Backend busca conductor
    trip_service >> Edge(label="Buscar conductor") >> matching_service
    matching_service >> cache
    matching_service >> Edge(label="Notificar") >> app_sync
    app_sync >> Edge(label="Aceptar/Rechazar") >> driver
    driver >> app_sync >> matching_service
    
    # Confirmación y actualización
    matching_service >> Edge(label="Conductor asignado") >> trip_service
    trip_service >> Edge(label="Info conductor") >> api_gateway >> passenger
    
    # Gestión de viaje
    trip_service >> trips_db
    trip_service >> Edge(label="Eventos") >> event_bridge
    event_bridge >> queue
    event_bridge >> notifier
    notifier >> [passenger, driver]
    
    # Inicio/Finalización de viaje
    driver >> app_sync >> trip_service
    trip_service >> Edge(label="Estado viaje") >> event_bridge
    
    # Pago
    trip_service >> Edge(label="Calcular tarifa") >> payment_service
    payment_service >> payment_gateway
    payment_service >> Edge(label="Confirmar pago") >> event_bridge
    payment_service >> notifier
    
    # Datos y almacenamiento
    user_service >> user_db
    trip_service >> storage
    matching_service >> cache
    
    # Monitoreo
    monitoring << [trip_service, matching_service, user_service, payment_service]
