# AKGC System Diagrams

This directory contains comprehensive PlantUML and Mermaid diagrams for the AKGC system architecture, design, and workflows.

## 📁 Diagram Files

> **🖼️ Quick Access**: See [DIAGRAM_INDEX.md](DIAGRAM_INDEX.md) for all rendered PNG images with previews!

### 1. [System Architecture](01_system_architecture.md)
- **PlantUML**: Complete system architecture with all components
- **Mermaid**: High-level architecture and context diagrams
- **C4 Context**: System context and boundaries

**Key Components**:
- API Server
- Standard Mode (100% accuracy, 40ms)
- Ultra-Optimized Mode (100% accuracy, 0.01ms)
- Knowledge Graph Manager
- Cache System
- External Services

### 2. [Use Case Diagrams](02_use_case.md)
- **PlantUML**: Actor interactions and use cases
- **Mermaid**: Use case relationships and flows
- **Detailed**: Text correction use case sequence

**Actors**:
- End User
- Developer
- Researcher
- System Administrator

**Use Cases**:
- Detect Hallucination
- Correct Text
- Batch Process
- Evaluate Quality
- Configure System
- Monitor Performance

### 3. [Sequence Diagrams](03_sequence.md)
- **Standard Mode Processing**: Complete flow with HVI calculation
- **Ultra-Optimized Mode**: Fast pattern-matching flow
- **Batch Processing**: Multiple text handling
- **API Interactions**: Request/response cycles

**Flows**:
- Entity extraction → Semantic analysis → KG lookup → HVI → Correction
- Pattern match → Cache lookup → Fast correction
- Batch processing with aggregation

### 4. [Activity Diagrams](04_activity.md)
- **Text Correction Flow**: Decision trees and processing paths
- **Knowledge Graph Update**: Cache management and Wikipedia queries
- **Batch Processing**: Loop and aggregation logic
- **HVI Calculation**: Component weighting and scoring

**Processes**:
- Mode selection (Standard vs Ultra)
- Cache hit/miss handling
- Threshold-based correction
- Metric computation

### 5. [Class Diagrams](05_class.md)
- **Core Classes**: AKGCBase, SimpleFastAKGC, UltraOptimizedAKGC
- **Component Classes**: EntityExtractor, SemanticAnalyzer, HVICalculator
- **Data Models**: Request/Response objects
- **Relationships**: Inheritance, composition, dependencies

**Key Classes**:
- `AKGCBase`: Base class with common functionality
- `SimpleFastAKGC`: Standard mode implementation
- `UltraOptimizedAKGC`: Ultra-fast mode implementation
- `KGManager`: Knowledge graph operations
- `APIServer`: REST API endpoints

### 6. [System Design](06_system_design.md)
- **Deployment Architecture**: Multi-instance setup with load balancing
- **Data Flow**: Request routing and processing pipeline
- **Component Interaction**: Service dependencies
- **Scalability**: Horizontal scaling and replication

**Infrastructure**:
- Load Balancer (Nginx/HAProxy)
- Application Instances (Auto-scaling)
- Cache Layer (Redis Cluster)
- Database (PostgreSQL with replication)
- Monitoring (Metrics and alerts)

## 🎨 Diagram Types

### PlantUML Diagrams
- **Format**: `.puml` code blocks
- **Rendering**: Use PlantUML server or local renderer
- **Best For**: Detailed technical documentation, papers

### Mermaid Diagrams
- **Format**: `.mermaid` code blocks
- **Rendering**: GitHub, GitLab, VS Code, online editors
- **Best For**: README files, web documentation, presentations

## 🔧 How to Use

### Viewing PlantUML Diagrams

**Option 1: Online Renderer**
```bash
# Copy PlantUML code and paste at:
http://www.plantuml.com/plantuml/uml/
```

**Option 2: VS Code Extension**
```bash
# Install PlantUML extension
code --install-extension jebbs.plantuml

# Preview: Alt+D (Windows/Linux) or Option+D (Mac)
```

**Option 3: Command Line**
```bash
# Install PlantUML
brew install plantuml  # Mac
apt-get install plantuml  # Linux

# Generate PNG
plantuml diagram.puml
```

### Viewing Mermaid Diagrams

