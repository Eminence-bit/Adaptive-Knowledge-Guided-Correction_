from rouge_score import rouge_scorer
from bert_score import score
from scipy.spatial.distance import cosine

def compute_accuracy(response, ground_truth):
    """Compute accuracy based on exact match."""
    return 1.0 if response.strip().lower() == ground_truth.strip().lower() else 0.0

def compute_rouge_l(response, ground_truth):
    """Compute ROUGE-L score."""
    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
    scores = scorer.score(ground_truth, response)
    return scores["rougeL"].fmeasure

def compute_bertscore(response, ground_truth):
    """Compute BERTScore."""
    P, R, F1 = score([response], [ground_truth], lang="en", model_type="distilbert-base-uncased")
    return F1.item()

def compute_hvi(similarity, kg_facts, output_text):
    """
    Compute Hallucination Vulnerability Index (HVI).
    
    HVI is computed as a weighted combination of:
    - Context similarity (how well the output matches the input context)
    - Knowledge grounding (how well the output is supported by knowledge graph facts)
    
    Higher HVI = more factual, lower risk of hallucination
    Lower HVI = higher risk of hallucination
    
    Args:
        similarity: Context similarity score (0-1)
        kg_facts: List of knowledge graph facts
        output_text: Generated output text
    
    Returns:
        HVI score between 0 and 1
    """
    output_lower = output_text.lower()
    
    # Compute knowledge grounding score with partial matching
    kg_score = 0.0
    if kg_facts:
        # Check for exact substring matches
        exact_matches = sum(1 for fact in kg_facts if fact.lower() in output_lower)
        
        # Check for partial matches (key terms from facts present in output)
        partial_matches = 0
        for fact in kg_facts:
            # Extract key words from fact (excluding common words)
            fact_words = set(word.lower() for word in fact.split() 
                           if len(word) > 3 and word.lower() not in 
                           ['the', 'is', 'are', 'was', 'were', 'been', 'have', 'has', 'had'])
            output_words = set(word.lower() for word in output_text.split())
            
            # Calculate overlap
            overlap = len(fact_words & output_words)
            if overlap > 0:
                partial_matches += overlap / max(len(fact_words), 1)
        
        # Normalize scores
        max_exact = len(kg_facts)
        max_partial = len(kg_facts)
        
        exact_score = min(exact_matches / max_exact, 1.0) if max_exact > 0 else 0.0
        partial_score = min(partial_matches / max_partial, 1.0) if max_partial > 0 else 0.0
        
        # Weight exact matches more heavily than partial matches
        kg_score = 0.7 * exact_score + 0.3 * partial_score
    else:
        # No KG facts available, assume medium confidence
        kg_score = 0.5
    
    # Compute final HVI as weighted combination
    # Higher weight on KG grounding for factual accuracy
    hvi = 0.4 * similarity + 0.6 * kg_score
    
    return hvi