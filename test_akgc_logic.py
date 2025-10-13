#!/usr/bin/env python3
"""
Test AKGC logic without requiring model downloads
"""
import sys
sys.path.insert(0, 'src')

from utils.kg_utils import fetch_kg_data, get_hardcoded_facts
from akgc_algorithm import extract_entity, normalize_entity_name, generate_contextual_facts

def test_kg_utils():
    """Test KG utility functions"""
    print("=" * 60)
    print("Testing KG Utils")
    print("=" * 60)
    
    # Test hardcoded facts
    print("\n1. Testing hardcoded facts for France:")
    facts = get_hardcoded_facts("France")
    for fact in facts:
        print(f"   - {fact}")
    
    print("\n2. Testing hardcoded facts for India:")
    facts = get_hardcoded_facts("India")
    for fact in facts:
        print(f"   - {fact}")
    
    print("\n3. Testing hardcoded facts for Oxygen:")
    facts = get_hardcoded_facts("Oxygen")
    for fact in facts:
        print(f"   - {fact}")

def test_entity_extraction():
    """Test entity extraction"""
    print("\n" + "=" * 60)
    print("Testing Entity Extraction")
    print("=" * 60)
    
    test_cases = [
        "The capital of France is Florida.",
        "Water is made of hydrogen and oxygen.",
        "World War II ended in 1945.",
        "The capital of India is Mumbai.",
        "Oxygen has atomic number 8.",
        "Napoleon was born in Corsica.",
        "The sun rises in the east."
    ]
    
    for prompt in test_cases:
        entity = extract_entity(prompt)
        normalized = normalize_entity_name(entity)
        print(f"\nPrompt: {prompt}")
        print(f"   Entity: {entity} -> Normalized: {normalized}")

def test_contextual_facts():
    """Test contextual fact generation"""
    print("\n" + "=" * 60)
    print("Testing Contextual Facts Generation")
    print("=" * 60)
    
    test_cases = [
        ("The capital of France is Florida.", "France"),
        ("World War II ended in 1945.", "World War II"),
        ("Oxygen has atomic number 8.", "Oxygen"),
        ("The capital of India is Mumbai.", "India"),
    ]
    
    for prompt, entity in test_cases:
        print(f"\nPrompt: {prompt}")
        print(f"Entity: {entity}")
        facts = generate_contextual_facts(prompt, entity)
        if facts:
            print("Generated Facts:")
            for fact in facts:
                print(f"   - {fact}")
        else:
            print("   (No contextual facts generated)")

def test_kg_fetch():
    """Test KG data fetching with caching"""
    print("\n" + "=" * 60)
    print("Testing KG Data Fetching (with caching)")
    print("=" * 60)
    
    entities = ["France", "India", "Oxygen", "World War II"]
    
    for entity in entities:
        print(f"\n{entity}:")
        try:
            facts = fetch_kg_data(entity)
            for i, fact in enumerate(facts[:3], 1):  # Show first 3 facts
                print(f"   {i}. {fact[:100]}..." if len(fact) > 100 else f"   {i}. {fact}")
        except Exception as e:
            print(f"   Error: {e}")

if __name__ == "__main__":
    print("AKGC Logic Testing Suite")
    print("=" * 60)
    
    try:
        test_kg_utils()
        test_entity_extraction()
        test_contextual_facts()
        test_kg_fetch()
        
        print("\n" + "=" * 60)
        print("All tests completed successfully!")
        print("=" * 60)
    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()
