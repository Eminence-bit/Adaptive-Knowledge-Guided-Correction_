# Tasks for AKGC Development

## 1. Literature Review and Benchmarking

- **Task 1.1**: Access and analyze the IEEE base paper ([https://ieeexplore.ieee.org/document/10322537](https://ieeexplore.ieee.org/document/10322537)) to extract exact accuracy metrics and datasets.
- **Task 1.2**: Review additional IEEE papers (e.g.,) for complementary methods.
- **Task 1.3**: Identify baseline metrics (target: accuracy >80%) and datasets (HaluEval, HotpotQA) for comparison.
- **Deliverable**: Updated literature review with IEEE-focused references.

## 2. Dataset Preparation

- **Task 2.1**: Download and preprocess HaluEval ([https://github.com/RUCAIBox/HaluEval](https://github.com/RUCAIBox/HaluEval)) for question answering, dialogue, and summarization tasks.
- **Task 2.2**: Download and preprocess a HotpotQA subset (~10,000 samples, [https://hotpotqa.github.io/](https://hotpotqa.github.io/)).
- **Task 2.3**: Generate a custom dataset (~1,000 samples) by prompting DistilGPT-2 and manually annotating hallucinations (domains: science, history).
- **Deliverable**: Preprocessed datasets in `data/` directory, JSON format.

## 3. Algorithm Development

- **Task 3.1**: Implement the AKGC algorithm (see `akgc_algorithm.py` from previous response) using DistilGPT-2 for contextual analysis.
- **Task 3.2**: Integrate dynamic KG updates via Wikipedia API ([https://api.wikipedia.org](https://api.wikipedia.org)) with caching for efficiency.
- **Task 3.3**: Develop the Hallucination Vulnerability Index (HVI) metric, combining context similarity and KG alignment.
- **Task 3.4**: Optimize for hardware (4GB VRAM) using mixed precision training (`torch.cuda.amp`) and batch processing (batch size ≤ 8).
- **Deliverable**: Functional `src/akgc_algorithm.py` script.

## 4. Evaluation

- **Task 4.1**: Implement evaluation scripts to compute accuracy, ROUGE-L, BERTScore, and HVI on HaluEval and HotpotQA.
- **Task 4.2**: Benchmark AKGC against the IEEE base paper’s accuracy (~80%), targeting >80%.
- **Task 4.3**: Conduct human annotation on a subset (~100 samples) to validate HVI.
- **Deliverable**: Evaluation script (`src/evaluate.py`) and results in `results/`.

## 5. Documentation and Paper Writing

- **Task 5.1**: Update the literature review to focus on IEEE sources, incorporating the base paper’s results.
- **Task 5.2**: Draft the research paper, including introduction, methodology (AKGC), experiments, and results.
- **Task 5.3**: Prepare for IEEE conference submission (e.g., ICASSP 2026, deadlines ~mid-2025).
- **Deliverable**: Draft paper in IEEE format, submission-ready.

## 6. Testing and Optimization

- **Task 6.1**: Test AKGC on diverse prompts to ensure robustness across domains.
- **Task 6.2**: Optimize latency (target: 30% reduction vs. base paper’s system) using caching and single-pass detection.
- **Task 6.3**: Debug memory usage to fit 4GB VRAM, using quantization if needed.
- **Deliverable**: Optimized, tested AKGC implementation.
