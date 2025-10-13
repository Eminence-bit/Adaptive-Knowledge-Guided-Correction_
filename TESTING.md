# AKGC Testing Guide

## Overview
This guide explains how to run and interpret the tests for the Adaptive Knowledge-Guided Correction (AKGC) framework.

## Test Files

### 1. `test_akgc_logic.py` - Component Testing
Tests individual components of the AKGC system without requiring model downloads.

**What it tests:**
- KG utility functions (fetch_kg_data, get_hardcoded_facts)
- Entity extraction (extract_entity, normalize_entity_name)
- Contextual fact generation (generate_contextual_facts)
- Knowledge graph data caching

**How to run:**
```bash
python3 test_akgc_logic.py
```

**Expected output:**
```
AKGC Logic Testing Suite
============================================================
Testing KG Utils
============================================================
1. Testing hardcoded facts for France:
   - France is a country in Western Europe.
   - The capital of France is Paris.
   ...

============================================================
Testing Entity Extraction
============================================================
Prompt: The capital of France is Florida.
   Entity: France -> Normalized: France
...

All tests completed successfully!
```

### 2. `test_akgc_comprehensive.py` - End-to-End Testing
Tests the complete AKGC pipeline with mock responses to simulate real usage.

**What it tests:**
- Entity extraction from various prompts
- KG fact retrieval and caching
- HVI computation
- Contradiction detection
- Correction application logic
- Overall system accuracy

**How to run:**
```bash
python3 test_akgc_comprehensive.py
```

**Expected output:**
```
Test Case 1/6
======================================================================
Processing: The capital of France is Florida.
======================================================================
✓ Extracted entity: France
✓ Retrieved 3 KG facts
✓ Generated 1 contextual facts
✓ Context similarity: 1.000
✓ HVI score: 0.520
⚠ HVI below threshold (0.520 < 0.7) and contradiction detected - applying correction
✓ Corrected response: The capital of France is Paris.

✓ Test case 1 PASSED
...

======================================================================
TEST SUMMARY
======================================================================
Total tests: 6
Passed: 3 (50.0%)
Failed: 3 (50.0%)
======================================================================
```

## Test Cases Explained

### Test Case 1: Incorrect Capital (Should Correct)
```
Prompt: "The capital of France is Florida."
Expected: Correction applied
Result: ✓ PASSED
Reasoning: Contradiction detected between "Florida" and "Paris"
```

### Test Case 2: Correct Chemical Composition (Should NOT Correct)
```
Prompt: "Water is made of hydrogen and oxygen."
Expected: No correction
Result: ✗ FAILED (false correction applied)
Issue: HVI below threshold despite being factually correct
```

### Test Case 3: Correct Historical Fact (Should NOT Correct)
```
Prompt: "World War II ended in 1945."
Expected: No correction
Result: ✗ FAILED (false correction applied)
Issue: Similar to test case 2
```

### Test Case 4: Incorrect Capital (Should Correct)
```
Prompt: "The capital of India is Mumbai."
Expected: Correction applied
Result: ✓ PASSED
Reasoning: Contradiction detected between "Mumbai" and "New Delhi"
```

### Test Case 5: Correct Scientific Fact (Should NOT Correct)
```
Prompt: "Oxygen has atomic number 8."
Expected: No correction
Result: ✓ PASSED
Reasoning: Strong word overlap with KG facts supports correctness
```

### Test Case 6: Directional Error (Should Correct)
```
Prompt: "The sun rises in the west."
Expected: Correction applied
Result: ✗ FAILED (correction not applied)
Issue: "west" appears in both incorrect prompt and correct fact
```

## Understanding Test Failures

### False Corrections (Test Cases 2, 3)
**Problem:** System applies corrections to factually correct statements.

**Root Cause:** HVI threshold (0.7) is too strict. Correct statements get HVI scores around 0.5-0.6 due to:
- Lack of exact substring matches
- Partial word overlap counted with lower weight

