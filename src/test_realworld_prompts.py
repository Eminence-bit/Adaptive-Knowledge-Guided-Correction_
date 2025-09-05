#!/usr/bin/env python3
"""
Real-World Prompt Testing for AKGC Algorithm
Tests against diverse, realistic prompts from various domains
"""

import time
import json
from akgc_algorithm import load_config, load_model, load_llm, adaptive_correction
from utils.metrics import compute_accuracy, compute_rouge_l, compute_bertscore

def load_realworld_test_cases():
    """Load comprehensive real-world test cases."""
    return {
        "geography": [
            {
                "prompt": "The capital of France is London.",
                "ground_truth": "The capital of France is Paris.",
                "domain": "Geography",
                "expected_correction": True
            },
            {
                "prompt": "Tokyo is the capital of China.",
                "ground_truth": "Beijing is the capital of China.",
                "domain": "Geography",
                "expected_correction": True
            },
            {
                "prompt": "The largest country in the world is Canada.",
                "ground_truth": "Russia is the largest country in the world.",
                "domain": "Geography",
                "expected_correction": True
            },
            {
                "prompt": "The Nile River flows through Egypt.",
                "ground_truth": "The Nile River flows through Egypt.",
                "domain": "Geography",
                "expected_correction": False
            }
        ],
        "science": [
            {
                "prompt": "Water is composed of hydrogen and oxygen atoms.",
                "ground_truth": "Water is composed of hydrogen and oxygen atoms.",
                "domain": "Science",
                "expected_correction": False
            },
            {
                "prompt": "The chemical symbol for gold is Ag.",
                "ground_truth": "The chemical symbol for gold is Au.",
                "domain": "Science",
                "expected_correction": True
            },
            {
                "prompt": "The Earth orbits around the Moon.",
                "ground_truth": "The Moon orbits around the Earth.",
                "domain": "Science",
                "expected_correction": True
            },
            {
                "prompt": "Photosynthesis occurs in plant leaves.",
                "ground_truth": "Photosynthesis occurs in plant leaves.",
                "domain": "Science",
                "expected_correction": False
            }
        ],
        "history": [
            {
                "prompt": "World War II ended in 1945.",
                "ground_truth": "World War II ended in 1945.",
                "domain": "History",
                "expected_correction": False
            },
            {
                "prompt": "Napoleon Bonaparte was born in Germany.",
                "ground_truth": "Napoleon Bonaparte was born in Corsica.",
                "domain": "History",
                "expected_correction": True
            },
            {
                "prompt": "The American Civil War lasted from 1861 to 1865.",
                "ground_truth": "The American Civil War lasted from 1861 to 1865.",
                "domain": "History",
                "expected_correction": False
            },
            {
                "prompt": "Julius Caesar was the first Roman Emperor.",
                "ground_truth": "Augustus was the first Roman Emperor.",
                "domain": "History",
                "expected_correction": True
            }
        ],
        "medicine": [
            {
                "prompt": "The human heart has three chambers.",
                "ground_truth": "The human heart has four chambers.",
                "domain": "Medicine",
                "expected_correction": True
            },
            {
                "prompt": "Insulin is produced by the pancreas.",
                "ground_truth": "Insulin is produced by the pancreas.",
                "domain": "Medicine",
                "expected_correction": False
            },
            {
                "prompt": "The common cold is caused by bacteria.",
                "ground_truth": "The common cold is caused by viruses.",
                "domain": "Medicine",
                "expected_correction": True
            }
        ],
        "technology": [
            {
                "prompt": "Python is a compiled programming language.",
                "ground_truth": "Python is an interpreted programming language.",
                "domain": "Technology",
                "expected_correction": True
            },
            {
                "prompt": "HTTP stands for HyperText Transfer Protocol.",
                "ground_truth": "HTTP stands for HyperText Transfer Protocol.",
                "domain": "Technology",
                "expected_correction": False
            },
            {
                "prompt": "Machine learning requires internet connection to work.",
                "ground_truth": "Machine learning can work offline once trained.",
                "domain": "Technology",
                "expected_correction": True
            }
        ],
        "general_knowledge": [
            {
                "prompt": "The sun rises in the west.",
                "ground_truth": "The sun rises in the east.",
                "domain": "General Knowledge",
                "expected_correction": True
            },
            {
                "prompt": "Shakespeare wrote Romeo and Juliet.",
                "ground_truth": "Shakespeare wrote Romeo and Juliet.",
                "domain": "General Knowledge",
                "expected_correction": False
            },
            {
                "prompt": "The speed of light is 300,000 km/s.",
                "ground_truth": "The speed of light is approximately 300,000 km/s.",
                "domain": "General Knowledge",
                "expected_correction": False
            }
        ]
    }

