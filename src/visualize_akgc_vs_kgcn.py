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

def create_individual_charts(results):
    """Create individual comparison charts"""
    
    # Set style
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # Prepare data
    systems = ['KGCN\n(Baseline)', 'RAG\n(Baseline)', 'AKGC\n(Standard)', 'AKGC\n(Ultra)']
    system_keys = ['baseline_kgcn', 'baseline_rag', 'standard', 'ultra_optimized']
    
    accuracies = [results[k]['accuracy'] for k in system_keys]
    latencies = [results[k]['avg_latency_ms'] for k in system_keys]
    std_latencies = [results[k]['std_latency_ms'] for k in system_keys]
    
    colors = ['#e74c3c', '#f39c12', '#3498db', '#2ecc71']
    
    # Chart 1: Accuracy Comparison
    fig1 = plt.figure(figsize=(10, 6))
    ax1 = fig1.add_subplot(111)
    bars = ax1.bar(systems, accuracies, color=colors, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Accuracy (%)', fontsize=13, fontweight='bold')
    ax1.set_title('Accuracy Comparison: AKGC vs Baseline Systems', fontsize=15, fontweight='bold', pad=20)
    ax1.set_ylim(0, 105)
    ax1.axhline(y=100, color='green', linestyle='--', alpha=0.3, linewidth=2, label='Perfect Score')
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    fig1.savefig('results/benchmark/chart1_accuracy_comparison.png', dpi=300, bbox_inches='tight')
    fig1.savefig('results/benchmark/chart1_accuracy_comparison.pdf', dpi=300, bbox_inches='tight', format='pdf')
    print("✅ Chart 1 saved: Accuracy Comparison")
    plt.close(fig1)
    
    # Chart 2: Latency Comparison
    fig2 = plt.figure(figsize=(10, 6))
    ax2 = fig2.add_subplot(111)
    bars = ax2.bar(systems, latencies, color=colors, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('Latency (ms, log scale)', fontsize=13, fontweight='bold')
    ax2.set_title('Latency Comparison: AKGC vs Baseline Systems', fontsize=15, fontweight='bold', pad=20)
    ax2.set_yscale('log')
    ax2.grid(True, alpha=0.3, which='both')
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height * 1.5,
                f'{height:.2f}ms',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    fig2.savefig('results/benchmark/chart2_latency_comparison.png', dpi=300, bbox_inches='tight')
    fig2.savefig('results/benchmark/chart2_latency_comparison.pdf', dpi=300, bbox_inches='tight', format='pdf')
    print("✅ Chart 2 saved: Latency Comparison")
    plt.close(fig2)
    
    # Chart 3: Speedup Factor
    fig3 = plt.figure(figsize=(10, 6))
    ax3 = fig3.add_subplot(111)
    baseline_latency = results['baseline_kgcn']['avg_latency_ms']
    speedups = [baseline_latency / lat for lat in latencies]
    
    bars = ax3.bar(systems, speedups, color=colors, edgecolor='black', linewidth=1.5)
    ax3.set_ylabel('Speedup Factor (×)', fontsize=13, fontweight='bold')
    ax3.set_title('Speedup Factor vs KGCN Baseline', fontsize=15, fontweight='bold', pad=20)
    ax3.axhline(y=1, color='red', linestyle='--', alpha=0.5, linewidth=2, label='Baseline (1×)')
    ax3.legend(fontsize=11)
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 500,
                f'{height:.0f}×',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    fig3.savefig('results/benchmark/chart3_speedup_factor.png', dpi=300, bbox_inches='tight')
    fig3.savefig('results/benchmark/chart3_speedup_factor.pdf', dpi=300, bbox_inches='tight', format='pdf')
    print("✅ Chart 3 saved: Speedup Factor")
    plt.close(fig3)
    
    # Chart 4: Accuracy vs Latency Trade-off
    fig4 = plt.figure(figsize=(10, 7))
    ax4 = fig4.add_subplot(111)
    scatter = ax4.scatter(latencies, accuracies, s=600, c=colors, 
                         edgecolors='black', linewidth=2.5, alpha=0.8, zorder=3)
    
    # Add labels for each point
    for i, system in enumerate(systems):
        ax4.annotate(system.replace('\n', ' '), 
                    (latencies[i], accuracies[i]),
                    xytext=(15, 15), textcoords='offset points',
                    fontsize=11, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.6', facecolor=colors[i], alpha=0.4, edgecolor='black', linewidth=1.5),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', lw=1.5))
    
    ax4.set_xlabel('Latency (ms, log scale)', fontsize=13, fontweight='bold')
    ax4.set_ylabel('Accuracy (%)', fontsize=13, fontweight='bold')
    ax4.set_title('Accuracy vs Latency Trade-off Analysis', fontsize=15, fontweight='bold', pad=20)
    ax4.set_xscale('log')
    ax4.grid(True, alpha=0.3, which='both')
    ax4.set_ylim(80, 105)
    
    plt.tight_layout()
    fig4.savefig('results/benchmark/chart4_accuracy_vs_latency.png', dpi=300, bbox_inches='tight')
    fig4.savefig('results/benchmark/chart4_accuracy_vs_latency.pdf', dpi=300, bbox_inches='tight', format='pdf')
    print("✅ Chart 4 saved: Accuracy vs Latency Trade-off")
    plt.close(fig4)
    
    # Chart 5: Performance Improvement Summary
    fig5 = plt.figure(figsize=(10, 6))
    ax5 = fig5.add_subplot(111)
    # Calculate improvements over KGCN
    kgcn_acc = results['baseline_kgcn']['accuracy']
    kgcn_lat = results['baseline_kgcn']['avg_latency_ms']
    
    improvements = {
        'AKGC Standard': {
            'accuracy': results['standard']['accuracy'] - kgcn_acc,
            'latency': ((kgcn_lat - results['standard']['avg_latency_ms']) / kgcn_lat) * 100
        },
        'AKGC Ultra': {
            'accuracy': results['ultra_optimized']['accuracy'] - kgcn_acc,
            'latency': ((kgcn_lat - results['ultra_optimized']['avg_latency_ms']) / kgcn_lat) * 100
        }
    }
    
    x = np.arange(len(improvements))
    width = 0.35
    
    acc_improvements = [v['accuracy'] for v in improvements.values()]
    lat_improvements = [v['latency'] for v in improvements.values()]
    
    bars1 = ax5.bar(x - width/2, acc_improvements, width, 
                    label='Accuracy Gain (%)', color='#3498db', 
                    edgecolor='black', linewidth=1.5)
    bars2 = ax5.bar(x + width/2, lat_improvements, width, 
                    label='Latency Reduction (%)', color='#2ecc71',
                    edgecolor='black', linewidth=1.5)
    
    ax5.set_ylabel('Improvement (%)', fontsize=13, fontweight='bold')
    ax5.set_title('Performance Improvement over KGCN Baseline', fontsize=15, fontweight='bold', pad=20)
    ax5.set_xticks(x)
    ax5.set_xticklabels(improvements.keys())
    ax5.legend(fontsize=11, loc='upper left')
    ax5.axhline(y=0, color='black', linestyle='-', linewidth=1.5)
    ax5.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax5.text(bar.get_x() + bar.get_width()/2., height + 3,
                    f'{height:.1f}%',
                    ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    fig5.savefig('results/benchmark/chart5_improvement_summary.png', dpi=300, bbox_inches='tight')
    fig5.savefig('results/benchmark/chart5_improvement_summary.pdf', dpi=300, bbox_inches='tight', format='pdf')
    print("✅ Chart 5 saved: Performance Improvement Summary")
    plt.close(fig5)
    
    print("\n✅ All individual charts created successfully!")

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
    print("\n🎨 Creating individual comparative charts...")
    create_individual_charts(results)
    
    print("\n✅ Comparison visualization complete!")

if __name__ == "__main__":
    main()
