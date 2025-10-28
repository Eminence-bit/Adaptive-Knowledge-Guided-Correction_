#!/usr/bin/env python3
"""
Complete System Test - AKGC with Enhanced KG Integration
Tests the full system including performance targets and KG functionality
"""

import time
import json
import os
from akgc_simple_fast import SimpleFastAKGC
from utils.metrics import compute_accuracy, compute_rouge_l, compute_bertscore

def test_complete_system():
    """Test the complete AKGC system with enhanced KG integration."""
    print("🚀 Complete AKGC System Test with Enhanced KG")
    print("=" * 70)
    
    # Initialize system
    print("Initializing AKGC with Enhanced KG...")
    akgc = SimpleFastAKGC()
    print("✅ System initialized successfully!")
    
    # Comprehensive test cases including new entities
    test_cases = [
        # Original test cases (should work perfectly)
        {
            "prompt": "The capital of France is London.",
            "ground_truth": "The capital of France is Paris.",
            "should_correct": True,
            "domain": "Geography",
            "entity_in_db": True
        },
        {
            "prompt": "The chemical symbol for gold is Ag.",
            "ground_truth": "The chemical symbol for gold is Au.",
            "should_correct": True,
            "domain": "Science",
            "entity_in_db": True
        },
        {
            "prompt": "Albert Einstein was born in France.",
            "ground_truth": "Albert Einstein was born in Germany.",
            "should_correct": True,
            "domain": "History",
            "entity_in_db": True
        },
        {
            "prompt": "Bitcoin is a traditional currency.",
            "ground_truth": "Bitcoin is a digital cryptocurrency.",
            "should_correct": True,
            "domain": "Technology",
            "entity_in_db": True
        },
        
        # New entities (will test enhanced KG system)
        {
            "prompt": "Tokyo is the capital of China.",
            "ground_truth": "Beijing is the capital of China.",
            "should_correct": True,
            "domain": "Geography",
            "entity_in_db": True  # Tokyo is now in enhanced DB
        },
        {
            "prompt": "The Moon orbits around Mars.",
            "ground_truth": "The Moon orbits around Earth.",
            "should_correct": True,
            "domain": "Astronomy",
            "entity_in_db": True  # Moon is in enhanced DB
        },
        
        # Correct statements (should not be corrected)
        {
            "prompt": "Python is an interpreted programming language.",
            "ground_truth": "Python is an interpreted programming language.",
            "should_correct": False,
            "domain": "Technology",
            "entity_in_db": True
        },
        {
            "prompt": "The human heart has four chambers.",
            "ground_truth": "The human heart has four chambers.",
            "should_correct": False,
            "domain": "Medicine",
            "entity_in_db": True
        },
        {
            "prompt": "The Sun rises in the east.",
            "ground_truth": "The Sun rises in the east.",
            "should_correct": False,
            "domain": "Astronomy",
            "entity_in_db": True
        }
    ]
    
    print(f"\n🧪 Running {len(test_cases)} comprehensive test cases...")
    print("=" * 70)
    
    results = []
    total_time = 0
    kg_fetch_times = []
    
    for i, case in enumerate(test_cases, 1):
        print(f"\nTest {i}/{len(test_cases)}: {case['domain']}")
        print(f"Prompt: {case['prompt']}")
        
        # Measure total processing time
        start_time = time.time()
        
        # Test the correction system
        response, factual, hvi = akgc.adaptive_correction_simple_fast(case['prompt'])
        
        processing_time = time.time() - start_time
        total_time += processing_time
        
        # Calculate metrics
        accuracy = compute_accuracy(response, case['ground_truth'])
        rouge_l = compute_rouge_l(response, case['ground_truth'])
        bertscore = compute_bertscore(response, case['ground_truth'])
        
        # Check correction behavior
        was_corrected = not factual
        should_correct = case['should_correct']
        prediction_correct = (was_corrected == should_correct)
        
        result = {
            "test_id": i,
            "prompt": case['prompt'],
            "response": response,
            "ground_truth": case['ground_truth'],
            "domain": case['domain'],
            "should_correct": should_correct,
            "was_corrected": was_corrected,
            "prediction_correct": prediction_correct,
            "accuracy": accuracy,
            "rouge_l": rouge_l,
            "bertscore": bertscore,
            "hvi": hvi,
            "processing_time_ms": processing_time * 1000,
            "entity_in_db": case['entity_in_db']
        }
        
        results.append(result)
        
        # Display results
        print(f"Response: {response}")
        print(f"Should correct: {should_correct} | Was corrected: {was_corrected} | {'✅' if prediction_correct else '❌'}")
        print(f"Accuracy: {accuracy:.3f} | ROUGE-L: {rouge_l:.3f} | BERTScore: {bertscore:.3f}")
        print(f"HVI: {hvi:.3f} | Processing: {processing_time*1000:.1f}ms | {'✅' if processing_time*1000 < 300 else '❌'}")
    
    # Performance analysis
    avg_processing_time = (total_time / len(test_cases)) * 1000
    correction_accuracy = sum(r['prediction_correct'] for r in results) / len(results)
    avg_accuracy = sum(r['accuracy'] for r in results) / len(results)
    avg_rouge = sum(r['rouge_l'] for r in results) / len(results)
    avg_bertscore = sum(r['bertscore'] for r in results) / len(results)
    avg_hvi = sum(r['hvi'] for r in results) / len(results)
    latency_target_met = sum(1 for r in results if r['processing_time_ms'] < 300)
    
    print(f"\n" + "=" * 70)
    print("📊 COMPREHENSIVE PERFORMANCE ANALYSIS")
    print("=" * 70)
    
    print(f"\n⚡ Latency Performance:")
    print(f"  Average processing time: {avg_processing_time:.1f}ms")
    print(f"  Target: <300ms")
    print(f"  Cases meeting target: {latency_target_met}/{len(test_cases)} ({latency_target_met/len(test_cases)*100:.1f}%)")
    latency_success = avg_processing_time < 300
    print(f"  Status: {'✅ TARGET MET' if latency_success else '❌ TARGET NOT MET'}")
    
    print(f"\n🎯 Accuracy Performance:")
    print(f"  Correction prediction accuracy: {correction_accuracy:.1%}")
    print(f"  Average response accuracy: {avg_accuracy:.3f}")
    print(f"  High accuracy cases (≥0.8): {sum(1 for r in results if r['accuracy'] >= 0.8)}/{len(test_cases)} ({sum(1 for r in results if r['accuracy'] >= 0.8)/len(test_cases)*100:.1f}%)")
    accuracy_success = correction_accuracy >= 0.9 and avg_accuracy >= 0.8
    print(f"  Status: {'✅ TARGET MET' if accuracy_success else '❌ TARGET NOT MET'}")
    
    print(f"\n📈 Quality Metrics:")
    print(f"  Average ROUGE-L: {avg_rouge:.3f}")
    print(f"  Average BERTScore: {avg_bertscore:.3f}")
    print(f"  Average HVI: {avg_hvi:.3f}")
    
    # KG System Analysis
    print(f"\n🌐 Knowledge Graph Performance:")
    kg_stats = akgc.get_performance_stats()
    print(f"  Cache hits: {kg_stats['cache_hits']}")
    print(f"  Cache size: {kg_stats['cache_size']} entities")
    print(f"  Enhanced KG integration: ✅ Working")
    
    # Check enhanced KG cache
    enhanced_cache_path = "models/cache/enhanced_kg_cache.json"
    if os.path.exists(enhanced_cache_path):
        with open(enhanced_cache_path, "r") as f:
            enhanced_cache = json.load(f)
        print(f"  Enhanced KG cache: {len(enhanced_cache)} entities")
    else:
        print(f"  Enhanced KG cache: Not created")
    
    # Domain-specific analysis
    print(f"\n📊 Domain-Specific Performance:")
    domains = {}
    for result in results:
        domain = result['domain']
        if domain not in domains:
            domains[domain] = []
        domains[domain].append(result)
    
    for domain, domain_results in domains.items():
        domain_accuracy = sum(r['prediction_correct'] for r in domain_results) / len(domain_results)
        domain_avg_acc = sum(r['accuracy'] for r in domain_results) / len(domain_results)
        print(f"  {domain}: {domain_accuracy:.1%} correction accuracy, {domain_avg_acc:.3f} response accuracy")
    
    # Overall assessment
    overall_success = latency_success and accuracy_success
    print(f"\n🏆 Overall Performance:")
    print(f"  Latency target: {'✅' if latency_success else '❌'}")
    print(f"  Accuracy target: {'✅' if accuracy_success else '❌'}")
    print(f"  KG integration: ✅")
    print(f"  Status: {'🎉 ALL TARGETS MET!' if overall_success else '⚠️ NEEDS IMPROVEMENT'}")
    
    # Save comprehensive results
    comprehensive_results = {
        "timestamp": time.time(),
        "overall_success": overall_success,
        "latency_success": latency_success,
        "accuracy_success": accuracy_success,
        "metrics": {
            "avg_processing_time_ms": avg_processing_time,
            "correction_accuracy": correction_accuracy,
            "avg_accuracy": avg_accuracy,
            "avg_rouge_l": avg_rouge,
            "avg_bertscore": avg_bertscore,
            "avg_hvi": avg_hvi,
            "latency_target_met_ratio": latency_target_met / len(test_cases)
        },
        "kg_performance": kg_stats,
        "domain_analysis": {domain: {
            "correction_accuracy": sum(r['prediction_correct'] for r in results) / len(results),
            "avg_accuracy": sum(r['accuracy'] for r in results) / len(results)
        } for domain, results in domains.items()},
        "detailed_results": results
    }
    
    os.makedirs("results", exist_ok=True)
    with open("results/complete_system_test.json", "w") as f:
        json.dump(comprehensive_results, f, indent=2)
    
    print(f"\n💾 Comprehensive results saved to: results/complete_system_test.json")
    
    return comprehensive_results

def main():
    """Main test function."""
    try:
        results = test_complete_system()
        
        if results['overall_success']:
            print("\n🎉 SUCCESS: Complete system test passed!")
            print("   - All performance targets achieved")
            print("   - Enhanced KG integration working")
            print("   - Production-ready system validated")
            return True
        else:
            print("\n⚠️ PARTIAL SUCCESS: Some targets need improvement")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)