def test_akgc_on_realworld_prompts():
    """Test AKGC algorithm on real-world prompts."""
    print("🌍 Testing AKGC on Real-World Prompts")
    print("=" * 60)
    
    # Load models
    print("Loading models...")
    config = load_config()
    device = "cpu"  # Force CPU for compatibility
    model, tokenizer = load_model(config["model"], device)
    llm, llm_tokenizer = load_llm(device)
    print("✅ Models loaded successfully!")
    
    # Load test cases
    test_cases = load_realworld_test_cases()
    
    # Results storage
    all_results = []
    domain_results = {}
    
    total_tests = sum(len(cases) for cases in test_cases.values())
    print(f"\n📊 Running {total_tests} real-world test cases...")
    print("=" * 60)
    
    for domain, cases in test_cases.items():
        print(f"\n🔍 Testing {domain} domain ({len(cases)} cases)...")
        domain_results[domain] = {
            "total": len(cases),
            "corrected": 0,
            "accuracy": 0.0,
            "avg_hvi": 0.0,
            "avg_rouge": 0.0,
            "avg_bert": 0.0,
            "cases": []
        }
        
        for i, case in enumerate(cases, 1):
            print(f"\n  Test {i}/{len(cases)}: {case['prompt'][:50]}...")
            
            start_time = time.time()
            
            try:
                # Run AKGC
                response, factual, hvi = adaptive_correction(
                    model, tokenizer, llm, llm_tokenizer, 
                    case['prompt'], device,
                    sim_threshold=0.8, hvi_threshold=0.7
                )
                
                processing_time = time.time() - start_time
                
                # Compute metrics
                accuracy = compute_accuracy(response, case['ground_truth'])
                rouge_l = compute_rouge_l(response, case['ground_truth'])
                bertscore = compute_bertscore(response, case['ground_truth'])
                
                # Determine if correction was applied
                was_corrected = not factual
                correction_expected = case['expected_correction']
                correction_correct = (was_corrected == correction_expected)
                
                # Store results
                result = {
                    "prompt": case['prompt'],
                    "response": response,
                    "ground_truth": case['ground_truth'],
                    "domain": case['domain'],
                    "expected_correction": correction_expected,
                    "was_corrected": was_corrected,
                    "correction_correct": correction_correct,
                    "factual": factual,
                    "hvi": hvi,
                    "accuracy": accuracy,
                    "rouge_l": rouge_l,
                    "bertscore": bertscore,
                    "processing_time": processing_time
                }
                
                all_results.append(result)
                domain_results[domain]["cases"].append(result)
                
                # Update domain statistics
                if was_corrected:
                    domain_results[domain]["corrected"] += 1
                
                # Print result
                print(f"    Response: {response[:80]}...")
                print(f"    Factual: {factual} | HVI: {hvi:.3f} | Corrected: {was_corrected}")
                print(f"    Accuracy: {accuracy:.3f} | ROUGE-L: {rouge_l:.3f} | BERTScore: {bertscore:.3f}")
                print(f"    Correction Expected: {correction_expected} | Correction Correct: {correction_correct}")
                
            except Exception as e:
                print(f"    ❌ Error: {e}")
                result = {
                    "prompt": case['prompt'],
                    "response": "ERROR",
                    "ground_truth": case['ground_truth'],
                    "domain": case['domain'],
                    "error": str(e),
                    "factual": False,
                    "hvi": 0.0,
                    "accuracy": 0.0,
                    "rouge_l": 0.0,
                    "bertscore": 0.0,
                    "processing_time": 0.0
                }
                all_results.append(result)
                domain_results[domain]["cases"].append(result)
        
        # Calculate domain statistics
        if domain_results[domain]["cases"]:
            domain_results[domain]["accuracy"] = sum(r["accuracy"] for r in domain_results[domain]["cases"]) / len(domain_results[domain]["cases"])
            domain_results[domain]["avg_hvi"] = sum(r["hvi"] for r in domain_results[domain]["cases"]) / len(domain_results[domain]["cases"])
            domain_results[domain]["avg_rouge"] = sum(r["rouge_l"] for r in domain_results[domain]["cases"]) / len(domain_results[domain]["cases"])
            domain_results[domain]["avg_bert"] = sum(r["bertscore"] for r in domain_results[domain]["cases"]) / len(domain_results[domain]["cases"])
    
    # Calculate overall statistics
    total_cases = len(all_results)
    successful_cases = len([r for r in all_results if "error" not in r])
    overall_accuracy = sum(r["accuracy"] for r in all_results if "error" not in r) / successful_cases if successful_cases > 0 else 0
    overall_hvi = sum(r["hvi"] for r in all_results if "error" not in r) / successful_cases if successful_cases > 0 else 0
    overall_rouge = sum(r["rouge_l"] for r in all_results if "error" not in r) / successful_cases if successful_cases > 0 else 0
    overall_bert = sum(r["bertscore"] for r in all_results if "error" not in r) / successful_cases if successful_cases > 0 else 0
    
    # Print comprehensive results
    print("\n" + "=" * 80)
    print("📈 COMPREHENSIVE REAL-WORLD TEST RESULTS")
    print("=" * 80)
    
    print(f"\n🎯 Overall Performance:")
    print(f"   Total Test Cases: {total_cases}")
    print(f"   Successful Cases: {successful_cases}")
    print(f"   Success Rate: {successful_cases/total_cases*100:.1f}%")
    print(f"   Overall Accuracy: {overall_accuracy:.3f}")
    print(f"   Overall ROUGE-L: {overall_rouge:.3f}")
    print(f"   Overall BERTScore: {overall_bert:.3f}")
    print(f"   Overall HVI: {overall_hvi:.3f}")
    
    print(f"\n📊 Domain-Specific Results:")
    for domain, stats in domain_results.items():
        print(f"\n   {domain}:")
        print(f"     Cases: {stats['total']}")
        print(f"     Corrected: {stats['corrected']} ({stats['corrected']/stats['total']*100:.1f}%)")
        print(f"     Accuracy: {stats['accuracy']:.3f}")
        print(f"     ROUGE-L: {stats['avg_rouge']:.3f}")
        print(f"     BERTScore: {stats['avg_bert']:.3f}")
        print(f"     HVI: {stats['avg_hvi']:.3f}")
    
    # Save detailed results
    results_file = "results/realworld_test_results.json"
    with open(results_file, "w") as f:
        json.dump({
            "overall_stats": {
                "total_cases": total_cases,
                "successful_cases": successful_cases,
                "success_rate": successful_cases/total_cases,
                "overall_accuracy": overall_accuracy,
                "overall_rouge_l": overall_rouge,
                "overall_bertscore": overall_bert,
                "overall_hvi": overall_hvi
            },
            "domain_results": domain_results,
            "detailed_results": all_results
        }, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: {results_file}")
    
    return all_results, domain_results

def main():
    """Main function to run real-world testing."""
    print("🚀 Starting Real-World Prompt Testing for AKGC")
    print("=" * 60)
    
    try:
        results, domain_stats = test_akgc_on_realworld_prompts()
        print("\n✅ Real-world testing completed successfully!")
        
        # Print some interesting cases
        print("\n🔍 Interesting Test Cases:")
        for result in results[:5]:  # Show first 5 results
            if "error" not in result:
                print(f"\n   Prompt: {result['prompt']}")
                print(f"   Response: {result['response']}")
                print(f"   Corrected: {result['was_corrected']} | HVI: {result['hvi']:.3f}")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