**Option 1: GitHub/GitLab**
- Mermaid diagrams render automatically in markdown files

**Option 2: VS Code Extension**
```bash
# Install Mermaid extension
code --install-extension bierner.markdown-mermaid

# Preview: Ctrl+Shift+V (Windows/Linux) or Cmd+Shift+V (Mac)
```

**Option 3: Online Editor**
```bash
# Visit Mermaid Live Editor:
https://mermaid.live/
```

**Option 4: Command Line**
```bash
# Install Mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# Generate PNG
mmdc -i diagram.mmd -o diagram.png
```

## 📊 Diagram Overview

### System Architecture
```
┌─────────────────────────────────────────┐
│           AKGC System                   │
├─────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────────────┐   │
│  │   API    │  │  Processing      │   │
│  │  Server  │──│  Modes           │   │
│  └──────────┘  │  - Standard      │   │
│                │  - Ultra         │   │
│                └──────────────────┘   │
│  ┌──────────────────────────────────┐ │
│  │  Core Components                 │ │
│  │  - Entity Extractor              │ │
│  │  - Semantic Analyzer             │ │
│  │  - HVI Calculator                │ │
│  │  - Correction Engine             │ │
│  └──────────────────────────────────┘ │
│  ┌──────────────────────────────────┐ │
│  │  Knowledge Graph                 │ │
│  │  - Wikipedia API                 │ │
│  │  - Cache System (29+ entities)   │ │
│  │  - Fact Selector                 │ │
│  └──────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### Processing Flow
```
Input Text
    ↓
[Mode Selection]
    ↓
┌───────────────┬───────────────┐
│   Standard    │     Ultra     │
│   (40ms)      │   (0.01ms)    │
├───────────────┼───────────────┤
│ Extract       │ Pattern       │
│ Analyze       │ Match         │
│ KG Lookup     │ Cache         │
│ HVI Calc      │ Lookup        │
│ Correct       │ Fast Correct  │
└───────────────┴───────────────┘
    ↓
Corrected Text + Metrics
```

## 🎯 Key Metrics

### Performance Comparison

| Mode | Accuracy | Latency | Speedup vs KGCN |
|------|----------|---------|-----------------|
| **Standard** | 100% | 40.71ms | 5.2× |
| **Ultra** | 100% | 0.0098ms | 21,701× |
| KGCN (Baseline) | 84% | 212.86ms | 1.0× |

### Component Metrics

| Component | Avg Time | Cache Hit Rate |
|-----------|----------|----------------|
| Entity Extraction | ~5ms | N/A |
| Semantic Analysis | ~15ms | 95% (model) |
| KG Lookup | ~10ms | 80% (facts) |
| HVI Calculation | ~5ms | N/A |
| Correction | ~5ms | N/A |

## 📝 Diagram Conventions

### Colors
- 🔴 **Red (#e74c3c)**: API/External interfaces
- 🔵 **Blue (#3498db)**: Core processing components
- 🟢 **Green (#2ecc71)**: Knowledge graph/data
- 🟠 **Orange (#f39c12)**: Utilities/helpers

### Shapes
- **Rectangle**: Components/Services
- **Cylinder**: Databases/Storage
- **Cloud**: External services
- **Actor**: Users/Systems
- **Diamond**: Decision points

### Arrows
- **Solid**: Direct calls/dependencies
- **Dashed**: Include/extend relationships
- **Dotted**: Optional/conditional

## 🚀 Quick Start

1. **View in GitHub**: All Mermaid diagrams render automatically
2. **Export to PDF**: Use PlantUML or Mermaid CLI
3. **Customize**: Edit diagram code and regenerate
4. **Integrate**: Include in documentation or presentations

## 📚 Additional Resources

- [PlantUML Documentation](https://plantuml.com/)
- [Mermaid Documentation](https://mermaid-js.github.io/)
- [C4 Model](https://c4model.com/)
- [UML Diagrams](https://www.uml-diagrams.org/)

## 🤝 Contributing

To add or modify diagrams:

1. Create/edit diagram in appropriate file
2. Test rendering with PlantUML/Mermaid
3. Update this README if adding new diagrams
4. Submit pull request with description

---

**Last Updated**: November 20, 2025  
**Version**: 1.0  
**Status**: Complete ✅
