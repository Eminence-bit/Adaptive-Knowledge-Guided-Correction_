# AKGC Activity Diagrams

## 1. Text Correction Flow - PlantUML

```plantuml
@startuml AKGC_Activity_Flow
start

:Receive Input Text;

if (Mode Selection?) then (Standard)
    :Extract Entities;
    :Compute Embeddings;
    :Fetch KG Facts;
    
    if (Facts in Cache?) then (yes)
        :Retrieve from Cache;
    else (no)
        :Query Wikipedia API;
        :Extract Facts;
        :Cache Facts;
    endif
    
    :Calculate HVI;
    
    if (HVI < Threshold?) then (yes)
        :Select Best Fact;
        :Apply Correction;
    else (no)
        :Keep Original Text;
    endif
    
else (Ultra)
    :Pattern Match Text;
    
    if (Pattern Found?) then (yes)
        :Lookup Cache;
        :Apply Fast Correction;
    else (no)
        :Keep Original Text;
    endif
endif

:Compute Metrics;
:Return Response;

stop

@enduml
```

## 2. Knowledge Graph Update - PlantUML

```plantuml
@startuml KG_Update_Activity
start

:Receive Entity Request;

if (Entity in Cache?) then (yes)
    :Return Cached Facts;
    stop
else (no)
    :Search Wikipedia;
    
    if (Page Found?) then (yes)
        :Fetch Page Content;
        :Extract Facts;
        
        if (Facts Valid?) then (yes)
            :Store in Cache;
            :Return Facts;
        else (no)
            :Use Fallback Facts;
        endif
    else (no)
        :Try Alternative Search;
        
        if (Alternative Found?) then (yes)
            :Fetch Alternative;
            :Extract Facts;
            :Store in Cache;
        else (no)
            :Return Empty Facts;
        endif
    endif
endif

stop

@enduml
```

## 3. Text Correction Flow - Mermaid

```mermaid
flowchart TD
    Start([Start]) --> Input[Receive Input Text]
    Input --> ModeCheck{Mode Selection?}
    
    ModeCheck -->|Standard| Extract[Extract Entities]
    ModeCheck -->|Ultra| Pattern[Pattern Match Text]
    
    Extract --> Embed[Compute Embeddings]
    Embed --> FetchKG[Fetch KG Facts]
    FetchKG --> CacheCheck{Facts in Cache?}
    
    CacheCheck -->|Yes| GetCache[Retrieve from Cache]
    CacheCheck -->|No| QueryWiki[Query Wikipedia API]
    
    QueryWiki --> ExtractFacts[Extract Facts]
    ExtractFacts --> StoreFacts[Cache Facts]
    StoreFacts --> CalcHVI[Calculate HVI]
    GetCache --> CalcHVI
    
    CalcHVI --> HVICheck{HVI < Threshold?}
    HVICheck -->|Yes| SelectFact[Select Best Fact]
    HVICheck -->|No| KeepText1[Keep Original Text]
    
    SelectFact --> ApplyCorrection[Apply Correction]
    ApplyCorrection --> Metrics[Compute Metrics]
    KeepText1 --> Metrics
    
    Pattern --> PatternCheck{Pattern Found?}
    PatternCheck -->|Yes| LookupCache[Lookup Cache]
    PatternCheck -->|No| KeepText2[Keep Original Text]
    
    LookupCache --> FastCorrect[Apply Fast Correction]
    FastCorrect --> Metrics
    KeepText2 --> Metrics
    
    Metrics --> Return[Return Response]
    Return --> End([End])
    
    style Start fill:#2ecc71,color:#fff
    style End fill:#e74c3c,color:#fff
    style ModeCheck fill:#f39c12,color:#fff
    style HVICheck fill:#f39c12,color:#fff
    style PatternCheck fill:#f39c12,color:#fff
```

## 4. Batch Processing Flow - Mermaid

```mermaid
flowchart TD
    Start([Start Batch]) --> Input[Receive Text Array]
    Input --> Init[Initialize Results Array]
    Init --> Loop{More Texts?}
    
    Loop -->|Yes| GetText[Get Next Text]
    GetText --> Process[Process Text]
    Process --> AddResult[Add to Results]
    AddResult --> Loop
    
    Loop -->|No| Aggregate[Aggregate Metrics]
    Aggregate --> CalcStats[Calculate Statistics]
    CalcStats --> Format[Format Response]
    Format --> Return[Return Batch Results]
    Return --> End([End])
    
    style Start fill:#2ecc71,color:#fff
    style End fill:#e74c3c,color:#fff
    style Loop fill:#f39c12,color:#fff
```

## 5. HVI Calculation - Mermaid

```mermaid
flowchart TD
    Start([Start HVI Calculation]) --> GetEmbed[Get Text Embeddings]
    GetEmbed --> GetFacts[Get KG Facts]
    
    GetFacts --> CalcContext[Calculate Context Similarity]
    GetFacts --> CalcKG[Calculate KG Alignment]
    
    CalcContext --> Weight1[Weight × 0.6]
    CalcKG --> Weight2[Weight × 0.4]
    
    Weight1 --> Sum[Sum Components]
    Weight2 --> Sum
    
    Sum --> HVI[HVI Score]
    HVI --> Normalize[Normalize to 0-1]
    Normalize --> Return[Return HVI]
    Return --> End([End])
    
    style Start fill:#2ecc71,color:#fff
    style End fill:#e74c3c,color:#fff
    style HVI fill:#3498db,color:#fff
```
