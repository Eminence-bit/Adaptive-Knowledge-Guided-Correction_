# Data Directory

This directory contains the datasets used for training and evaluation of the AKGC algorithm.

## Directory Structure

```
data/
├── halu_eval/              # HaluEval dataset (original)
│   ├── qa.json             # Question-Answering data (large file)
│   ├── dialogue.json       # Dialogue data (large file)
│   ├── general.json        # General data (large file)
│   └── summarization.json  # Summarization data (large file)
├── hotpotqa/               # HotpotQA dataset
│   ├── hotpot_dev.json     # Development set
│   └── hotpot_train_subset.json  # Training subset
├── custom/                 # Custom dataset
│   └── custom_dataset.json # Custom science/history data
├── samples/                # Sample datasets (for demo)
│   └── halu_eval_sample.json  # 100 samples from HaluEval
└── README.md               # This file
```

## File Sizes

- **HaluEval dataset**: ~245MB (large files, use Git LFS)
- **HotpotQA dataset**: Small files
- **Custom dataset**: Small files
- **Sample datasets**: Small files for demonstration

## Usage

### For Development
Use the sample files in `data/samples/` for development and testing:
```bash
python src/test_realworld_prompts.py
```

### For Full Evaluation
Download the full datasets and place them in the appropriate directories:
```bash
# Full HaluEval dataset (245MB)
# Place qa.json, dialogue.json, general.json, summarization.json in data/halu_eval/

# Run full evaluation
python src/comprehensive_evaluation.py --datasets halu_eval --max_samples 1000
```

## Dataset Sources

- **HaluEval**: [HaluEval: A Large-Scale Hallucination Evaluation Benchmark](https://github.com/RUCAIBox/HaluEval)
- **HotpotQA**: [HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering](https://hotpotqa.github.io/)
- **Custom**: Generated science and history questions for domain-specific testing

## Notes

- Large files (>100MB) are stored using Git LFS
- Sample files are included for demonstration purposes
- Full datasets need to be downloaded separately due to size constraints
- All datasets are in JSON format with standardized structure

## Data Format

Each dataset follows this structure:
```json
[
  {
    "prompt": "Question or statement",
    "ground_truth": "Correct answer",
    "answer": "Model response",
    "is_hallucination": true/false
  }
]
```
