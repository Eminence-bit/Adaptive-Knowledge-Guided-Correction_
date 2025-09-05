# Project Planning for AKGC Development

## Timeline Overview

- **Duration**: 4–6 months (August 2025 – January 2026)
- **Goal**: Develop, evaluate, and document the AKGC framework for IEEE conference submission (e.g., ICASSP 2026, deadlines ~mid-2025).
- **Hardware**: Ryzen 7 5800 HS, RTX 3050 (4GB VRAM), 16GB RAM.

## Milestones and Timeline

### Month 1 (August 2025): Setup and Literature Review

- **Week 1–2**:
  - Set up development environment (Python, PyTorch, Transformers).
  - Clone repository and install dependencies (see `readme.md`).
  - Access IEEE base paper ([https://ieeexplore.ieee.org/document/10322537](https://ieeexplore.ieee.org/document/10322537)) for metrics.
- **Week 3–4**:
  - Review IEEE papers and finalize literature review.
  - Download and preprocess HaluEval and HotpotQA datasets.
- **Deliverable**: Environment setup, initial literature review, preprocessed datasets.

### Month 2–3 (September–October 2025): Algorithm Development

- **Week 5–8**:
  - Implement AKGC algorithm (contextual analysis with DistilGPT-2, KG integration).
  - Develop HVI metric (context similarity + KG alignment).
- **Week 9–12**:
  - Generate custom dataset (~1,000 samples).
  - Optimize algorithm for 4GB VRAM (mixed precision, batch size ≤ 8).
- **Deliverable**: Functional `akgc_algorithm.py`, custom dataset.

### Month 4 (November 2025): Evaluation and Testing

- **Week 13–16**:
  - Implement evaluation scripts for accuracy, ROUGE-L, BERTScore, and HVI.
  - Benchmark against base paper’s accuracy (~80%).
  - Conduct human annotation (~100 samples) for HVI validation.
  - Optimize latency (target: 30% reduction).
- **Deliverable**: Evaluation results, optimized implementation.

### Month 5–6 (December 2025 – January 2026): Paper Writing and Submission

- **Week 17–20**:
  - Draft IEEE paper (introduction, methodology, experiments, results).
  - Refine comparisons with base paper’s system.
- **Week 21–24**:
  - Finalize paper in IEEE format.
  - Submit to IEEE conference (e.g., ICASSP 2026 or TNNLS).
- **Deliverable**: Submission-ready paper.

## Risk Management

- **Risk**: Limited access to IEEE paper metrics/datasets.
  - **Mitigation**: Use HaluEval and HotpotQA as fallbacks; contact authors for clarification.
- **Risk**: Hardware constraints (4GB VRAM).
  - **Mitigation**: Use quantization, gradient checkpointing, and small batch sizes.
- **Risk**: Delays in dataset annotation.
  - **Mitigation**: Start with smaller custom dataset (~500 samples) if needed.

## Milestones

1. **End of Month 1**: Environment setup, datasets ready, initial literature review.
2. **End of Month 3**: AKGC algorithm implemented, custom dataset generated.
3. **End of Month 4**: Evaluation completed, results benchmarked.
4. **End of Month 6**: Paper submitted to IEEE conference.
