# AKGC System Design Diagrams

## 1. Deployment Architecture - PlantUML

```plantuml
@startuml AKGC_Deployment
!define RECTANGLE class

node "Client Layer" {
    [Web Application] as WebApp
    [Mobile App] as MobileApp
    [CLI Tool] as CLI
}

node "Load Balancer" {
    [Nginx/HAProxy] as LB
}

node "Application Layer" {
    node "AKGC Instance 1" {
        [API Server 1] as API1
        [Standard Mode 1] as Std1
        [Ultra Mode 1] as Ultra1
    }
    
    node "AKGC Instance 2" {
        [API Server 2] as API2
        [Standard Mode 2] as Std2
        [Ultra Mode 2] as Ultra2
    }
}

node "Cache Layer" {
    database "Redis Cluster" as Redis {
        [Entity Cache]
        [Model Cache]
        [Session Cache]
    }
}

node "External Services" {
    cloud "Wikipedia API" as Wiki
    cloud "Monitoring" as Monitor
}

node "Storage Layer" {
    database "PostgreSQL" as DB {
        [Logs]
        [Metrics]
        [Configurations]
    }
}

' Connections
WebApp --> LB
MobileApp --> LB
CLI --> LB

LB --> API1
LB --> API2

API1 --> Std1
API1 --> Ultra1
API2 --> Std2
API2 --> Ultra2

Std1 --> Redis
Std2 --> Redis
Ultra1 --> Redis
Ultra2 --> Redis

Std1 --> Wiki
Std2 --> Wiki

API1 --> DB
API2 --> DB

API1 --> Monitor
API2 --> Monitor

@enduml
```

## 2. Deployment Architecture - Mermaid

```mermaid
graph TB
    subgraph "Client Layer"
        WebApp[Web Application]
        Mobile[Mobile App]
        CLI[CLI Tool]
    end
    
    subgraph "Load Balancer"
        LB[Nginx/HAProxy]
    end
    
    subgraph "Application Layer"
        subgraph "Instance 1"
            API1[API Server 1]
            Std1[Standard Mode 1]
            Ultra1[Ultra Mode 1]
        end
        
        subgraph "Instance 2"
            API2[API Server 2]
            Std2[Standard Mode 2]
            Ultra2[Ultra Mode 2]
        end
    end
    
    subgraph "Cache Layer"
        Redis[(Redis Cluster)]
    end
    
    subgraph "External Services"
        Wiki[Wikipedia API]
        Monitor[Monitoring Service]
    end
    
    subgraph "Storage Layer"
        DB[(PostgreSQL)]
    end
    
    WebApp --> LB
    Mobile --> LB
    CLI --> LB
    
    LB --> API1
    LB --> API2
    
    API1 --> Std1
    API1 --> Ultra1
    API2 --> Std2
    API2 --> Ultra2
    
    Std1 --> Redis
    Std2 --> Redis
    Ultra1 --> Redis
    Ultra2 --> Redis
    
    Std1 --> Wiki
    Std2 --> Wiki
    
    API1 --> DB
    API2 --> DB
    
    API1 --> Monitor
    API2 --> Monitor
    
    style LB fill:#e74c3c,color:#fff
    style Redis fill:#f39c12,color:#fff
    style DB fill:#3498db,color:#fff
```

## 3. Data Flow Architecture - Mermaid

```mermaid
graph LR
    subgraph "Input"
        User[User Request]
    end
    
    subgraph "Processing Pipeline"
        API[API Gateway]
        Router[Request Router]
        
        subgraph "Standard Path"
            Extract[Entity Extraction]
            Analyze[Semantic Analysis]
            KG[KG Lookup]
            HVI[HVI Calculation]
            Correct1[Correction]
        end
        
        subgraph "Ultra Path"
            Pattern[Pattern Match]
            Cache[Cache Lookup]
            Correct2[Fast Correction]
        end
        
        Metrics[Metrics Collection]
    end
    
    subgraph "Output"
        Response[API Response]
    end
    
    User --> API
    API --> Router
    
    Router -->|Standard| Extract
    Router -->|Ultra| Pattern
    
    Extract --> Analyze
    Analyze --> KG
    KG --> HVI
    HVI --> Correct1
    
    Pattern --> Cache
    Cache --> Correct2
    
    Correct1 --> Metrics
    Correct2 --> Metrics
    
    Metrics --> Response
    Response --> User
    
    style API fill:#e74c3c,color:#fff
    style Router fill:#f39c12,color:#fff
    style Metrics fill:#3498db,color:#fff
```

## 4. Component Interaction - Mermaid

```mermaid
graph TD
    subgraph "API Layer"
        REST[REST API Endpoints]
    end
    
    subgraph "Business Logic"
        Standard[Standard Mode Handler]
        Ultra[Ultra Mode Handler]
        Validator[Input Validator]
    end
    
    subgraph "Core Services"
        Entity[Entity Service]
        Semantic[Semantic Service]
        KG[Knowledge Graph Service]
        Correction[Correction Service]
    end
    
    subgraph "Data Access"
        Cache[Cache Manager]
        Wiki[Wikipedia Client]
        DB[Database Client]
    end
    
    subgraph "Infrastructure"
        Config[Configuration]
        Logger[Logging]
        Monitor[Monitoring]
    end
    
    REST --> Validator
    Validator --> Standard
    Validator --> Ultra
    
    Standard --> Entity
    Standard --> Semantic
    Standard --> KG
    Standard --> Correction
    
    Ultra --> Cache
    Ultra --> Correction
    
    Entity --> Cache
    Semantic --> Cache
    KG --> Wiki
    KG --> Cache
    
    Standard --> Logger
    Ultra --> Logger
    Standard --> Monitor
    Ultra --> Monitor
    
    Config --> Standard
    Config --> Ultra
    
    style REST fill:#e74c3c,color:#fff
    style Standard fill:#3498db,color:#fff
    style Ultra fill:#2ecc71,color:#fff
```

## 5. Scalability Architecture - Mermaid

```mermaid
graph TB
    subgraph "Horizontal Scaling"
        LB[Load Balancer]
        
        subgraph "Auto-Scaling Group"
            API1[AKGC Instance 1]
            API2[AKGC Instance 2]
            API3[AKGC Instance 3]
            APIN[AKGC Instance N]
        end
    end
    
    subgraph "Caching Layer"
        Redis1[(Redis Master)]
        Redis2[(Redis Replica 1)]
        Redis3[(Redis Replica 2)]
    end
    
    subgraph "Database Layer"
        DBMaster[(DB Master)]
        DBReplica[(DB Replica)]
    end
    
    subgraph "Monitoring"
        Metrics[Metrics Collector]
        Alerts[Alert Manager]
        Dashboard[Dashboard]
    end
    
    LB --> API1
    LB --> API2
    LB --> API3
    LB --> APIN
    
    API1 --> Redis1
    API2 --> Redis1
    API3 --> Redis1
    APIN --> Redis1
    
    Redis1 --> Redis2
    Redis1 --> Redis3
    
    API1 --> DBMaster
    API2 --> DBMaster
    DBMaster --> DBReplica
    
    API1 --> Metrics
    API2 --> Metrics
    Metrics --> Alerts
    Metrics --> Dashboard
    
    style LB fill:#e74c3c,color:#fff
    style Redis1 fill:#f39c12,color:#fff
    style DBMaster fill:#3498db,color:#fff
```
