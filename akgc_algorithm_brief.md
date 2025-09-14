# Adaptive Knowledge-Guided Correction (AKGC)

## Purpose  

The **Adaptive Knowledge-Guided Correction (AKGC)** algorithm detects and corrects factual hallucinations in Large Language Models (LLMs) **in real-time**.  
Unlike heavy graph neural network approaches (e.g., KGCN by Kang et al., 2024), AKGC is **lightweight, general-purpose, and optimized for 4GB VRAM hardware**.  
It introduces a **Hallucination Vulnerability Index (HVI)** for calibrated detection and uses dynamic knowledge graphs (KG) for efficient correction.

## Pipeline Overview  

### 1. Input  

- User query or prompt `P`  
- Initial LLM-generated response `O`  

### 2. Entity Extraction  

- Extract entities from both `P` and `O` using NER.  
- Example:  
  - `P`: *"What is the capital of France?"*  
  - `O`: *"The capital of France is Florida."*  
  - Extracted entities: `France`, `Florida`  

### 3. Knowledge Graph Retrieval  

- Retrieve related facts for extracted entities from a **local, cached KG** (Wikipedia/Wikidata snapshot).  
- Use FAISS/HNSW indexing for sub-50 ms retrieval.  
- Example fact: `France – hasCapital – Paris`  

### 4. Contextual Similarity Check  

- Compute embeddings for `P` and `O` using **DistilBERT**.  
- Calculate **cosine similarity** → `S_context`.  
- Low similarity → potential hallucination.  

### 5. Knowledge Alignment Check  

- Compute embeddings for `O` and retrieved facts `F(E)`.  
- Calculate **cosine similarity** → `S_kg`.  
- Low alignment → response contradicts KG.  

### 6. Hallucination Vulnerability Index (HVI)

- Compute hallucination risk score:  
HVI = α × S_context + (1 – α) × S_kg
- α ≈ 0.6 (calibrated on dev set)  
- HVI ∈ [0,1]  

- Threshold τ:  
- `HVI ≥ τ` → reliable  
- `HVI < τ` → hallucination suspected  

### 7. Decision Policy

- **Pass-through:** if `HVI ≥ τ`, return `O`.  
- **Refuse:** if `HVI < τ` but no reliable KG fact, output:  
*"I cannot verify this information with high confidence."*  
- **Correct:** if `HVI < τ` and KG fact exists, regenerate:  

Example fact-injection prompt

```bash
Question: What is the capital of France?
Retrieved Fact: The capital of France is Paris.
Please provide a corrected response.
```

### 8. Output  

- Final response `O*` (pass, refuse, or corrected).  
- Log metadata:  
- HVI score  
- Decision taken  
- KG facts used  

## Efficiency Optimizations  

- Mixed precision (`torch.cuda.amp`) → reduce VRAM usage.  
- KG pruning → keep KG ≤ 500 MB for stability.  
- Caching → avoid repeated network calls.  
- Single-pass correction → latency <300 ms (p50).  

## Evaluation Strategy  

- **Detection:** AUROC, AUPRC, calibration error of HVI vs baselines.  
- **Correction:** FactScore, human-annotated factual accuracy.  
- **Latency & Memory:** Benchmark p50/p95 on 4GB GPU.  
- **Generalization:** Evaluate across complaints, science, geography, history.  

## Novelty vs KGCN  

- **Lightweight:** DistilBERT + FAISS instead of GCN layers.  
- **Calibrated risk metric:** HVI provides interpretability.  
- **Latency-bounded:** Designed for <300 ms response on consumer GPUs.  
- **Structured policy:** Outputs *pass/refuse/correct* instead of opaque ranking.  
- **Multi-domain:** Not restricted to complaints; supports open-domain QA.  
