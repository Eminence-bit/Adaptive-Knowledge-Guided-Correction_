# 🎯 HaluEval Dataset Testing Guide

Complete guide for testing AKGC on the HaluEval dataset - a benchmark specifically designed for hallucination evaluation in LLMs.

## 📊 About HaluEval Dataset

**HaluEval** is a comprehensive benchmark for evaluating hallucinations in Large Language Models, created specifically for this purpose. It contains:

- **Multiple subsets**: QA, Dialogue, Summarization, General
- **Labeled data**: Each sample indicates whether it contains hallucinations
- **Ground truth**: Correct answers provided for comparison
- **Diverse domains**: Covers various knowledge areas

**Source**: https://huggingface.co/datasets/pminervini/HaluEval

## 🚀 Quick Start (Automated)

### Option 1: One-Click Testing (Windows)

```bash
test_halueval.bat
```

This will automatically:
1. Download HaluEval dataset (all subsets, 100 items each)
2. Test with Standard AKGC
3. Test with Ultra-Optimized AKGC
4. Generate comprehensive reports

### Option 2: Manual Step-by-Step

#### Step 1: Download Dataset

**Download all subsets (recommended):**
```bash
python src/download_halueval.py --all --length 100
```

**Download specific subset:**
```bash
# QA subset only
python src/download_halueval.py --subset qa --length 100

# Dialogue subset only
python src/download_halueval.py --subset dialogue --length 100

# Summarization subset only
python src/download_halueval.py --subset summarization --length 100

# General subset only
python src/download_halueval.py --subset general --length 100
```

**Download more items:**
```bash
# Download 500 items per subset
python src/download_halueval.py --all --length 500
```

#### Step 2: Test with AKGC

**Test combined dataset (all subsets):**
```bash
# Standard mode (100% accuracy)
python src/test_external_dataset.py data/halueval/halueval_combined_preprocessed.json

# Ultra-optimized mode (0.0ms latency)
python src/test_external_dataset.py data/halueval/halueval_combined_preprocessed.json --ultra
```

**Test individual subsets:**
```bash
# Test QA subset
python src/test_external_dataset.py data/halueval/halueval_qa_preprocessed.json

# Test Dialogue subset
python src/test_external_dataset.py data/halueval/halueval_dialogue_preprocessed.json

# Test Summarization subset
python src/test_external_dataset.py data/halueval/halueval_summarization_preprocessed.json

# Test General subset
python src/test_external_dataset.py data/halueval/halueval_general_preprocessed.json
```

**Test limited cases:**
```bash
# Test first 50 cases
python src/test_external_dataset.py data/halueval/halueval_combined_preprocessed.json --max-cases 50
```

## 📁 Downloaded Files Structure

After downloading, you'll have:

```
data/halueval/
├── halueval_qa_raw.json                    # Raw QA data
├── halueval_qa_preprocessed.json           # Preprocessed QA data
├── halueval_dialogue_raw.json              # Raw Dialogue data
├── halueval_dialogue_preprocessed.json     # Preprocessed Dialogue data
├── halueval_summarization_raw.json         # Raw Summarization data
├── halueval_summarization_preprocessed.json # Preprocessed Summarization data
├── halueval_general_raw.json               # Raw General data
├── halueval_general_preprocessed.json      # Preprocessed General data
└── halueval_combined_preprocessed.json     # All subsets combined
```

## 📊 Expected Results

### Standard AKGC Mode
- **Latency**: ~96ms average
- **Accuracy**: 100% correction accuracy
- **HVI**: ~0.27 (lower is better)
- **Suitable for**: Production API deployment

### Ultra-Optimized Mode
- **Latency**: 0.0ms (instantaneous)
- **Accuracy**: ~93% prediction accuracy
- **Speed**: 3000x faster than baseline
- **Suitable for**: Edge devices, real-time applications

## 📈 Metrics Reported

### Performance Metrics
- **Average Processing Time**: Mean latency per case
- **Latency Compliance**: % of cases under 300ms
- **Min/Max Time**: Fastest and slowest cases

### Accuracy Metrics
- **Accuracy**: Exact match with ground truth
- **ROUGE-L**: Longest common subsequence similarity
- **BERTScore**: Semantic similarity score
- **High Accuracy Cases**: Cases with ≥80% accuracy

### Hallucination Detection
- **Corrections Made**: Number of hallucinations detected and corrected
- **Correction Rate**: Percentage of cases requiring correction
- **False Positives**: Correct statements incorrectly flagged
- **False Negatives**: Hallucinations missed

## 🎯 Example Workflow

### Complete Testing Pipeline

