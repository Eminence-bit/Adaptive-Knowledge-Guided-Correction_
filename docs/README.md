# Adaptive Knowledge-Guided Correction (AKGC) for LLM Hallucination Detection and Correction

## Overview

This project develops the **Adaptive Knowledge-Guided Correction (AKGC)** framework to detect and correct hallucinations in Large Language Models (LLMs). Hallucinations—plausible but factually incorrect outputs—are a critical challenge in LLM reliability. AKGC integrates lightweight contextual analysis with dynamic knowledge graph (KG) updates to achieve real-time detection and correction, optimized for mid-range hardware (e.g., Ryzen 7 5800 HS, RTX 3050 with 4GB VRAM, 16GB RAM). The framework aims to surpass existing systems, such as those achieving ~80% detection accuracy, by improving accuracy and reducing latency. It introduces a novel **Hallucination Vulnerability Index (HVI)** metric and will be evaluated on HaluEval and HotpotQA datasets, targeting publication in IEEE conferences.

## Objectives

- Develop a lightweight, real-time hallucination detection and correction system.
- Surpass the accuracy benchmark (~80%) of existing systems
- Introduce HVI to quantify hallucination risk.
- Optimize for resource-constrained hardware.

## Setup Instructions

### Prerequisites

- **Hardware**: Ryzen 7 5800 HS, RTX 3050 (4GB VRAM), 16GB RAM or equivalent.
- **OS**: Ubuntu 20.04+ or Windows 10/11.
- **Software**: Python 3.8+, PyTorch 1.13+, Transformers (Hugging Face), Requests, SciPy, NumPy.

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-repo/akgc-llm-hallucination.git
   cd akgc-llm-hallucination
   ```

2. **Install Dependencies**:

   ```bash
   pip install torch==1.13.1 transformers==4.35.0 requests scipy numpy
   ```

3. **Download Datasets**:
   - HaluEval: [https://github.com/RUCAIBox/HaluEval](https://github.com/RUCAIBox/HaluEval)
   - HotpotQA: [https://hotpotqa.github.io/](https://hotpotqa.github.io/)
   - Place datasets in `data/` directory.
4. **Set Up Environment**:
   - Ensure CUDA 11.6+ for GPU support (RTX 3050).
   - Use mixed precision training for memory efficiency (`torch.cuda.amp`).

### Usage

1. **Run the AKGC Algorithm**:

   ```bash
   python src/akgc_algorithm.py --prompt "The capital of France is Florida." --output_dir results/
   ```

2. **Evaluate on Datasets**:

   ```bash
   python src/evaluate.py --dataset halu_eval --metrics accuracy hvi
   ```

3. **Generate Custom Dataset**:

   ```bash
   python src/generate_custom_dataset.py --prompts prompts.txt --output data/custom_dataset.json
   ```

## Project Structure

- `src/`: Core implementation (akgc_algorithm.py, evaluate.py, etc.).
- `data/`: Datasets (HaluEval, HotpotQA, custom).
- `results/`: Output metrics and corrected responses.
- `docs/`: Documentation (readme.md, tasks.md, planning.md).

## Contributing

- Follow the tasks outlined in `tasks.md`.
- Adhere to the timeline in `planning.md`.
- Submit pull requests with clear documentation.

## License

MIT License
