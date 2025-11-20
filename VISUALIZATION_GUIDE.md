# AKGC Performance Visualization Guide

## 📊 Overview

This guide explains the performance comparison visualizations between AKGC and KGCN baseline systems.

## 🎨 Available Charts

### Chart 1: Accuracy Comparison
**File**: `results/benchmark/chart1_accuracy_comparison.png`

Shows accuracy comparison across all systems:
- KGCN Baseline: 84.0%
- RAG Baseline: 89.0%
- AKGC Standard: 100.0% ✨
- AKGC Ultra: 100.0% ✨

**Key Insight**: AKGC achieves perfect 100% accuracy, a +16% improvement over KGCN.

### Chart 2: Latency Comparison
**File**: `results/benchmark/chart2_latency_comparison.png`

Compares average processing latency (log scale):
- KGCN Baseline: 212.86ms
- RAG Baseline: 188.20ms
- AKGC Standard: 40.71ms
- AKGC Ultra: 0.0098ms ⚡

**Key Insight**: AKGC Ultra is 21,701× faster than KGCN baseline.

### Chart 3: Speedup Factor
**File**: `results/benchmark/chart3_speedup_factor.png`

Visualizes speedup relative to KGCN baseline:
- KGCN: 1.0× (baseline)
- RAG: 1.1×
- AKGC Standard: 5.2×
- AKGC Ultra: 21,701× 🚀

**Key Insight**: Dramatic performance improvements while maintaining accuracy.

### Chart 4: Accuracy vs Latency Trade-off
**File**: `results/benchmark/chart4_accuracy_vs_latency.png`

Scatter plot showing the relationship between accuracy and latency:
- AKGC systems are in the top-left corner (high accuracy, low latency)
- Baseline systems are in the bottom-right (lower accuracy, higher latency)

**Key Insight**: AKGC achieves the best of both worlds - highest accuracy AND lowest latency.

### Chart 5: Performance Improvement Summary
**File**: `results/benchmark/chart5_improvement_summary.png`

Bar chart showing improvements over KGCN baseline:

**AKGC Standard**:
- Accuracy Gain: +16.0%
- Latency Reduction: 80.9%

**AKGC Ultra**:
- Accuracy Gain: +16.0%
- Latency Reduction: 100.0%

**Key Insight**: Significant improvements in both accuracy and speed.

## 🔄 Generating Charts

To regenerate all comparison charts:

```bash
python src/visualize_akgc_vs_kgcn.py
```

This will create:
- 5 individual PNG charts (300 DPI)
- 5 individual PDF charts (publication-ready)
- Console output with performance summary

## 📁 Output Files

All charts are saved to `results/benchmark/`:

```
results/benchmark/
├── chart1_accuracy_comparison.png
├── chart1_accuracy_comparison.pdf
├── chart2_latency_comparison.png
├── chart2_latency_comparison.pdf
├── chart3_speedup_factor.png
├── chart3_speedup_factor.pdf
├── chart4_accuracy_vs_latency.png
├── chart4_accuracy_vs_latency.pdf
├── chart5_improvement_summary.png
├── chart5_improvement_summary.pdf
├── benchmark_results.json (raw data)
└── benchmark_table.tex (LaTeX table)
```

## 🎯 Key Metrics Summary

| Metric | KGCN | AKGC Standard | AKGC Ultra | Improvement |
|--------|------|---------------|------------|-------------|
| **Accuracy** | 84.0% | 100.0% | 100.0% | +16.0% |
| **Latency** | 212.86ms | 40.71ms | 0.0098ms | 80.9-100% |
| **Speedup** | 1.0× | 5.2× | 21,701× | Up to 21,701× |

## 📊 Chart Design Features

- **High Resolution**: 300 DPI for publication quality
- **Color Coded**: Consistent color scheme across all charts
  - Red: KGCN Baseline
  - Orange: RAG Baseline
  - Blue: AKGC Standard
  - Green: AKGC Ultra
- **Clear Labels**: Bold, readable text with value annotations
- **Grid Lines**: Subtle gridlines for easy reading
- **Professional Style**: Clean, modern design suitable for papers

## 🔧 Customization

To customize the charts, edit `src/visualize_akgc_vs_kgcn.py`:

```python
# Change colors
colors = ['#e74c3c', '#f39c12', '#3498db', '#2ecc71']

# Change figure size
fig = plt.figure(figsize=(10, 6))

# Change DPI
plt.savefig(output_path, dpi=300, bbox_inches='tight')
```

## 📝 Usage in Papers

These charts are designed for academic papers and presentations:

1. **PNG files**: Use in presentations and web documents
2. **PDF files**: Use in LaTeX papers for vector graphics
3. **High DPI**: Ensures quality when printed

### LaTeX Example

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{results/benchmark/chart1_accuracy_comparison.pdf}
  \caption{Accuracy comparison between AKGC and baseline systems}
  \label{fig:accuracy_comparison}
\end{figure}
```

## 🚀 Quick Reference

**Generate all charts**:
```bash
python src/visualize_akgc_vs_kgcn.py
```

**View results**:
```bash
# Windows
start results/benchmark/chart1_accuracy_comparison.png

# Linux/Mac
xdg-open results/benchmark/chart1_accuracy_comparison.png
```

**Check raw data**:
```bash
cat results/benchmark/benchmark_results.json
```

---

**Last Updated**: November 20, 2025
**Version**: 1.0
**Status**: Production Ready ✅