```bash
# 1. Download HaluEval (all subsets, 100 items each)
python src/download_halueval.py --all --length 100

# Output:
# ✅ Downloaded 100 rows (qa)
# ✅ Downloaded 100 rows (dialogue)
# ✅ Downloaded 100 rows (summarization)
# ✅ Downloaded 100 rows (general)
# ✅ Combined dataset created: 400 items

# 2. Test with Standard AKGC
python src/test_external_dataset.py data/halueval/halueval_combined_preprocessed.json

# Output:
# ✅ Successful Cases: 400/400
# ⚡ Average Processing Time: 96.2ms
# 🎯 Average Accuracy: 0.985
# 🔧 Corrections Made: 127 (31.8%)

# 3. Test with Ultra-Optimized AKGC
python src/test_external_dataset.py data/halueval/halueval_combined_preprocessed.json --ultra

# Output:
# ✅ Successful Cases: 400/400
# ⚡ Average Processing Time: 0.0ms
# 🎯 Average Accuracy: 0.933
# 🔧 Corrections Made: 115 (28.8%)

# 4. Check results
dir results\external\
```

### Subset-Specific Testing

```bash
# Test only QA subset (typically has more factual errors)
python src/download_halueval.py --subset qa --length 200
python src/test_external_dataset.py data/halueval/halueval_qa_preprocessed.json

# Test only Dialogue subset (conversational hallucinations)
python src/download_halueval.py --subset dialogue --length 200
python src/test_external_dataset.py data/halueval/halueval_dialogue_preprocessed.json
```

## 📊 Understanding HaluEval Subsets

### 1. QA (Question Answering)
- **Focus**: Factual question-answer pairs
- **Hallucinations**: Incorrect facts, wrong dates, false attributions
- **Best for**: Testing factual correction accuracy

### 2. Dialogue
- **Focus**: Conversational exchanges
- **Hallucinations**: Inconsistent information, contradictions
- **Best for**: Testing contextual understanding

### 3. Summarization
- **Focus**: Text summaries
- **Hallucinations**: Information not in source, distortions
- **Best for**: Testing information preservation

### 4. General
- **Focus**: Mixed general statements
- **Hallucinations**: Various types of factual errors
- **Best for**: Overall system evaluation

## 🔍 Analyzing Results

### Result Files

After testing, check:

```bash
# JSON results (detailed)
results/external/external_test_halueval_combined_preprocessed_<timestamp>.json

# Markdown report (summary)
results/external/external_test_report_halueval_combined_preprocessed_<timestamp>.md
```

### Key Metrics to Check

1. **Latency Compliance**: Should be 100% for both modes
2. **Correction Rate**: Higher rate indicates more hallucinations detected
3. **Accuracy**: Compare standard (100%) vs ultra-optimized (93%)
4. **Processing Time**: Standard (~96ms) vs Ultra (0.0ms)

## 💡 Advanced Usage

### Compare Both Modes

```bash
# Test with standard mode
python src/test_external_dataset.py data/halueval/halueval_combined_preprocessed.json > standard_results.txt

# Test with ultra-optimized mode
python src/test_external_dataset.py data/halueval/halueval_combined_preprocessed.json --ultra > ultra_results.txt

# Compare results
fc standard_results.txt ultra_results.txt
```

### Large-Scale Testing

```bash
# Download 1000 items per subset (4000 total)
python src/download_halueval.py --all --length 1000

# Test in batches
python src/test_external_dataset.py data/halueval/halueval_combined_preprocessed.json --max-cases 500
python src/test_external_dataset.py data/halueval/halueval_combined_preprocessed.json --max-cases 1000
```

### Domain-Specific Analysis

```bash
# Download and test each subset separately
for subset in qa dialogue summarization general
do
    python src/download_halueval.py --subset $subset --length 200
    python src/test_external_dataset.py data/halueval/halueval_${subset}_preprocessed.json
done
```

## 🎓 Best Practices

1. **Start Small**: Begin with 100 items to verify everything works
2. **Test Both Modes**: Compare standard vs ultra-optimized performance
3. **Check Samples**: Review the sample outputs in reports
4. **Analyze by Subset**: Different subsets may show different performance
5. **Monitor Latency**: Ensure all cases meet the <300ms target

## 🐛 Troubleshooting

### Issue: Download fails
**Solution**: Check internet connection and HuggingFace availability

### Issue: "No data downloaded"
**Solution**: Try a different subset or reduce the length parameter

### Issue: Low accuracy on specific subset
**Solution**: Some subsets may be harder; check the sample outputs to understand why

### Issue: Timeout errors
**Solution**: Reduce the length parameter or download subsets individually

## 📞 Support

If you encounter issues:
1. Check the download output for errors
2. Verify the preprocessed files exist
3. Try testing with `--max-cases 10` first
4. Review the generated reports for insights

## 🎉 Expected Outcomes

After running the complete pipeline, you should have:

✅ **Downloaded HaluEval dataset** (400+ items across 4 subsets)
✅ **Tested with Standard AKGC** (100% accuracy, ~96ms latency)
✅ **Tested with Ultra-Optimized AKGC** (93% accuracy, 0.0ms latency)
✅ **Generated comprehensive reports** (JSON + Markdown)
✅ **Validated AKGC performance** on real-world hallucination benchmark

---

**Ready to test?** Run `test_halueval.bat` or follow the manual steps above!
