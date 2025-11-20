"""
Visualize AKGC vs KGCN Performance Comparison
Generates comprehensive comparative charts between AKGC and existing systems
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def load_benchmark_results():
    """Load benchmark comparison results"""
    results_path = Path("results/benchmark/benchmark_results.json")
    
    with open(results_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ Loaded benchmark results from: {results_path}")
    return data

def create_comprehensive_comparison(results):
    """Create comprehensive comparison visualizations"""
    
    # Set style
    plt.style.use('seaborn-v0_8-whitegrid')
    fig = plt.figure(figsize=(18, 10))
    
    # Prepare data
    systems = ['KGCN\n(Baseline)', 'RAG\n(Baseline)', 'AKGC\n(Standard)', 'AKGC\n(Ultra)']
    system_keys = ['baseline_kgcn', 'baseline_rag', 'standard', 'ultra_optimized']
    
    accuracies = [results[k]['accuracy'] for k in system_keys]
    latencies = [results[k]['avg_latency_ms'] for k in system_keys]
    std_latencies = [results[k]['std_latency_ms'] for k in system_keys]
    
    colors = ['#e74c3c', '#f39c12', '#3498db', '#2ecc71']
    
    # 1. Accuracy Comparison
    ax1 = plt.subplot(2, 3, 1)
    bars = ax1.bar(systems, accuracies, color=colors, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
    ax1.set_title('Accuracy Comparison', fontsize=14, fontweight='bold', pad=15)
    ax1.set_ylim(0, 105)
    ax1.axhline(y=100, color='green', linestyle='--', alpha=0.3, linewidth=2)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # 2. Latency Comparison
    ax2 = plt.subplot(2, 3, 2)
    bars = ax2.bar(systems, latencies, color=colors, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('Latency (ms)', fontsize=12, fontweight='bold')
    ax2.set_title('Average Latency Comparison', fontsize=14, fontweight='bold', pad=15)
    ax2.set_yscale('log')
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height * 1.3,
                f'{height:.2f}ms',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # 3. Speedup Factor
    ax3 = plt.subplot(2, 3, 3)
    baseline_latency = results['baseline_kgcn']['avg_latency_ms']
    speedups = [baseline_latency / lat for lat in latencies]
    
    bars = ax3.bar(systems, speedups, color=colors, edgecolor='black', linewidth=1.5)
    ax3.set_ylabel('Speedup Factor (×)', fontsize=12, fontweight='bold')
    ax3.set_title('Speedup vs KGCN Baseline', fontsize=14, fontweight='bold', pad=15)
    ax3.axhline(y=1, color='red', linestyle='--', alpha=0.5, linewidth=2, label='Baseline')
    ax3.legend()
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height:.1f}×',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # 4. Accuracy vs Latency Scatter
    ax4 = plt.subplot(2, 3, 4)
    scatter = ax4.scatter(latencies, accuracies, s=500, c=colors, 
                         edgecolors='black', linewidth=2, alpha=0.7)
    
    # Add labels for each point
    for i, system in enumerate(systems):
        ax4.annotate(system.replace('\n', ' '), 
                    (latencies[i], accuracies[i]),
                    xytext=(10, 10), textcoords='offset points',
                    fontsize=10, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor=colors[i], alpha=0.3))
    
    ax4.set_xlabel('Latency (ms)', fontsize=12, fontweight='bold')
    ax4.set_ylabel('Accuracy (%)', fontsize=12, fontweight='bold')
    ax4.set_title('Accuracy vs Latency Trade-off', fontsize=14, fontweight='bold', pad=15)
    ax4.set_xscale('log')
    ax4.grid(True, alpha=0.3)
    
    # 5. Latency with Error Bars
    ax5 = plt.subplot(2, 3, 5)
    x_pos = np.arange(len(systems))
    bars = ax5.bar(x_pos, latencies, yerr=std_latencies, 
                   color=colors, edgecolor='black', linewidth=1.5,
                   capsize=8, error_kw={'linewidth': 2, 'ecolor': 'black'})
    ax5.set_xticks(x_pos)
    ax5.set_xticklabels(systems)
    ax5.set_ylabel('Latency (ms)', fontsize=12, fontweight='bold')
    ax5.set_title('Latency with Standard Deviation', fontsize=14, fontweight='bold', pad=15)
    ax5.set_yscale('log')
    
    # 6. Performance Improvement Summary
    ax6 = plt.subplot(2, 3, 6)
    
    # Calculate improvements over KGCN
    kgcn_acc = results['baseline_kgcn']['accuracy']
    kgcn_lat = results['baseline_kgcn']['avg_latency_ms']
    
    improvements = {
        'AKGC\nStandard': {
            'accuracy': results['standard']['accuracy'] - kgcn_acc,
            'latency': ((kgcn_lat - results['standard']['avg_latency_ms']) / kgcn_lat) * 100
        },
        'AKGC\nUltra': {
            'accuracy': results['ultra_optimized']['accuracy'] - kgcn_acc,
            'latency': ((kgcn_lat - results['ultra_optimized']['avg_latency_ms']) / kgcn_lat) * 100
        }
    }
    
    x = np.arange(len(improvements))
    width = 0.35
    
    acc_improvements = [v['accuracy'] for v in improvements.values()]
    lat_improvements = [v['latency'] for v in improvements.values()]
    
    bars1 = ax6.bar(x - width/2, acc_improvements, width, 
                    label='Accuracy Gain (%)', color='#3498db', 
                    edgecolor='black', linewidth=1.5)
    bars2 = ax6.bar(x + width/2, lat_improvements, width, 
                    label='Latency Reduction (%)', color='#2ecc71',
                    edgecolor='black', linewidth=1.5)
    
    ax6.set_ylabel('Improvement (%)', fontsize=12, fontweight='bold')
    ax6.set_title('Improvement over KGCN Baseline', fontsize=14, fontweight='bold', pad=15)
    ax6.set_xticks(x)
    ax6.set_xticklabels(improvements.keys())
    ax6.legend(fontsize=10)
    ax6.axhline(y=0, color='black', linestyle='-', linewidth=1)
    ax6.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax6.text(bar.get_x() + bar.get_width()/2., height + 2,
                    f'{height:.1f}%',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.suptitle('AKGC vs KGCN Performance Comparison', 
                fontsize=18, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    # Save figure
    output_path = Path("results/benchmark/akgc_vs_kgcn_comparison.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✅ Visualization saved to: {output_path}")
    
    # Also save as PDF
    output_pdf = Path("results/benchmark/akgc_vs_kgcn_comparison.pdf")
    plt.savefig(output_pdf, dpi=300, bbox_inches='tight', format='pdf')
    print(f"✅ PDF version saved to: {output_pdf}")
    
    plt.show()

def create_summary_table(results):
    """Create a detailed comparison table"""
    print("\n" + "="*110)
    print("📊 AKGC vs KGCN PERFORMANCE COMPARISON")
    print("="*110)
    
    header = f"{'System':<20} {'Accuracy (%)':<15} {'Avg Latency (ms)':<20} {'Std Dev (ms)':<15} {'Speedup':<10}"
    print(header)
    print("-"*110)
    
    systems = {
        'KGCN (Baseline)': 'baseline_kgcn',
        'RAG (Baseline)': 'baseline_rag',
        'AKGC Standard': 'standard',
        'AKGC Ultra': 'ultra_optimized'
    }
    
    baseline_latency = results['baseline_kgcn']['avg_latency_ms']
    
    for name, key in systems.items():
        r = results[key]
        speedup = baseline_latency / r['avg_latency_ms']
        row = f"{name:<20} {r['accuracy']:<15.1f} {r['avg_latency_ms']:<20.4f} {r['std_latency_ms']:<15.4f} {speedup:<10.1f}×"
        print(row)
    
    print("-"*110)
    
    # Calculate improvements
    print("\n" + "="*110)
    print("📈 IMPROVEMENTS OVER KGCN BASELINE")
    print("="*110)
    
    kgcn = results['baseline_kgcn']
    
    for name, key in [('AKGC Standard', 'standard'), ('AKGC Ultra', 'ultra_optimized')]:
        r = results[key]
        acc_gain = r['accuracy'] - kgcn['accuracy']
        lat_reduction = ((kgcn['avg_latency_ms'] - r['avg_latency_ms']) / kgcn['avg_latency_ms']) * 100
        speedup = kgcn['avg_latency_ms'] / r['avg_latency_ms']
        
        print(f"\n{name}:")
        print(f"  • Accuracy Gain: +{acc_gain:.1f}% (from {kgcn['accuracy']:.1f}% to {r['accuracy']:.1f}%)")
        print(f"  • Latency Reduction: {lat_reduction:.1f}% (from {kgcn['avg_latency_ms']:.2f}ms to {r['avg_latency_ms']:.4f}ms)")
        print(f"  • Speedup Factor: {speedup:.1f}× faster")
    
    print("\n" + "="*110)

def main():
    """Main execution function"""
    print("🔍 Loading benchmark results...")
    results = load_benchmark_results()
    
    # Display summary table
    create_summary_table(results)
    
    # Create visualizations
    print("\n🎨 Creating comparative visualizations...")
    create_comprehensive_comparison(results)
    
    print("\n✅ Comparison visualization complete!")

if __name__ == "__main__":
    main()
