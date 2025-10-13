#!/usr/bin/env python3
"""
Comprehensive AKGC Test Suite
Tests the complete pipeline with mock models to avoid requiring downloads
"""
import sys
sys.path.insert(0, 'src')

import numpy as np
from utils.kg_utils import fetch_kg_data
from utils.metrics import compute_hvi
from akgc_algorithm import extract_entity, normalize_entity_name, generate_contextual_facts

def mock_similarity_score(prompt, response):
    """
    Mock context similarity computation.
    Returns high score if response is semantically related to prompt.
    """
    prompt_words = set(prompt.lower().split())
    response_words = set(response.lower().split())
    
    overlap = len(prompt_words & response_words)
    total = len(prompt_words | response_words)
    
    return overlap / total if total > 0 else 0.0

def simulate_adaptive_correction(prompt, sim_threshold=0.8, hvi_threshold=0.7):
    """
    Simulate the adaptive correction process without requiring actual models.
    This tests the core logic of the AKGC algorithm.
    """
    print(f"\n{'='*70}")
    print(f"Processing: {prompt}")
    print(f"{'='*70}")
    
    # Step 1: Extract entity
    entity = extract_entity(prompt)
    print(f"✓ Extracted entity: {entity}")
    
    # Step 2: Fetch KG facts
    kg_facts = fetch_kg_data(entity)
    print(f"✓ Retrieved {len(kg_facts)} KG facts")
    
    # Display first 2 facts
    for i, fact in enumerate(kg_facts[:2], 1):
        print(f"  {i}. {fact[:80]}..." if len(fact) > 80 else f"  {i}. {fact}")
    
    # Step 3: Check for contextual facts
    context_facts = generate_contextual_facts(prompt, entity)
    if context_facts:
        print(f"✓ Generated {len(context_facts)} contextual facts")
        for i, fact in enumerate(context_facts[:2], 1):
            print(f"  {i}. {fact[:80]}..." if len(fact) > 80 else f"  {i}. {fact}")
        # Use contextual facts if available
        kg_facts = context_facts
    
    # Step 4: Generate mock response (simulate what LLM would generate)
    # For testing, we'll use the prompt itself or a corrected version
    mock_response = prompt
    
    # Step 5: Compute mock similarity
    similarity = mock_similarity_score(prompt, mock_response)
    print(f"✓ Context similarity: {similarity:.3f}")
    
    # Step 6: Compute HVI
    hvi = compute_hvi(similarity, kg_facts, mock_response)
    print(f"✓ HVI score: {hvi:.3f}")
    
    # Step 7: Determine if correction is needed
    factual = True
    corrected_response = mock_response
    
    # Check if any KG fact semantically supports the response
    stopwords = {'the', 'is', 'are', 'was', 'were', 'been', 'have', 'has', 'had', 
                'this', 'that', 'with', 'from', 'for', 'and', 'or', 'but', 'a', 'an'}
    response_words = set(word.lower().strip('.,;:!?') for word in mock_response.split() 
                        if len(word) > 2 and word.lower() not in stopwords)
    
    kg_supports_response = False
    has_contradiction = False
    
    for fact in kg_facts:
        if "not available" in fact.lower():
            continue
        fact_words = set(word.lower().strip('.,;:!?') for word in fact.split() 
                        if len(word) > 2 and word.lower() not in stopwords)
        overlap = len(response_words & fact_words)
        overlap_ratio = overlap / max(len(response_words), 1)
        
        # Check for contradiction: if facts contain entity names not in response
        fact_entities = fact_words - response_words
        response_entities = response_words - fact_words
        
        # If we have shared context but different entities, it's a contradiction
        if overlap >= 2 and len(fact_entities) > 0 and len(response_entities) > 0:
            has_contradiction = True
        
        # If significant overlap (>60%) and no clear contradiction, consider supported
        if overlap_ratio > 0.6 and not has_contradiction:
            kg_supports_response = True
            break
    
    # Apply correction if HVI is low AND (no KG support OR has contradiction)
    if hvi < hvi_threshold and (not kg_supports_response or has_contradiction):
        factual = False
        reason = "contradiction detected" if has_contradiction else "no KG support"
        print(f"⚠ HVI below threshold ({hvi:.3f} < {hvi_threshold}) and {reason} - applying correction")
        
        # Select best fact for correction
        prompt_lower = prompt.lower()
        best_fact = None
        
        # Priority-based selection
        for fact in kg_facts:
            fact_lower = fact.lower()
            if "capital" in prompt_lower and "capital" in fact_lower:
                best_fact = fact
                break
            elif "element" in prompt_lower and "element" in fact_lower:
                best_fact = fact
                break
            elif "war" in prompt_lower and "war" in fact_lower:
                best_fact = fact
                break
            elif "atomic number" in prompt_lower and "atomic number" in fact_lower:
                best_fact = fact
                break
        
        if not best_fact:
            # Fallback to first fact
            best_fact = kg_facts[0] if kg_facts else mock_response
        
        corrected_response = best_fact
        print(f"✓ Corrected response: {corrected_response}")
    else:
        print(f"✓ Response is factual (HVI: {hvi:.3f} >= {hvi_threshold})")
    
    return {
        'prompt': prompt,
        'entity': entity,
        'response': corrected_response,
        'factual': factual,
        'hvi': hvi,
        'similarity': similarity,
        'kg_facts_count': len(kg_facts)
    }

