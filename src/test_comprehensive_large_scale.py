#!/usr/bin/env python3
"""
Comprehensive Large-Scale Test Suite for AKGC
Tests 100+ cases across multiple domains to validate production readiness
"""

import time
import json
import os
from akgc_ultra_optimized import UltraOptimizedAKGC
from utils.metrics import compute_accuracy, compute_rouge_l, compute_bertscore

class ComprehensiveLargeScaleTest:
    """Large-scale test suite with 100+ test cases."""
    
    def __init__(self):
        self.akgc = None
        self.test_cases = self.load_comprehensive_test_cases()
        
    def load_comprehensive_test_cases(self):
        """Load 100+ comprehensive test cases across all domains."""
        return {
            "geography": [
                # Capital Cities (20 cases)
                {"prompt": "The capital of France is London.", "ground_truth": "The capital of France is Paris.", "should_correct": True},
                {"prompt": "The capital of Germany is Munich.", "ground_truth": "The capital of Germany is Berlin.", "should_correct": True},
                {"prompt": "The capital of Italy is Milan.", "ground_truth": "The capital of Italy is Rome.", "should_correct": True},
                {"prompt": "The capital of Spain is Barcelona.", "ground_truth": "The capital of Spain is Madrid.", "should_correct": True},
                {"prompt": "The capital of Australia is Sydney.", "ground_truth": "The capital of Australia is Canberra.", "should_correct": True},
                {"prompt": "The capital of Brazil is Rio de Janeiro.", "ground_truth": "The capital of Brazil is Brasília.", "should_correct": True},
                {"prompt": "The capital of Canada is Toronto.", "ground_truth": "The capital of Canada is Ottawa.", "should_correct": True},
                {"prompt": "The capital of India is Mumbai.", "ground_truth": "The capital of India is New Delhi.", "should_correct": True},
                {"prompt": "The capital of China is Shanghai.", "ground_truth": "The capital of China is Beijing.", "should_correct": True},
                {"prompt": "The capital of Japan is Osaka.", "ground_truth": "The capital of Japan is Tokyo.", "should_correct": True},
                {"prompt": "The capital of Russia is St. Petersburg.", "ground_truth": "The capital of Russia is Moscow.", "should_correct": True},
                {"prompt": "The capital of Egypt is Alexandria.", "ground_truth": "The capital of Egypt is Cairo.", "should_correct": True},
                {"prompt": "The capital of Turkey is Istanbul.", "ground_truth": "The capital of Turkey is Ankara.", "should_correct": True},
                {"prompt": "The capital of South Africa is Johannesburg.", "ground_truth": "The capital of South Africa is Cape Town.", "should_correct": True},
                {"prompt": "The capital of Argentina is Córdoba.", "ground_truth": "The capital of Argentina is Buenos Aires.", "should_correct": True},
                # Correct capitals (5 cases)
                {"prompt": "The capital of France is Paris.", "ground_truth": "The capital of France is Paris.", "should_correct": False},
                {"prompt": "The capital of Germany is Berlin.", "ground_truth": "The capital of Germany is Berlin.", "should_correct": False},
                {"prompt": "The capital of Japan is Tokyo.", "ground_truth": "The capital of Japan is Tokyo.", "should_correct": False},
                {"prompt": "The capital of USA is Washington D.C.", "ground_truth": "The capital of USA is Washington D.C.", "should_correct": False},
                {"prompt": "The capital of China is Beijing.", "ground_truth": "The capital of China is Beijing.", "should_correct": False},
            ],
            
            "science": [
                # Chemical Elements (15 cases)
                {"prompt": "The chemical symbol for gold is Ag.", "ground_truth": "The chemical symbol for gold is Au.", "should_correct": True},
                {"prompt": "The chemical symbol for silver is Au.", "ground_truth": "The chemical symbol for silver is Ag.", "should_correct": True},
                {"prompt": "The chemical symbol for iron is Ir.", "ground_truth": "The chemical symbol for iron is Fe.", "should_correct": True},
                {"prompt": "The chemical symbol for copper is Co.", "ground_truth": "The chemical symbol for copper is Cu.", "should_correct": True},
                {"prompt": "The chemical symbol for lead is Pb.", "ground_truth": "The chemical symbol for lead is Pb.", "should_correct": False},
                {"prompt": "The chemical symbol for sodium is Na.", "ground_truth": "The chemical symbol for sodium is Na.", "should_correct": False},
                {"prompt": "The chemical symbol for potassium is K.", "ground_truth": "The chemical symbol for potassium is K.", "should_correct": False},
                {"prompt": "The chemical symbol for calcium is Ca.", "ground_truth": "The chemical symbol for calcium is Ca.", "should_correct": False},
                {"prompt": "The chemical symbol for oxygen is O.", "ground_truth": "The chemical symbol for oxygen is O.", "should_correct": False},
                {"prompt": "The chemical symbol for hydrogen is H.", "ground_truth": "The chemical symbol for hydrogen is H.", "should_correct": False},
                # Atomic Numbers (10 cases)
                {"prompt": "Oxygen has atomic number 6.", "ground_truth": "Oxygen has atomic number 8.", "should_correct": True},
                {"prompt": "Carbon has atomic number 8.", "ground_truth": "Carbon has atomic number 6.", "should_correct": True},
                {"prompt": "Nitrogen has atomic number 6.", "ground_truth": "Nitrogen has atomic number 7.", "should_correct": True},
                {"prompt": "Helium has atomic number 4.", "ground_truth": "Helium has atomic number 2.", "should_correct": True},
                {"prompt": "Hydrogen has atomic number 1.", "ground_truth": "Hydrogen has atomic number 1.", "should_correct": False},
                {"prompt": "Carbon has atomic number 6.", "ground_truth": "Carbon has atomic number 6.", "should_correct": False},
                {"prompt": "Oxygen has atomic number 8.", "ground_truth": "Oxygen has atomic number 8.", "should_correct": False},
                {"prompt": "Nitrogen has atomic number 7.", "ground_truth": "Nitrogen has atomic number 7.", "should_correct": False},
                {"prompt": "Neon has atomic number 10.", "ground_truth": "Neon has atomic number 10.", "should_correct": False},
                {"prompt": "Fluorine has atomic number 9.", "ground_truth": "Fluorine has atomic number 9.", "should_correct": False},
            ],
            
            "history": [
                # World Wars (10 cases)
                {"prompt": "World War I ended in 1919.", "ground_truth": "World War I ended in 1918.", "should_correct": True},
                {"prompt": "World War II ended in 1944.", "ground_truth": "World War II ended in 1945.", "should_correct": True},
                {"prompt": "World War I started in 1915.", "ground_truth": "World War I started in 1914.", "should_correct": True},
                {"prompt": "World War II started in 1940.", "ground_truth": "World War II started in 1939.", "should_correct": True},
                {"prompt": "World War I ended in 1918.", "ground_truth": "World War I ended in 1918.", "should_correct": False},
                {"prompt": "World War II ended in 1945.", "ground_truth": "World War II ended in 1945.", "should_correct": False},
                {"prompt": "World War I started in 1914.", "ground_truth": "World War I started in 1914.", "should_correct": False},
                {"prompt": "World War II started in 1939.", "ground_truth": "World War II started in 1939.", "should_correct": False},
                {"prompt": "World War I lasted from 1914 to 1918.", "ground_truth": "World War I lasted from 1914 to 1918.", "should_correct": False},
                {"prompt": "World War II lasted from 1939 to 1945.", "ground_truth": "World War II lasted from 1939 to 1945.", "should_correct": False},
                # Historical Figures (15 cases)
                {"prompt": "Napoleon Bonaparte was born in Germany.", "ground_truth": "Napoleon Bonaparte was born in Corsica.", "should_correct": True},
                {"prompt": "Albert Einstein was born in France.", "ground_truth": "Albert Einstein was born in Germany.", "should_correct": True},
                {"prompt": "Julius Caesar was the first Roman Emperor.", "ground_truth": "Augustus was the first Roman Emperor.", "should_correct": True},
                {"prompt": "Christopher Columbus discovered America in 1491.", "ground_truth": "Christopher Columbus discovered America in 1492.", "should_correct": True},
                {"prompt": "The American Civil War ended in 1864.", "ground_truth": "The American Civil War ended in 1865.", "should_correct": True},
                {"prompt": "Napoleon Bonaparte was born in Corsica.", "ground_truth": "Napoleon Bonaparte was born in Corsica.", "should_correct": False},
                {"prompt": "Albert Einstein was born in Germany.", "ground_truth": "Albert Einstein was born in Germany.", "should_correct": False},
                {"prompt": "Augustus was the first Roman Emperor.", "ground_truth": "Augustus was the first Roman Emperor.", "should_correct": False},
                {"prompt": "Christopher Columbus discovered America in 1492.", "ground_truth": "Christopher Columbus discovered America in 1492.", "should_correct": False},
                {"prompt": "The American Civil War ended in 1865.", "ground_truth": "The American Civil War ended in 1865.", "should_correct": False},
                {"prompt": "George Washington was the first US President.", "ground_truth": "George Washington was the first US President.", "should_correct": False},
                {"prompt": "Abraham Lincoln was assassinated in 1865.", "ground_truth": "Abraham Lincoln was assassinated in 1865.", "should_correct": False},
                {"prompt": "The Declaration of Independence was signed in 1776.", "ground_truth": "The Declaration of Independence was signed in 1776.", "should_correct": False},
                {"prompt": "The Berlin Wall fell in 1989.", "ground_truth": "The Berlin Wall fell in 1989.", "should_correct": False},
                {"prompt": "The Soviet Union dissolved in 1991.", "ground_truth": "The Soviet Union dissolved in 1991.", "should_correct": False},
            ],
            
            "technology": [
                # Programming Languages (10 cases)
                {"prompt": "Python is a compiled programming language.", "ground_truth": "Python is an interpreted programming language.", "should_correct": True},
                {"prompt": "JavaScript is a compiled programming language.", "ground_truth": "JavaScript is an interpreted programming language.", "should_correct": True},
                {"prompt": "Java is an interpreted programming language.", "ground_truth": "Java is a compiled programming language.", "should_correct": True},
                {"prompt": "C++ is an interpreted programming language.", "ground_truth": "C++ is a compiled programming language.", "should_correct": True},
                {"prompt": "Python is an interpreted programming language.", "ground_truth": "Python is an interpreted programming language.", "should_correct": False},
                {"prompt": "JavaScript is an interpreted programming language.", "ground_truth": "JavaScript is an interpreted programming language.", "should_correct": False},
                {"prompt": "Java is a compiled programming language.", "ground_truth": "Java is a compiled programming language.", "should_correct": False},
                {"prompt": "C++ is a compiled programming language.", "ground_truth": "C++ is a compiled programming language.", "should_correct": False},
                {"prompt": "HTML is a markup language.", "ground_truth": "HTML is a markup language.", "should_correct": False},
                {"prompt": "CSS is a styling language.", "ground_truth": "CSS is a styling language.", "should_correct": False},
                # Technology Facts (10 cases)
                {"prompt": "Bitcoin is a traditional currency.", "ground_truth": "Bitcoin is a digital cryptocurrency.", "should_correct": True},
                {"prompt": "The Internet was invented in the 1990s.", "ground_truth": "The Internet was invented in the 1960s-1970s.", "should_correct": True},
                {"prompt": "The first computer was invented in 1950.", "ground_truth": "The first computer was invented in the 1940s.", "should_correct": True},
                {"prompt": "HTTP stands for HyperText Transfer Protocol.", "ground_truth": "HTTP stands for HyperText Transfer Protocol.", "should_correct": False},
                {"prompt": "URL stands for Uniform Resource Locator.", "ground_truth": "URL stands for Uniform Resource Locator.", "should_correct": False},
                {"prompt": "TCP/IP is a network protocol.", "ground_truth": "TCP/IP is a network protocol.", "should_correct": False},
                {"prompt": "WiFi stands for Wireless Fidelity.", "ground_truth": "WiFi stands for Wireless Fidelity.", "should_correct": False},
                {"prompt": "GPS stands for Global Positioning System.", "ground_truth": "GPS stands for Global Positioning System.", "should_correct": False},
                {"prompt": "USB stands for Universal Serial Bus.", "ground_truth": "USB stands for Universal Serial Bus.", "should_correct": False},
                {"prompt": "RAM stands for Random Access Memory.", "ground_truth": "RAM stands for Random Access Memory.", "should_correct": False},
            ],
            
            "medicine": [
                # Human Anatomy (10 cases)
                {"prompt": "The human heart has three chambers.", "ground_truth": "The human heart has four chambers.", "should_correct": True},
                {"prompt": "Humans have 205 bones.", "ground_truth": "Humans have 206 bones.", "should_correct": True},
                {"prompt": "The human brain has two hemispheres.", "ground_truth": "The human brain has two hemispheres.", "should_correct": False},
                {"prompt": "Humans have 32 teeth.", "ground_truth": "Humans have 32 teeth.", "should_correct": False},
                {"prompt": "The human spine has 33 vertebrae.", "ground_truth": "The human spine has 33 vertebrae.", "should_correct": False},
                {"prompt": "Humans have 12 pairs of ribs.", "ground_truth": "Humans have 12 pairs of ribs.", "should_correct": False},
                {"prompt": "The human heart has four chambers.", "ground_truth": "The human heart has four chambers.", "should_correct": False},
                {"prompt": "Humans have 206 bones.", "ground_truth": "Humans have 206 bones.", "should_correct": False},
                {"prompt": "The human body has 5 senses.", "ground_truth": "The human body has 5 senses.", "should_correct": False},
                {"prompt": "Blood is pumped by the heart.", "ground_truth": "Blood is pumped by the heart.", "should_correct": False},
                # Medical Facts (10 cases)
                {"prompt": "The common cold is caused by bacteria.", "ground_truth": "The common cold is caused by viruses.", "should_correct": True},
                {"prompt": "Insulin is produced by the liver.", "ground_truth": "Insulin is produced by the pancreas.", "should_correct": True},
                {"prompt": "Antibiotics are effective against viruses.", "ground_truth": "Antibiotics are effective against bacteria.", "should_correct": True},
                {"prompt": "Insulin is produced by the pancreas.", "ground_truth": "Insulin is produced by the pancreas.", "should_correct": False},
                {"prompt": "The common cold is caused by viruses.", "ground_truth": "The common cold is caused by viruses.", "should_correct": False},
                {"prompt": "Antibiotics are effective against bacteria.", "ground_truth": "Antibiotics are effective against bacteria.", "should_correct": False},
                {"prompt": "Vaccines help prevent diseases.", "ground_truth": "Vaccines help prevent diseases.", "should_correct": False},
                {"prompt": "DNA contains genetic information.", "ground_truth": "DNA contains genetic information.", "should_correct": False},
                {"prompt": "Red blood cells carry oxygen.", "ground_truth": "Red blood cells carry oxygen.", "should_correct": False},
                {"prompt": "The liver detoxifies the body.", "ground_truth": "The liver detoxifies the body.", "should_correct": False},
            ],
            
            "astronomy": [
                # Solar System (10 cases)
                {"prompt": "The sun rises in the west.", "ground_truth": "The sun rises in the east.", "should_correct": True},
                {"prompt": "The Moon orbits around Mars.", "ground_truth": "The Moon orbits around Earth.", "should_correct": True},
                {"prompt": "Earth is the second planet from the Sun.", "ground_truth": "Earth is the third planet from the Sun.", "should_correct": True},
                {"prompt": "Mars is known as the Blue Planet.", "ground_truth": "Earth is known as the Blue Planet.", "should_correct": True},
                {"prompt": "The sun rises in the east.", "ground_truth": "The sun rises in the east.", "should_correct": False},
                {"prompt": "The Moon orbits around Earth.", "ground_truth": "The Moon orbits around Earth.", "should_correct": False},
                {"prompt": "Earth is the third planet from the Sun.", "ground_truth": "Earth is the third planet from the Sun.", "should_correct": False},
                {"prompt": "Mars is known as the Red Planet.", "ground_truth": "Mars is known as the Red Planet.", "should_correct": False},
                {"prompt": "Jupiter is the largest planet.", "ground_truth": "Jupiter is the largest planet.", "should_correct": False},
                {"prompt": "Saturn has rings.", "ground_truth": "Saturn has rings.", "should_correct": False},
                # Space Facts (5 cases)
                {"prompt": "Light travels at 300,000 km/s.", "ground_truth": "Light travels at approximately 300,000 km/s.", "should_correct": False},
                {"prompt": "The Milky Way is our galaxy.", "ground_truth": "The Milky Way is our galaxy.", "should_correct": False},
                {"prompt": "A year on Earth is 365 days.", "ground_truth": "A year on Earth is 365 days.", "should_correct": False},
                {"prompt": "The Sun is a star.", "ground_truth": "The Sun is a star.", "should_correct": False},
                {"prompt": "Space is a vacuum.", "ground_truth": "Space is a vacuum.", "should_correct": False},
            ]
        }
    
    def run_comprehensive_test(self):
        """Run comprehensive test with 100+ cases."""
        print("🧪 COMPREHENSIVE LARGE-SCALE AKGC TEST")
        print("=" * 70)
        print("Testing 100+ cases across 6 domains for production validation")
        
        # Initialize AKGC
        print("\n🚀 Initializing AKGC System...")
        self.akgc = UltraOptimizedAKGC()
        print("✅ AKGC initialized successfully!")
        
        # Count total test cases
        total_cases = sum(len(cases) for cases in self.test_cases.values())
        print(f"\n📊 Total test cases: {total_cases}")
        
        # Run tests by domain
        all_results = []
        domain_stats = {}
        total_time = 0
        
        for domain, cases in self.test_cases.items():
            print(f"\n🔍 Testing {domain.upper()} domain ({len(cases)} cases)")
            print("-" * 50)
            
            domain_results = []
            domain_time = 0
            correct_predictions = 0
            
            for i, case in enumerate(cases, 1):
                if i % 10 == 0 or i == len(cases):
                    print(f"   Progress: {i}/{len(cases)} cases completed")
                
                try:
                    start_time = time.time()
                    response, factual, hvi = self.akgc.ultra_fast_correction(case['prompt'])
                    processing_time = time.time() - start_time
                    
                    domain_time += processing_time
                    total_time += processing_time
                    
                    # Calculate metrics
                    accuracy = compute_accuracy(response, case['ground_truth'])
                    rouge_l = compute_rouge_l(response, case['ground_truth'])
                    bertscore = compute_bertscore(response, case['ground_truth'])
                    
                    # Check correction behavior
                    was_corrected = not factual
                    should_correct = case['should_correct']
                    prediction_correct = (was_corrected == should_correct)
                    
                    if prediction_correct:
                        correct_predictions += 1
                    
                    result = {
                        "domain": domain,
                        "case_id": i,
                        "prompt": case['prompt'],
                        "response": response,
                        "ground_truth": case['ground_truth'],
                        "should_correct": should_correct,
                        "was_corrected": was_corrected,
                        "prediction_correct": prediction_correct,
                        "accuracy": accuracy,
                        "rouge_l": rouge_l,
                        "bertscore": bertscore,
                        "hvi": hvi,
                        "processing_time_ms": processing_time * 1000
                    }
                    
                    domain_results.append(result)
                    all_results.append(result)
                    
                except Exception as e:
                    print(f"   ❌ Error in case {i}: {e}")
                    error_result = {
                        "domain": domain,
                        "case_id": i,
                        "prompt": case['prompt'],
                        "error": str(e),
                        "prediction_correct": False,
                        "processing_time_ms": 0
                    }
                    domain_results.append(error_result)
                    all_results.append(error_result)
            
            # Domain statistics
            domain_accuracy = correct_predictions / len(cases) if cases else 0
            avg_domain_time = (domain_time / len(cases)) * 1000 if cases else 0
            avg_response_accuracy = sum(r.get('accuracy', 0) for r in domain_results) / len(domain_results) if domain_results else 0
            
            domain_stats[domain] = {
                "total_cases": len(cases),
                "correct_predictions": correct_predictions,
                "prediction_accuracy": domain_accuracy,
                "avg_response_accuracy": avg_response_accuracy,
                "avg_processing_time_ms": avg_domain_time,
                "results": domain_results
            }
            
            print(f"   ✅ {domain.upper()} completed:")
            print(f"      Prediction accuracy: {domain_accuracy:.1%}")
            print(f"      Avg response accuracy: {avg_response_accuracy:.3f}")
            print(f"      Avg processing time: {avg_domain_time:.1f}ms")
        
        # Overall statistics
        total_correct_predictions = sum(r.get('prediction_correct', False) for r in all_results)
        overall_prediction_accuracy = total_correct_predictions / len(all_results) if all_results else 0
        overall_response_accuracy = sum(r.get('accuracy', 0) for r in all_results) / len(all_results) if all_results else 0
        avg_processing_time = (total_time / len(all_results)) * 1000 if all_results else 0
        
        # Performance analysis
        latency_target_met = sum(1 for r in all_results if r.get('processing_time_ms', 1000) < 300)
        high_accuracy_cases = sum(1 for r in all_results if r.get('accuracy', 0) >= 0.8)
        
        print(f"\n" + "=" * 70)
        print("🏆 COMPREHENSIVE TEST RESULTS")
        print("=" * 70)
        
        print(f"\n📊 Overall Performance:")
        print(f"   Total test cases: {len(all_results)}")
        print(f"   Prediction accuracy: {overall_prediction_accuracy:.1%}")
        print(f"   Average response accuracy: {overall_response_accuracy:.3f}")
        print(f"   Average processing time: {avg_processing_time:.1f}ms")
        print(f"   Cases meeting latency target (<300ms): {latency_target_met}/{len(all_results)} ({latency_target_met/len(all_results)*100:.1f}%)")
        print(f"   High accuracy cases (≥0.8): {high_accuracy_cases}/{len(all_results)} ({high_accuracy_cases/len(all_results)*100:.1f}%)")
        
        print(f"\n📈 Domain Breakdown:")
        for domain, stats in domain_stats.items():
            print(f"   {domain.upper()}: {stats['prediction_accuracy']:.1%} prediction accuracy, {stats['avg_response_accuracy']:.3f} response accuracy, {stats['avg_processing_time_ms']:.1f}ms avg")
        
        # Target assessment
        latency_success = avg_processing_time < 300
        accuracy_success = overall_prediction_accuracy >= 0.9 and overall_response_accuracy >= 0.8
        scale_success = len(all_results) >= 100
        
        print(f"\n🎯 Target Assessment:")
        print(f"   Latency target (<300ms): {'✅ MET' if latency_success else '❌ NOT MET'} - {avg_processing_time:.1f}ms")
        print(f"   Accuracy target (≥90% prediction, ≥80% response): {'✅ MET' if accuracy_success else '❌ NOT MET'}")
        print(f"   Scale target (≥100 cases): {'✅ MET' if scale_success else '❌ NOT MET'} - {len(all_results)} cases")
        
        overall_success = latency_success and accuracy_success and scale_success
        print(f"\n🏆 Overall Status: {'🎉 ALL TARGETS MET!' if overall_success else '⚠️ SOME TARGETS NOT MET'}")
        
        # Save comprehensive results
        comprehensive_results = {
            "timestamp": time.time(),
            "total_cases": len(all_results),
            "overall_success": overall_success,
            "metrics": {
                "prediction_accuracy": overall_prediction_accuracy,
                "response_accuracy": overall_response_accuracy,
                "avg_processing_time_ms": avg_processing_time,
                "latency_target_met_ratio": latency_target_met / len(all_results),
                "high_accuracy_ratio": high_accuracy_cases / len(all_results)
            },
            "domain_stats": domain_stats,
            "target_assessment": {
                "latency_success": latency_success,
                "accuracy_success": accuracy_success,
                "scale_success": scale_success
            },
            "detailed_results": all_results
        }
        
        # Save results
        os.makedirs("results", exist_ok=True)
        with open("results/comprehensive_large_scale_test.json", "w") as f:
            json.dump(comprehensive_results, f, indent=2, default=str)
        
        print(f"\n💾 Comprehensive results saved to: results/comprehensive_large_scale_test.json")
        
        return comprehensive_results

def main():
    """Main test function."""
    try:
        tester = ComprehensiveLargeScaleTest()
        results = tester.run_comprehensive_test()
        
        if results['overall_success']:
            print("\n🎉 SUCCESS: Large-scale comprehensive test passed!")
            print("   - All performance targets achieved")
            print("   - 100+ test cases validated")
            print("   - Production-ready system confirmed")
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