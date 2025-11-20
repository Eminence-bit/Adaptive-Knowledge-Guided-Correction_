# 📊 External Dataset Testing Guide

Complete guide for testing AKGC on external datasets downloaded from online sources.

## 🚀 Quick Start

### Step 1: Download a Dataset

Download any factual dataset from sources like:
- **Kaggle**: https://www.kaggle.com/datasets
- **HuggingFace**: https://huggingface.co/datasets
- **GitHub**: Various fact-checking datasets
- **Academic Sources**: FEVER, HaluEval, TruthfulQA, etc.

### Step 2: Preprocess the Dataset

```bash
python src/preprocess_external_dataset.py path/to/your/dataset.json
```

**Supported formats:**
- `.json` - JSON format
- `.jsonl` - JSON Lines format
- `.csv` - Comma-separated values
- `.tsv` - Tab-separated values
- `.txt` - Plain text (one statement per line)

### Step 3: Test with AKGC

**Standard Mode (100% accuracy):**
```bash
python src/test_external_dataset.py data/external/preprocessed_dataset.json
```

**Ultra-Optimized Mode (0.0ms latency):**
```bash
python src/test_external_dataset.py data/external/preprocessed_dataset.json --ultra
```

**Test Limited Cases:**
```bash
python src/test_external_dataset.py data/external/preprocessed_dataset.json --max-cases 50
```

## 📋 Dataset Format Requirements

### Minimum Requirements

Your dataset should have at least one of these fields:
- **Text/Prompt**: `text`, `prompt`, `statement`, `claim`, `sentence`, `question`, `input`
- **Label (optional)**: `label`, `ground_truth`, `answer`, `truth`, `correct`, `target`

### Example Formats

#### JSON Format
```json
[
  {
    "text": "The capital of France is London.",
    "ground_truth": "The capital of France is Paris.",
    "label": "incorrect"
  },
  {
    "claim": "Water boils at 100 degrees Celsius.",
    "answer": "Water boils at 100 degrees Celsius.",
    "label": "correct"
  }
]
```

#### JSONL Format
```jsonl
{"prompt": "The chemical symbol for gold is Ag.", "truth": "The chemical symbol for gold is Au."}
{"prompt": "World War II ended in 1945.", "truth": "World War II ended in 1945."}
```

#### CSV Format
```csv
id,statement,ground_truth,category
1,"The capital of France is London.","The capital of France is Paris.",geography
2,"Water is H2O.","Water is H2O.",science
```

#### Plain Text Format
```
The capital of France is London.
The chemical symbol for gold is Ag.
World War II ended in 1945.
```

## 🔧 Preprocessing Features

The preprocessor automatically:
- ✅ **Detects format** - Automatically identifies file format
- ✅ **Normalizes fields** - Maps various field names to standard format
- ✅ **Cleans text** - Removes extra whitespace and special characters
- ✅ **Validates data** - Filters invalid or malformed entries
- ✅ **Categorizes by domain** - Automatically sorts into 6 domains
- ✅ **Generates statistics** - Provides dataset overview

### Domain Categories

Data is automatically categorized into:
1. **Geography** - Capitals, countries, geographic features
2. **Science** - Chemistry, physics, biology facts
3. **History** - Historical events, dates, figures
4. **Technology** - Programming, computers, internet
5. **Medicine** - Health, anatomy, medical facts
6. **Astronomy** - Planets, space, celestial bodies
7. **General** - Uncategorized statements

## 📊 Output Files

### Preprocessed Data
- `data/external/preprocessed_dataset.json` - Main preprocessed file
- `data/external/preprocessed_geography.json` - Geography domain
- `data/external/preprocessed_science.json` - Science domain
- `data/external/preprocessed_history.json` - History domain
- (etc. for each domain)

### Test Results
- `results/external/external_test_<name>_<timestamp>.json` - Detailed results
- `results/external/external_test_report_<name>_<timestamp>.md` - Summary report

## 📈 Metrics Reported

### Performance Metrics
- **Average Processing Time** - Mean latency per case
- **Min/Max Time** - Fastest and slowest cases
- **Latency Compliance** - % of cases under 300ms target