def test_suite():
    """Run comprehensive test suite"""
    print("\n" + "="*70)
    print("AKGC COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    test_cases = [
        {
            'prompt': "The capital of France is Florida.",
            'expected_entity': "France",
            'should_correct': True,
            'expected_keyword': "Paris"
        },
        {
            'prompt': "Water is made of hydrogen and oxygen.",
            'expected_entity': "Water",
            'should_correct': False,  # This is correct
            'expected_keyword': "H2O"
        },
        {
            'prompt': "World War II ended in 1945.",
            'expected_entity': "World War II",
            'should_correct': False,  # This is correct
            'expected_keyword': "1945"
        },
        {
            'prompt': "The capital of India is Mumbai.",
            'expected_entity': "India",
            'should_correct': True,
            'expected_keyword': "New Delhi"
        },
        {
            'prompt': "Oxygen has atomic number 8.",
            'expected_entity': "Oxygen",
            'should_correct': False,  # This is correct
            'expected_keyword': "atomic number 8"
        },
        {
            'prompt': "The sun rises in the west.",
            'expected_entity': "Sun",
            'should_correct': True,
            'expected_keyword': "east"
        },
    ]
    
    results = []
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n\nTest Case {i}/{len(test_cases)}")
        result = simulate_adaptive_correction(test_case['prompt'])
        results.append(result)
        
        # Validate results
        checks = []
        
        # Check entity extraction
        if result['entity'] == test_case['expected_entity']:
            checks.append(("Entity extraction", True))
        else:
            checks.append(("Entity extraction", False))
            print(f"  ✗ Expected entity: {test_case['expected_entity']}, got: {result['entity']}")
        
        # Check if correction was applied when needed
        if test_case['should_correct']:
            if not result['factual']:
                checks.append(("Correction applied", True))
                # Check if response contains expected keyword
                if test_case['expected_keyword'].lower() in result['response'].lower():
                    checks.append(("Correct keyword", True))
                else:
                    checks.append(("Correct keyword", False))
                    print(f"  ✗ Expected keyword '{test_case['expected_keyword']}' not found in response")
            else:
                checks.append(("Correction applied", False))
                print(f"  ✗ Expected correction but none was applied")
        else:
            if result['factual']:
                checks.append(("No false correction", True))
            else:
                checks.append(("No false correction", False))
                print(f"  ✗ Unexpected correction applied to correct statement")
        
        # Check KG facts retrieved
        if result['kg_facts_count'] > 0:
            checks.append(("KG facts retrieved", True))
        else:
            checks.append(("KG facts retrieved", False))
            print(f"  ✗ No KG facts retrieved")
        
        # Evaluate test case
        all_passed = all(check[1] for check in checks)
        if all_passed:
            passed += 1
            print(f"\n✓ Test case {i} PASSED")
        else:
            failed += 1
            print(f"\n✗ Test case {i} FAILED")
            for check_name, check_result in checks:
                if not check_result:
                    print(f"  - {check_name}: FAILED")
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Total tests: {len(test_cases)}")
    print(f"Passed: {passed} ({passed/len(test_cases)*100:.1f}%)")
    print(f"Failed: {failed} ({failed/len(test_cases)*100:.1f}%)")
    print("="*70)
    
    return results, passed, failed

if __name__ == "__main__":
    try:
        results, passed, failed = test_suite()
        
        # Exit with appropriate code
        sys.exit(0 if failed == 0 else 1)
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(2)
