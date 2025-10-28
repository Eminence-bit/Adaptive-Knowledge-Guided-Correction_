#!/usr/bin/env python3
"""
Comprehensive Production API Test Suite
Tests the finalized AKGC API with examples from multiple domains
"""

import requests
import json
import time
import threading
import subprocess
import sys
from typing import Dict, List, Optional

class AKGCAPITester:
    """Comprehensive API tester for production AKGC system."""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.server_process = None
        
    def start_api_server(self) -> bool:
        """Start the API server in background."""
        try:
            print("🚀 Starting AKGC API Server...")
            self.server_process = subprocess.Popen(
                [sys.executable, "src/api_server.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for server to start
            max_attempts = 30
            for attempt in range(max_attempts):
                try:
                    response = requests.get(f"{self.base_url}/health", timeout=2)
                    if response.status_code == 200:
                        print("✅ API Server started successfully!")
                        return True
                except requests.exceptions.RequestException:
                    pass
                
                time.sleep(1)
                print(f"   Waiting for server... ({attempt + 1}/{max_attempts})")
            
            print("❌ Failed to start API server")
            return False
            
        except Exception as e:
            print(f"❌ Error starting server: {e}")
            return False
    
    def stop_api_server(self):
        """Stop the API server."""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
            print("🛑 API Server stopped")
    
    def test_health_endpoint(self) -> Dict:
        """Test the health check endpoint."""
        print("\n🏥 Testing Health Endpoint")
        print("-" * 40)
        
        try:
            response = requests.get(f"{self.base_url}/health")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check passed")
                print(f"   Status: {data.get('status')}")
                print(f"   Model loaded: {data.get('model_loaded')}")
                print(f"   Device: {data.get('device')}")
                return {"success": True, "data": data}
            else:
                print(f"❌ Health check failed: HTTP {response.status_code}")
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return {"success": False, "error": str(e)}
    
    def test_single_detection(self) -> Dict:
        """Test single text detection with comprehensive examples."""
        print("\n🔍 Testing Single Text Detection")
        print("-" * 40)
        
        # Comprehensive test cases from multiple domains
        test_cases = [
            # Geography
            {
                "text": "The capital of France is London.",
                "domain": "Geography",
                "expected_correction": True,
                "description": "Incorrect capital city"
            },
            {
                "text": "Tokyo is the capital of China.",
                "domain": "Geography", 
                "expected_correction": True,
                "description": "Wrong capital assignment"
            },
            {
                "text": "The capital of India is New Delhi.",
                "domain": "Geography",
                "expected_correction": False,
                "description": "Correct capital city"
            },
            
            # Science
            {
                "text": "The chemical symbol for gold is Ag.",
                "domain": "Science",
                "expected_correction": True,
                "description": "Wrong chemical symbol"
            },
            {
                "text": "Water is composed of hydrogen and oxygen.",
                "domain": "Science",
                "expected_correction": False,
                "description": "Correct chemical composition"
            },
            {
                "text": "The chemical symbol for oxygen is O.",
                "domain": "Science",
                "expected_correction": False,
                "description": "Correct chemical symbol"
            },
            
            # History
            {
                "text": "World War II ended in 1944.",
                "domain": "History",
                "expected_correction": True,
                "description": "Wrong end date"
            },
            {
                "text": "Napoleon Bonaparte was born in Germany.",
                "domain": "History",
                "expected_correction": True,
                "description": "Wrong birthplace"
            },
            {
                "text": "World War II ended in 1945.",
                "domain": "History",
                "expected_correction": False,
                "description": "Correct historical date"
            },
            
            # Technology
            {
                "text": "Python is a compiled programming language.",
                "domain": "Technology",
                "expected_correction": True,
                "description": "Wrong language type"
            },
            {
                "text": "Bitcoin is a traditional currency.",
                "domain": "Technology",
                "expected_correction": True,
                "description": "Wrong currency type"
            },
            {
                "text": "Python is an interpreted programming language.",
                "domain": "Technology",
                "expected_correction": False,
                "description": "Correct language type"
            },
            
            # Medicine
            {
                "text": "The human heart has three chambers.",
                "domain": "Medicine",
                "expected_correction": True,
                "description": "Wrong anatomy fact"
            },
            {
                "text": "The common cold is caused by bacteria.",
                "domain": "Medicine",
                "expected_correction": True,
                "description": "Wrong cause"
            },
            {
                "text": "The human heart has four chambers.",
                "domain": "Medicine",
                "expected_correction": False,
                "description": "Correct anatomy fact"
            },
            
            # Astronomy
            {
                "text": "The sun rises in the west.",
                "domain": "Astronomy",
                "expected_correction": True,
                "description": "Wrong direction"
            },
            {
                "text": "The Moon orbits around Mars.",
                "domain": "Astronomy",
                "expected_correction": True,
                "description": "Wrong orbital relationship"
            },
            {
                "text": "The sun rises in the east.",
                "domain": "Astronomy",
                "expected_correction": False,
                "description": "Correct astronomical fact"
            }
        ]
        
        results = []
        successful_tests = 0
        correct_predictions = 0
        total_processing_time = 0
        
        for i, case in enumerate(test_cases, 1):
            print(f"\n  Test {i}/{len(test_cases)}: {case['domain']} - {case['description']}")
            print(f"  Text: \"{case['text']}\"")
            
            try:
                start_time = time.time()
                response = requests.post(
                    f"{self.base_url}/detect",
                    json={"text": case["text"], "threshold": 0.7},
                    timeout=10
                )
                request_time = time.time() - start_time
                total_processing_time += request_time
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Check if correction behavior matches expectation
                    needs_correction = data.get("needs_correction", False)
                    was_corrected = case["text"] != data.get("corrected_text", case["text"])
                    expected_correction = case["expected_correction"]
                    
                    prediction_correct = (needs_correction == expected_correction) or (was_corrected == expected_correction)
                    
                    if prediction_correct:
                        correct_predictions += 1
                    
                    result = {
                        "test_id": i,
                        "domain": case["domain"],
                        "original_text": case["text"],
                        "corrected_text": data.get("corrected_text"),
                        "expected_correction": expected_correction,
                        "needs_correction": needs_correction,
                        "was_corrected": was_corrected,
                        "prediction_correct": prediction_correct,
                        "hvi": data.get("hvi"),
                        "processing_time": data.get("processing_time"),
                        "request_time": request_time,
                        "performance_target_met": data.get("performance_target_met", False)
                    }
                    
                    results.append(result)
                    successful_tests += 1
                    
                    print(f"     Original: {case['text']}")
                    print(f"     Corrected: {data.get('corrected_text')}")
                    print(f"     Expected correction: {expected_correction}")
                    print(f"     Needs correction: {needs_correction}")
                    print(f"     HVI: {data.get('hvi', 0):.3f}")
                    print(f"     Processing time: {data.get('processing_time', 0)*1000:.1f}ms")
                    print(f"     Result: {'✅ CORRECT' if prediction_correct else '❌ INCORRECT'}")
                    
                else:
                    print(f"     ❌ API Error: HTTP {response.status_code}")
                    results.append({
                        "test_id": i,
                        "domain": case["domain"],
                        "error": f"HTTP {response.status_code}",
                        "prediction_correct": False
                    })
                    
            except Exception as e:
                print(f"     ❌ Request Error: {e}")
                results.append({
                    "test_id": i,
                    "domain": case["domain"],
                    "error": str(e),
                    "prediction_correct": False
                })
        
        # Summary
        avg_processing_time = total_processing_time / len(test_cases) if test_cases else 0
        accuracy = correct_predictions / len(test_cases) if test_cases else 0
        
        print(f"\n📊 Single Detection Test Summary:")
        print(f"   Total tests: {len(test_cases)}")
        print(f"   Successful requests: {successful_tests}")
        print(f"   Correct predictions: {correct_predictions}")
        print(f"   Accuracy: {accuracy:.1%}")
        print(f"   Average request time: {avg_processing_time*1000:.1f}ms")
        
        return {
            "success": successful_tests == len(test_cases),
            "accuracy": accuracy,
            "total_tests": len(test_cases),
            "successful_tests": successful_tests,
            "correct_predictions": correct_predictions,
            "avg_processing_time": avg_processing_time,
            "results": results
        }
    
    def test_batch_detection(self) -> Dict:
        """Test batch detection functionality."""
        print("\n📦 Testing Batch Detection")
        print("-" * 40)
        
        batch_texts = [
            "The capital of France is London.",
            "Water is composed of hydrogen and oxygen.",
            "World War II ended in 1944.",
            "Python is an interpreted programming language.",
            "The sun rises in the west."
        ]
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{self.base_url}/batch_detect",
                json={"texts": batch_texts, "threshold": 0.7},
                timeout=30
            )
            request_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"✅ Batch processing successful")
                print(f"   Total processed: {data.get('total_processed')}")
                print(f"   Processing time: {data.get('processing_time', 0)*1000:.1f}ms")
                print(f"   Avg time per text: {data.get('avg_time_per_text', 0)*1000:.1f}ms")
                print(f"   Request time: {request_time*1000:.1f}ms")
                
                # Show sample results
                results = data.get('results', [])
                print(f"\n   Sample results:")
                for i, result in enumerate(results[:3], 1):
                    print(f"     {i}. \"{result.get('original_text', '')[:50]}...\"")
                    print(f"        → \"{result.get('corrected_text', '')[:50]}...\"")
                    print(f"        HVI: {result.get('hvi', 0):.3f}")
                
                return {
                    "success": True,
                    "total_processed": data.get('total_processed'),
                    "processing_time": data.get('processing_time'),
                    "avg_time_per_text": data.get('avg_time_per_text'),
                    "request_time": request_time,
                    "results": results
                }
            else:
                print(f"❌ Batch detection failed: HTTP {response.status_code}")
                return {"success": False, "error": f"HTTP {response.status_code}"}
                
        except Exception as e:
            print(f"❌ Batch detection error: {e}")
            return {"success": False, "error": str(e)}
    
    def test_evaluation_endpoint(self) -> Dict:
        """Test the evaluation endpoint with ground truth."""
        print("\n📏 Testing Evaluation Endpoint")
        print("-" * 40)
        
        test_cases = [
            {
                "text": "The capital of France is London.",
                "ground_truth": "The capital of France is Paris.",
                "description": "Geography correction"
            },
            {
                "text": "The chemical symbol for gold is Ag.",
                "ground_truth": "The chemical symbol for gold is Au.",
                "description": "Science correction"
            },
            {
                "text": "Python is an interpreted programming language.",
                "ground_truth": "Python is an interpreted programming language.",
                "description": "Technology (correct)"
            }
        ]
        
        results = []
        successful_tests = 0
        
        for i, case in enumerate(test_cases, 1):
            print(f"\n  Test {i}/{len(test_cases)}: {case['description']}")
            
            try:
                response = requests.post(
                    f"{self.base_url}/evaluate",
                    json={
                        "text": case["text"],
                        "ground_truth": case["ground_truth"],
                        "threshold": 0.7
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    metrics = data.get("metrics", {})
                    
                    result = {
                        "test_id": i,
                        "description": case["description"],
                        "original_text": case["text"],
                        "corrected_text": data.get("corrected_text"),
                        "ground_truth": case["ground_truth"],
                        "hvi": data.get("hvi"),
                        "accuracy": metrics.get("accuracy"),
                        "rouge_l": metrics.get("rouge_l"),
                        "bertscore": metrics.get("bertscore"),
                        "processing_time": data.get("processing_time")
                    }
                    
                    results.append(result)
                    successful_tests += 1
                    
                    print(f"     Accuracy: {metrics.get('accuracy', 0):.3f}")
                    print(f"     ROUGE-L: {metrics.get('rouge_l', 0):.3f}")
                    print(f"     BERTScore: {metrics.get('bertscore', 0):.3f}")
                    print(f"     HVI: {data.get('hvi', 0):.3f}")
                    print(f"     Processing: {data.get('processing_time', 0)*1000:.1f}ms")
                    print(f"     ✅ Success")
                    
                else:
                    print(f"     ❌ API Error: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"     ❌ Request Error: {e}")
        
        avg_accuracy = sum(r.get("accuracy", 0) for r in results) / len(results) if results else 0
        avg_rouge = sum(r.get("rouge_l", 0) for r in results) / len(results) if results else 0
        avg_bertscore = sum(r.get("bertscore", 0) for r in results) / len(results) if results else 0
        
        print(f"\n📊 Evaluation Test Summary:")
        print(f"   Successful tests: {successful_tests}/{len(test_cases)}")
        print(f"   Average accuracy: {avg_accuracy:.3f}")
        print(f"   Average ROUGE-L: {avg_rouge:.3f}")
        print(f"   Average BERTScore: {avg_bertscore:.3f}")
        
        return {
            "success": successful_tests == len(test_cases),
            "successful_tests": successful_tests,
            "total_tests": len(test_cases),
            "avg_accuracy": avg_accuracy,
            "avg_rouge_l": avg_rouge,
            "avg_bertscore": avg_bertscore,
            "results": results
        }
    
    def test_config_endpoints(self) -> Dict:
        """Test configuration endpoints."""
        print("\n⚙️ Testing Configuration Endpoints")
        print("-" * 40)
        
        try:
            # Test GET config
            print("  Testing GET /config...")
            response = requests.get(f"{self.base_url}/config")
            
            if response.status_code == 200:
                config_data = response.json()
                print(f"     ✅ GET config successful")
                print(f"     Device: {config_data.get('device')}")
                print(f"     KG cache size: {config_data.get('kg_cache_size')}")
                
                # Test POST config (update)
                print("  Testing POST /config...")
                update_response = requests.post(
                    f"{self.base_url}/config",
                    json={"hvi_threshold": 0.75}
                )
                
                if update_response.status_code == 200:
                    update_data = update_response.json()
                    print(f"     ✅ POST config successful")
                    print(f"     Message: {update_data.get('message')}")
                    
                    return {
                        "success": True,
                        "get_config": config_data,
                        "update_config": update_data
                    }
                else:
                    print(f"     ❌ POST config failed: HTTP {update_response.status_code}")
                    return {"success": False, "error": f"POST failed: {update_response.status_code}"}
            else:
                print(f"     ❌ GET config failed: HTTP {response.status_code}")
                return {"success": False, "error": f"GET failed: {response.status_code}"}
                
        except Exception as e:
            print(f"     ❌ Config test error: {e}")
            return {"success": False, "error": str(e)}
    
    def run_comprehensive_test(self) -> Dict:
        """Run all API tests comprehensively."""
        print("🧪 COMPREHENSIVE AKGC PRODUCTION API TEST")
        print("=" * 60)
        
        # Start server
        if not self.start_api_server():
            return {"success": False, "error": "Failed to start API server"}
        
        try:
            # Run all tests
            health_result = self.test_health_endpoint()
            single_result = self.test_single_detection()
            batch_result = self.test_batch_detection()
            eval_result = self.test_evaluation_endpoint()
            config_result = self.test_config_endpoints()
            
            # Overall assessment
            all_tests_passed = all([
                health_result.get("success", False),
                single_result.get("success", False),
                batch_result.get("success", False),
                eval_result.get("success", False),
                config_result.get("success", False)
            ])
            
            print(f"\n" + "=" * 60)
            print("🏆 COMPREHENSIVE TEST RESULTS")
            print("=" * 60)
            
            print(f"\n✅ Health Check: {'PASS' if health_result.get('success') else 'FAIL'}")
            print(f"✅ Single Detection: {'PASS' if single_result.get('success') else 'FAIL'}")
            if single_result.get("success"):
                print(f"   - Accuracy: {single_result.get('accuracy', 0):.1%}")
                print(f"   - Avg processing: {single_result.get('avg_processing_time', 0)*1000:.1f}ms")
            
            print(f"✅ Batch Detection: {'PASS' if batch_result.get('success') else 'FAIL'}")
            if batch_result.get("success"):
                print(f"   - Avg per text: {batch_result.get('avg_time_per_text', 0)*1000:.1f}ms")
            
            print(f"✅ Evaluation: {'PASS' if eval_result.get('success') else 'FAIL'}")
            if eval_result.get("success"):
                print(f"   - Avg accuracy: {eval_result.get('avg_accuracy', 0):.3f}")
                print(f"   - Avg ROUGE-L: {eval_result.get('avg_rouge_l', 0):.3f}")
            
            print(f"✅ Configuration: {'PASS' if config_result.get('success') else 'FAIL'}")
            
            print(f"\n🎯 Overall Status: {'🎉 ALL TESTS PASSED!' if all_tests_passed else '⚠️ SOME TESTS FAILED'}")
            
            return {
                "success": all_tests_passed,
                "health_test": health_result,
                "single_detection_test": single_result,
                "batch_detection_test": batch_result,
                "evaluation_test": eval_result,
                "config_test": config_result
            }
            
        finally:
            # Always stop the server
            self.stop_api_server()

def main():
    """Main test function."""
    tester = AKGCAPITester()
    
    try:
        results = tester.run_comprehensive_test()
        
        # Save results
        with open("results/production_api_test_results.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n💾 Test results saved to: results/production_api_test_results.json")
        
        return results.get("success", False)
        
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
        tester.stop_api_server()
        return False
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        tester.stop_api_server()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)