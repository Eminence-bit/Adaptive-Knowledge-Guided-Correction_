# Pre-Commit Checklist

## ✅ Files to Commit

### Core Source Code
- `src/akgc_simple_fast.py` - Standard AKGC implementation
- `src/akgc_ultra_optimized.py` - Ultra-optimized AKGC
- `src/api_server.py` - API server
- `src/benchmark_evaluation.py` - Benchmark testing
- `src/download_halueval.py` - HaluEval dataset downloader
- `src/preprocess_external_dataset.py` - External dataset preprocessor
- `src/test_external_dataset.py` - External dataset testing
- `src/visualize_akgc_vs_kgcn.py` - AKGC vs KGCN comparison visualization

### Documentation
- `README.md` - Main project documentation
- `BENCHMARK_RESULTS_GUIDE.md` - Benchmark results guide
- `EXTERNAL_DATASET_GUIDE.md` - External dataset testing guide
- `HALUEVAL_TESTING_GUIDE.md` - HaluEval testing guide
- `LICENSE` - Project license
- `requirements.txt` - Python dependencies

### Configuration & Scripts
- `.gitignore` - Git ignore rules
- `deploy.sh` - Deployment script
- `test_halueval.bat` - Windows batch script for HaluEval testing

### Paper & Results
- `Paper_for_AKGC.pdf` - Research paper
- `paper_benchmark_section.tex` - LaTeX benchmark section
- `results/benchmark/benchmark_results.json` - Core benchmark data
- `results/benchmark/akgc_vs_kgcn_comparison.png` - Main comparison chart
- `results/benchmark/akgc_vs_kgcn_comparison.pdf` - PDF version
- `results/benchmark/benchmark_table.tex` - LaTeX table
- `results/benchmark/domain_performance.png` - Domain performance chart
- `results/benchmark/domain_performance.pdf` - PDF version

## ❌ Files NOT to Commit (Already in .gitignore)

### Virtual Environment
- `.venv/` - Python virtual environment (large, user-specific)

### Large Data Files
- `data/halueval/*.json` - HaluEval dataset files (can be downloaded)
- `models/cache/` - Model cache files (regenerated)

### Test Results
- `results/external/*.json` - Large external test result files
- `results/external/*.md` - External test reports
- `src/__pycache__/` - Python cache files

### Temporary Files
- `*.pyc` - Compiled Python files
- `__pycache__/` - Python cache directories
- `*.log` - Log files

## 📋 Pre-Commit Actions

1. **Review Changes**
   ```bash
   git status
   git diff
   ```

2. **Stage Files**
   ```bash
   git add src/
   git add *.md
   git add requirements.txt
   git add results/benchmark/
   git add Paper_for_AKGC.pdf
   git add paper_benchmark_section.tex
   git add deploy.sh
   git add test_halueval.bat
   ```

3. **Verify Staged Files**
   ```bash
   git status
   ```

4. **Commit**
   ```bash
   git commit -m "Add AKGC implementation with comprehensive benchmarks and external dataset testing"
   ```

## 📊 Summary

**Total Files to Commit:** ~20 essential files
**Excluded:** Large data files, test results, virtual environment, cache files

**Key Features:**
- Complete AKGC implementation (Standard + Ultra-optimized)
- Comprehensive benchmark comparison with KGCN
- External dataset testing framework (HaluEval)
- Visualization tools for performance comparison
- Complete documentation and guides