**Mitigation:** The contradiction detection helps reduce false positives, but threshold tuning is needed.

### Missed Corrections (Test Case 6)
**Problem:** System fails to detect contradictions in directional statements.

**Root Cause:** "west" appears in both:
- Incorrect: "sun rises in the west"
- Correct: "sun sets in the west"

**Impact:** Word-level matching sees 100% overlap and marks as supported.

**Solution Needed:** Position-aware or dependency-based semantic analysis.

## Running Tests Without Internet

The tests are designed to work offline:
- Wikipedia API calls fail gracefully
- System falls back to hardcoded facts
- Caching preserves previous API results

**Note:** Initial run requires internet to fetch facts. Subsequent runs use cache.

## Performance Benchmarks

### Component Tests (test_akgc_logic.py)
- **Execution time:** ~5 seconds
- **Memory usage:** ~100 MB
- **Dependencies:** Python + basic packages (no models)

### Comprehensive Tests (test_akgc_comprehensive.py)
- **Execution time:** ~10 seconds
- **Memory usage:** ~150 MB
- **Dependencies:** Python + utils package (no models)

## Test Maintenance

### Adding New Test Cases

1. **Component Test:**
```python
# In test_akgc_logic.py
def test_new_component():
    print("\nTesting New Component")
    # Your test code
    assert result == expected
```

2. **End-to-End Test:**
```python
# In test_akgc_comprehensive.py
test_cases.append({
    'prompt': "Your test prompt",
    'expected_entity': "Expected Entity",
    'should_correct': True/False,
    'expected_keyword': "keyword to find in correction"
})
```

### Updating Test Thresholds

```python
# In test_akgc_comprehensive.py
# Adjust these values based on your requirements
sim_threshold = 0.8   # Context similarity threshold
hvi_threshold = 0.7   # HVI threshold for corrections
```

## Troubleshooting

### "Module not found" errors
```bash
# Ensure you're in the project root directory
cd /path/to/Adaptive-Knowledge-Guided-Correction_

# Run with proper path
python3 test_akgc_logic.py
```

### Tests hang or timeout
```bash
# Check for network issues (tests should work offline)
# Verify cache directory exists
mkdir -p models/cache

# Run with verbose output
python3 -v test_akgc_logic.py
```

### Inconsistent results
```bash
# Clear cache and rerun
rm -f models/cache/kg_cache.json
python3 test_akgc_comprehensive.py
```

## CI/CD Integration

### GitHub Actions Example
```yaml
name: AKGC Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run component tests
        run: python3 test_akgc_logic.py
      - name: Run comprehensive tests
        run: python3 test_akgc_comprehensive.py
```

## Future Test Improvements

1. **Unit Tests with pytest**
   - Individual function testing
   - Better assertion framework
   - Coverage reporting

2. **Integration Tests**
   - Test with actual models (CPU mode)
   - End-to-end with API calls
   - Performance benchmarking

3. **Regression Tests**
   - Store expected outputs
   - Detect unintended changes
   - Version-to-version comparison

4. **Property-Based Testing**
   - Generate random prompts
   - Verify invariants
   - Edge case discovery

## Interpreting Results

### Good HVI Scores
- **> 0.7:** Strong factual grounding, no correction needed
- **0.5 - 0.7:** Moderate confidence, check for contradictions
- **< 0.5:** Low confidence, likely needs correction

### Entity Extraction Quality
- **Exact match:** Perfect extraction
- **Normalized match:** Correct with standardization
- **Fallback used:** May indicate pattern gap

### Correction Decisions
- **Corrected with high HVI:** Likely false positive
- **Not corrected with low HVI:** Likely missed hallucination
- **Corrected with low HVI:** Likely correct decision

## Contact

For questions about testing:
- Review `IMPLEMENTATION_IMPROVEMENTS.md` for algorithm details
- Check GitHub issues for known testing limitations
- Refer to main README.md for project overview