### Accuracy Metrics (if ground truth available)
- **Accuracy** - Exact match accuracy
- **ROUGE-L** - Longest common subsequence similarity
- **BERTScore** - Semantic similarity score
- **High Accuracy Cases** - Cases with ≥80% accuracy

### Correction Statistics
- **Corrections Made** - Number of factual corrections
- **Correction Rate** - Percentage of cases corrected

## 🎯 Recommended Datasets

### Fact-Checking Datasets
1. **FEVER** (Fact Extraction and VERification)
   - 185K claims with evidence
   - Download: https://fever.ai/dataset/fever.html

2. **HaluEval**
   - LLM hallucination benchmark
   - Download: https://github.com/RUCAIBox/HaluEval

3. **TruthfulQA**
   - 817 questions testing truthfulness
   - Download: https://github.com/sylinrl/TruthfulQA

4. **LIAR Dataset**
   - 12.8K short statements with labels
   - Download: https://www.cs.ucsb.edu/~william/data/liar_dataset.zip

### Knowledge Base Datasets
1. **SimpleQuestions**
   - 108K questions with KB facts
   - Download: https://research.fb.com/downloads/babi/

2. **Natural Questions**
   - 307K questions from Google Search
   - Download: https://ai.google.com/research/NaturalQuestions

## 💡 Usage Examples

### Example 1: Test FEVER Dataset
```bash
# Download FEVER dataset
wget https://fever.ai/download/fever/train.jsonl

# Preprocess
python src/preprocess_external_dataset.py train.jsonl

# Test with standard AKGC
python src/test_external_dataset.py data/external/preprocessed_dataset.json

# Test with ultra-optimized AKGC
python src/test_external_dataset.py data/external/preprocessed_dataset.json --ultra
```

### Example 2: Test Custom CSV Dataset
```bash
# Preprocess your CSV
python src/preprocess_external_dataset.py my_facts.csv

# Test first 100 cases
python src/test_external_dataset.py data/external/preprocessed_dataset.json --max-cases 100
```

### Example 3: Test by Domain
```bash
# Preprocess with domain categorization
python src/preprocess_external_dataset.py dataset.json

# Test only science domain
python src/test_external_dataset.py data/external/preprocessed_science.json

# Test only geography domain
python src/test_external_dataset.py data/external/preprocessed_geography.json
```

## 🔍 Troubleshooting

### Issue: "No valid data after preprocessing"
**Solution**: Check your dataset format. Ensure it has text/prompt fields.

### Issue: "Unsupported format"
**Solution**: Convert your dataset to JSON, CSV, or TXT format.

### Issue: "File not found"
**Solution**: Verify the file path is correct and the file exists.

### Issue: "Memory error with large datasets"
**Solution**: Use `--max-cases` to test a subset first.

## 📝 Custom Dataset Creation

If you want to create your own test dataset:

```python
import json

# Create custom test cases
test_cases = [
    {
        "prompt": "Your factual statement here",
        "ground_truth": "The correct version",
        "category": "science"
    },
    # Add more cases...
]

# Save as JSON
with open('my_custom_dataset.json', 'w') as f:
    json.dump(test_cases, f, indent=2)

# Preprocess and test
# python src/preprocess_external_dataset.py my_custom_dataset.json
# python src/test_external_dataset.py data/external/preprocessed_dataset.json
```

## 🎓 Best Practices

1. **Start Small**: Test with `--max-cases 50` first to verify everything works
2. **Check Preprocessing**: Review the preprocessed files before testing
3. **Use Ground Truth**: Include ground truth labels for accuracy metrics
4. **Compare Modes**: Test both standard and ultra-optimized modes
5. **Review Reports**: Check the generated markdown reports for insights

## 📞 Support

If you encounter issues:
1. Check the preprocessing output for errors
2. Verify your dataset format matches the requirements
3. Review the generated statistics for data quality issues
4. Test with a small subset first using `--max-cases`

---

**Ready to test?** Download a dataset and run the preprocessing pipeline!
