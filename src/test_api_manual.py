#!/usr/bin/env python3
"""
Manual API Test - Quick validation of production API
"""

import requests
import json
import time

def test_api_endpoints():
    """Test API endpoints manually."""
    base_url = "http://localhost:5000"
    
    print("🧪 Manual AKGC Production API Test")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Health: {data}")
        else:
            print(f"   ❌ Health failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Health error: {e}")
    
    # Test 2: Single Detection - Multiple Domains
    print("\n2. Testing Single Detection...")
    
    test_cases = [
        {
            "text": "The capital of France is London.",
            "domain": "Geography",
            "expected": "Should correct to Paris"
        },
        {
            "text": "The chemical symbol for gold is Ag.",
            "domain": "Science", 
            "expected": "Should correct to Au"
        },
        {
            "text": "World War II ended in 1944.",
            "domain": "History",
            "expected": "Should correct to 1945"
        },
        {
            "text": "Python is a compiled programming language.",
            "domain": "Technology",
            "expected": "Should correct to interpreted"
        },
        {
            "text": "The human heart has three chambers.",
            "domain": "Medicine",
            "expected": "Should correct to four"
        },
        {
            "text": "The sun rises in the west.",
            "domain": "Astronomy",
            "expected": "Should correct to east"
        },
        {
            "text": "The capital of France is Paris.",
            "domain": "Geography (Correct)",
            "expected": "Should not correct"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n   Test {i}: {case['domain']}")
        print(f"   Input: \"{case['text']}\"")
        print(f"   Expected: {case['expected']}")
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{base_url}/detect",
                json={"text": case["text"], "threshold": 0.7},
                timeout=10
            )
            request_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"   Output: \"{data.get('corrected_text')}\"")
                print(f"   HVI: {data.get('hvi', 0):.3f}")
                print(f"   Needs correction: {data.get('needs_correction')}")
                print(f"   Processing time: {data.get('processing_time', 0)*1000:.1f}ms")
                print(f"   Request time: {request_time*1000:.1f}ms")
                print(f"   Performance target met: {data.get('performance_target_met')}")
                print(f"   ✅ Success")
            else:
                print(f"   ❌ Failed: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test 3: Batch Detection
    print("\n3. Testing Batch Detection...")
    batch_texts = [
        "The capital of France is London.",
        "Water is H2O.",
        "World War II ended in 1944."
    ]
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{base_url}/batch_detect",
            json={"texts": batch_texts, "threshold": 0.7},
            timeout=15
        )
        request_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Batch Success")
            print(f"   Total processed: {data.get('total_processed')}")
            print(f"   Processing time: {data.get('processing_time', 0)*1000:.1f}ms")
            print(f"   Avg per text: {data.get('avg_time_per_text', 0)*1000:.1f}ms")
            print(f"   Request time: {request_time*1000:.1f}ms")
        else:
            print(f"   ❌ Batch failed: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Batch error: {e}")
    
    # Test 4: Evaluation
    print("\n4. Testing Evaluation...")
    try:
        response = requests.post(
            f"{base_url}/evaluate",
            json={
                "text": "The capital of France is London.",
                "ground_truth": "The capital of France is Paris.",
                "threshold": 0.7
            },
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            metrics = data.get("metrics", {})
            print(f"   ✅ Evaluation Success")
            print(f"   Accuracy: {metrics.get('accuracy', 0):.3f}")
            print(f"   ROUGE-L: {metrics.get('rouge_l', 0):.3f}")
            print(f"   BERTScore: {metrics.get('bertscore', 0):.3f}")
        else:
            print(f"   ❌ Evaluation failed: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Evaluation error: {e}")
    
    # Test 5: Configuration
    print("\n5. Testing Configuration...")
    try:
        # Get config
        response = requests.get(f"{base_url}/config", timeout=5)
        if response.status_code == 200:
            config_data = response.json()
            print(f"   ✅ Get Config Success")
            print(f"   Device: {config_data.get('device')}")
            print(f"   KG cache size: {config_data.get('kg_cache_size')}")
        else:
            print(f"   ❌ Get config failed: HTTP {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Config error: {e}")
    
    print(f"\n🎉 Manual API test completed!")

if __name__ == "__main__":
    test_api_endpoints()