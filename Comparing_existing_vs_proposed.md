## Comparison: Existing vs Proposed System

| Feature / Aspect                    | Existing (KGCN - Kang et al., 2024)                                      | Proposed (AKGC)                                                       |
|------------------------------------|--------------------------------------------------------------------------|----------------------------------------------------------------------|
| **Primary Domain**                  | Complaint-specific tasks only                                            | Multi-domain (complaints, science, geography, history)                |
| **Architecture Type**               | 4-layer Knowledge Graph Convolutional Network (GCN)                      | DistilBERT-based semantic analysis + KG retrieval                     |
| **Knowledge Graph Design**          | Static ontology, domain-locked                                           | Dynamic, cached KG (Wikipedia/Wikidata snapshot), entity-pruned (~500MB) |
| **Hallucination Detection**          | Confidence-based ranking (implicit)                                      | Hallucination Vulnerability Index (HVI) — calibrated, interpretable   |
| **Correction Method**               | Multi-step iterative regeneration                                        | Single-pass fact-injection correction                                |
| **Output Style**                    | Single corrected output                                                  | Structured decision: Pass / Refuse / Correct                          |
| **Generalization Capability**       | Domain-specific, poor transfer                                           | Domain-general, scalable to diverse topics                           |
| **Latency (per 100 words)**         | ~37s on V100 GPU                                                          | <300ms p50 on 4GB GPU                                                 |
| **Hardware Requirements**           | High-end GPU (V100, >16GB VRAM)                                           | Consumer GPU (RTX 3050, 4GB VRAM)                                     |
| **Memory Usage**                     | High (multi-GB graph embeddings)                                         | ~500MB KG + DistilBERT embeddings                                     |
| **Reproducibility**                  | Requires heavy preprocessing & retraining                                | Plug-and-play, no retraining required                                |
| **Evaluation Scope**                 | Complaint datasets                                                       | HaluEval, HotpotQA, FEVER, TruthfulQA (multi-domain)                  |
| **Interpretability of Detection**   | Opaque (confidence scores only)                                          | Transparent risk score (HVI ∈ [0,1])                                  |
| **Deployment Readiness**             | Research prototype                                                       | Real-time ready (API + Docker)                                       |
