from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import ECS, Lambda
from diagrams.aws.database import RDS, Dynamodb, ElastiCache
from diagrams.aws.network import ELB, CloudFront, Route53
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.analytics import KinesisDataStreams
from diagrams.aws.mobile import Amplify
from diagrams.aws.security import Cognito
from diagrams.aws.storage import S3
from diagrams.aws.engagement import Pinpoint
from diagrams.onprem.client import Users

# Configuración del diagrama
graph_attr = {
    "fontsize": "14",
    "bgcolor": "white",
    "pad": "0.5"
}

with Diagram("Arquitectura App de Transporte - AWS", 
             show=False, 
             direction="TB",
             graph_attr=graph_attr):
    
    # Usuarios
    pasajeros = Users("Pasajeros\n(App Mobile)")
    conductores = Users("Conductores\n(App Mobile)")
    
    # DNS y CDN
    dns = Route53("Route 53")
    cdn = CloudFront("CloudFront")
    
    # Autenticación
    with Cluster("Autenticación"):
        auth = Cognito("Cognito\nUser Pools")
    
    # Load Balancer
    lb = ELB("Application\nLoad Balancer")
    
    # Capa de aplicación
    with Cluster("Capa de Aplicación"):
        with Cluster("APIs REST"):
            api_users = ECS("User Service\n(ECS)")
            api_trips = ECS("Trip Service\n(ECS)")
            api_payments = ECS("Payment Service\n(ECS)")
        
        with Cluster("Funciones Serverless"):
            lambda_notifications = Lambda("Notificaciones")
            lambda_pricing = Lambda("Cálculo\nde Tarifas")
            lambda_matching = Lambda("Emparejamiento\nde Viajes")
    
    # Colas y mensajería
    with Cluster("Mensajería Asíncrona"):
        queue_trips = SQS("Cola de\nViajes")
        queue_notifications = SQS("Cola de\nNotificaciones")
        topic_events = SNS("Eventos\ndel Sistema")
    
    # Streaming de datos en tiempo real
    kinesis = KinesisDataStreams("Kinesis\n(Ubicación\nTiempo Real)")
    
    # Capa de datos
    with Cluster("Capa de Datos"):
        # Base de datos relacional
        db_main = RDS("RDS PostgreSQL\n(Usuarios, Viajes,\nPagos)")
        
        # NoSQL para datos en tiempo real
        dynamodb_locations = Dynamodb("DynamoDB\n(Ubicaciones\nActivas)")
        
        # Cache
        cache = ElastiCache("ElastiCache\nRedis")
    
    # Almacenamiento
    s3 = S3("S3\n(Fotos, Documentos)")
    
    # Notificaciones push
    push_notifications = Pinpoint("Pinpoint\n(Push\nNotifications)")
    
    # Flujo de datos - Pasajeros
    pasajeros >> Edge(label="HTTPS") >> dns
    dns >> cdn >> lb
    
    # Flujo de datos - Conductores
    conductores >> Edge(label="HTTPS") >> dns
    
    # Autenticación
    lb >> auth
    
    # APIs
    lb >> api_users
    lb >> api_trips
    lb >> api_payments
    
    # Servicios a bases de datos
    api_users >> db_main
    api_users >> cache
    api_users >> s3
    
    api_trips >> db_main
    api_trips >> cache
    api_trips >> queue_trips
    api_trips >> kinesis
    
    api_payments >> db_main
    api_payments >> cache
    
    # Procesamiento de ubicaciones en tiempo real
    kinesis >> dynamodb_locations
    kinesis >> lambda_matching
    
    # Emparejamiento de viajes
    queue_trips >> lambda_matching
    lambda_matching >> dynamodb_locations
    lambda_matching >> topic_events
    
    # Cálculo de tarifas
    api_trips >> lambda_pricing
    lambda_pricing >> cache
    
    # Sistema de notificaciones
    topic_events >> queue_notifications
    queue_notifications >> lambda_notifications
    lambda_notifications >> push_notifications
    push_notifications >> Edge(label="Push") >> pasajeros
    push_notifications >> Edge(label="Push") >> conductores
    
    # Eventos del sistema
    topic_events >> Edge(label="subscribe") >> lambda_notifications

print("Diagrama generado exitosamente: arquitectura_app_de_transporte_aws.png")
print("\nComponentes principales:")
print("- Route 53: DNS management")
print("- CloudFront: CDN para contenido estático")
print("- Cognito: Autenticación de usuarios")
print("- ECS: Microservicios en contenedores")
print("- Lambda: Funciones serverless para lógica específica")
print("- RDS: Base de datos relacional para datos persistentes")
print("- DynamoDB: Base de datos NoSQL para ubicaciones en tiempo real")
print("- ElastiCache: Cache Redis para mejorar performance")
print("- Kinesis: Streaming de ubicaciones en tiempo real")
print("- SQS/SNS: Mensajería asíncrona y eventos")
print("- S3: Almacenamiento de archivos")
print("- Pinpoint: Notificaciones push móviles")