#!/usr/bin/env python3
"""
External Dataset Testing Pipeline
Tests AKGC on preprocessed external datasets
"""

import json
import time
import os
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# Import AKGC systems
from akgc_ultra_optimized import UltraOptimizedAKGC
from akgc_simple_fast import SimpleFastAKGC
from utils.metrics import compute_accuracy, compute_rouge_l, compute_bertscore


class ExternalDatasetTester:
    """Tests AKGC on external datasets."""
    
    def __init__(self, use_ultra: bool = False):
        self.use_ultra = use_ultra
        self.results_dir = Path("results/external")
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🚀 Initializing AKGC System ({'Ultra-Optimized' if use_ultra else 'Standard'})...")
        
        if use_ultra:
            self.akgc = UltraOptimizedAKGC()
        else:
            self.akgc = SimpleFastAKGC()
        
        print("✅ AKGC initialized successfully!")
    
    def load_dataset(self, file_path: str) -> List[Dict]:
        """Load preprocessed dataset."""
        print(f"\n📂 Loading dataset from: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Loaded {len(data)} test cases")
        return data
    
    def test_single_case(self, case: Dict) -> Dict:
        """Test a single case."""
        prompt = case['prompt']
        ground_truth = case.get('ground_truth')
        
        start_time = time.time()
        
        try:
            if self.use_ultra:
                response, factual, confidence = self.akgc.ultra_fast_correction(prompt)
            else:
                response, factual, hvi = self.akgc.adaptive_correction_simple_fast(prompt)
                confidence = hvi
            
            processing_time = (time.time() - start_time) * 1000  # Convert to ms
            
            # Compute metrics if ground truth available
            metrics = {}
            if ground_truth:
                metrics['accuracy'] = compute_accuracy(response, ground_truth)
                metrics['rouge_l'] = compute_rouge_l(response, ground_truth)
                
                # BERTScore (optional, can be slow)
                try:
                    metrics['bertscore'] = compute_bertscore(response, ground_truth)
                except:
                    metrics['bertscore'] = None
            
            result = {
                'id': case.get('id'),
                'prompt': prompt,
                'response': response,
                'ground_truth': ground_truth,
                'factual': factual,
                'confidence': confidence,
                'processing_time_ms': processing_time,
                'metrics': metrics,
                'metadata': case.get('metadata', {}),
                'success': True
            }
            
        except Exception as e:
            result = {
                'id': case.get('id'),
                'prompt': prompt,
                'error': str(e),
                'success': False
            }
        
        return result
    
    def test_dataset(self, data: List[Dict], max_cases: int = None) -> Dict:
        """Test entire dataset."""
        print(f"\n🧪 Testing AKGC on External Dataset")
        print("=" * 70)
        
        if max_cases:
            data = data[:max_cases]
            print(f"📊 Testing first {max_cases} cases")
        else:
            print(f"📊 Testing all {len(data)} cases")
        
        results = []
        total_time = 0
        successful_cases = 0
        
        for idx, case in enumerate(data, 1):
            if idx % 10 == 0 or idx == 1:
                print(f"   Progress: {idx}/{len(data)} cases completed")
            
            result = self.test_single_case(case)
            results.append(result)
            
            if result['success']:
                successful_cases += 1
                total_time += result['processing_time_ms']
        
        # Compute aggregate metrics
        aggregate_metrics = self.compute_aggregate_metrics(results)
        
        # Print summary
        self.print_summary(results, aggregate_metrics)
        
        # Prepare output
        output = {
            'timestamp': datetime.now().isoformat(),
            'system': 'Ultra-Optimized' if self.use_ultra else 'Standard',
            'total_cases': len(data),
            'successful_cases': successful_cases,
            'failed_cases': len(data) - successful_cases,
            'aggregate_metrics': aggregate_metrics,
            'results': results
        }
        
        return output
    
    def compute_aggregate_metrics(self, results: List[Dict]) -> Dict:
        """Compute aggregate metrics across all results."""
        successful = [r for r in results if r['success']]
        
        if not successful:
            return {}
        
        # Processing time
        processing_times = [r['processing_time_ms'] for r in successful]
        avg_time = sum(processing_times) / len(processing_times)
        min_time = min(processing_times)
        max_time = max(processing_times)
        
        # Latency compliance
        latency_target = 300  # ms
        cases_meeting_target = sum(1 for t in processing_times if t < latency_target)
        latency_compliance = (cases_meeting_target / len(processing_times)) * 100
        
        # Accuracy metrics (if ground truth available)
        with_ground_truth = [r for r in successful if r.get('ground_truth')]
        
        metrics = {
            'avg_processing_time_ms': avg_time,
            'min_processing_time_ms': min_time,
            'max_processing_time_ms': max_time,
            'latency_compliance_pct': latency_compliance,
            'cases_with_ground_truth': len(with_ground_truth)
        }
        
        if with_ground_truth:
            accuracies = [r['metrics']['accuracy'] for r in with_ground_truth]
            rouge_scores = [r['metrics']['rouge_l'] for r in with_ground_truth]
            
            metrics['avg_accuracy'] = sum(accuracies) / len(accuracies)
            metrics['avg_rouge_l'] = sum(rouge_scores) / len(rouge_scores)
            
            # BERTScore if available
            bertscores = [r['metrics']['bertscore'] for r in with_ground_truth 
                         if r['metrics'].get('bertscore') is not None]
            if bertscores:
                metrics['avg_bertscore'] = sum(bertscores) / len(bertscores)
            
            # High accuracy cases
            high_accuracy = sum(1 for a in accuracies if a >= 0.8)
            metrics['high_accuracy_cases'] = high_accuracy
            metrics['high_accuracy_pct'] = (high_accuracy / len(accuracies)) * 100
        
        # Correction statistics
        corrections_made = sum(1 for r in successful if not r['factual'])
        metrics['corrections_made'] = corrections_made
        metrics['correction_rate_pct'] = (corrections_made / len(successful)) * 100
        
        return metrics
    
    def print_summary(self, results: List[Dict], metrics: Dict):
        """Print test summary."""
        print("\n" + "=" * 70)
        print("📊 EXTERNAL DATASET TEST RESULTS")
        print("=" * 70)
        
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        print(f"\n✅ Successful Cases: {len(successful)}/{len(results)}")
        if failed:
            print(f"❌ Failed Cases: {len(failed)}")
        
        if metrics:
            print(f"\n⚡ Performance Metrics:")
            print(f"   Average Processing Time: {metrics['avg_processing_time_ms']:.2f}ms")
            print(f"   Min/Max Time: {metrics['min_processing_time_ms']:.2f}ms / {metrics['max_processing_time_ms']:.2f}ms")
            print(f"   Latency Compliance (<300ms): {metrics['latency_compliance_pct']:.1f}%")
            
            if metrics.get('avg_accuracy') is not None:
                print(f"\n🎯 Accuracy Metrics:")
                print(f"   Average Accuracy: {metrics['avg_accuracy']:.3f}")
                print(f"   Average ROUGE-L: {metrics['avg_rouge_l']:.3f}")
                if metrics.get('avg_bertscore'):
                    print(f"   Average BERTScore: {metrics['avg_bertscore']:.3f}")
                print(f"   High Accuracy Cases (≥0.8): {metrics['high_accuracy_cases']} ({metrics['high_accuracy_pct']:.1f}%)")
            
            print(f"\n🔧 Correction Statistics:")
            print(f"   Corrections Made: {metrics['corrections_made']}")
            print(f"   Correction Rate: {metrics['correction_rate_pct']:.1f}%")
    
    def save_results(self, output: Dict, dataset_name: str):
        """Save test results."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"external_test_{dataset_name}_{timestamp}.json"
        output_path = self.results_dir / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to: {output_path}")
        return str(output_path)
    
    def generate_report(self, output: Dict, dataset_name: str):
        """Generate markdown report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"external_test_report_{dataset_name}_{timestamp}.md"
        report_path = self.results_dir / filename
        
        metrics = output['aggregate_metrics']
        
        report = f"""# AKGC External Dataset Test Report

## Test Information
- **Dataset**: {dataset_name}
- **System**: {output['system']}
- **Timestamp**: {output['timestamp']}
- **Total Cases**: {output['total_cases']}
- **Successful**: {output['successful_cases']}
- **Failed**: {output['failed_cases']}

## Performance Metrics

### Processing Time
- **Average**: {metrics.get('avg_processing_time_ms', 0):.2f}ms
- **Min/Max**: {metrics.get('min_processing_time_ms', 0):.2f}ms / {metrics.get('max_processing_time_ms', 0):.2f}ms
- **Latency Compliance (<300ms)**: {metrics.get('latency_compliance_pct', 0):.1f}%

"""
        
        if metrics.get('avg_accuracy') is not None:
            report += f"""### Accuracy Metrics
- **Average Accuracy**: {metrics['avg_accuracy']:.3f}
- **Average ROUGE-L**: {metrics['avg_rouge_l']:.3f}
"""
            if metrics.get('avg_bertscore'):
                report += f"- **Average BERTScore**: {metrics['avg_bertscore']:.3f}\n"
            
            report += f"- **High Accuracy Cases (≥0.8)**: {metrics['high_accuracy_cases']} ({metrics['high_accuracy_pct']:.1f}%)\n\n"
        
        report += f"""### Correction Statistics
- **Corrections Made**: {metrics.get('corrections_made', 0)}
- **Correction Rate**: {metrics.get('correction_rate_pct', 0):.1f}%

## Sample Results

"""
        
        # Add sample results
        sample_results = [r for r in output['results'] if r['success']][:5]
        for idx, result in enumerate(sample_results, 1):
            report += f"""### Sample {idx}
- **Prompt**: {result['prompt'][:100]}...
- **Response**: {result['response'][:100]}...
- **Processing Time**: {result['processing_time_ms']:.2f}ms
- **Factual**: {result['factual']}

"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📄 Report saved to: {report_path}")
        return str(report_path)


def main():
    """Main testing function."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python test_external_dataset.py <preprocessed_dataset.json> [--ultra] [--max-cases N]")
        print("\nOptions:")
        print("  --ultra       Use ultra-optimized AKGC variant")
        print("  --max-cases N Test only first N cases")
        print("\nExample:")
        print("  python src/test_external_dataset.py data/external/preprocessed_dataset.json")
        print("  python src/test_external_dataset.py data/external/preprocessed_dataset.json --ultra --max-cases 50")
        return
    
    file_path = sys.argv[1]
    use_ultra = '--ultra' in sys.argv
    
    max_cases = None
    if '--max-cases' in sys.argv:
        idx = sys.argv.index('--max-cases')
        if idx + 1 < len(sys.argv):
            max_cases = int(sys.argv[idx + 1])
    
    if not os.path.exists(file_path):
        print(f"❌ Error: File not found: {file_path}")
        return
    
    try:
        # Initialize tester
        tester = ExternalDatasetTester(use_ultra=use_ultra)
        
        # Load dataset
        data = tester.load_dataset(file_path)
        
        # Run tests
        output = tester.test_dataset(data, max_cases=max_cases)
        
        # Save results
        dataset_name = Path(file_path).stem
        tester.save_results(output, dataset_name)
        tester.generate_report(output, dataset_name)
        
        print("\n✅ Testing Complete!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
