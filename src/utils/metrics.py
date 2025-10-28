from rouge_score import rouge_scorer
from bert_score import score
from scipy.spatial.distance import cosine

def compute_accuracy(response, ground_truth):
    """Compute accuracy based on semantic similarity and key fact matching."""
    if not response or not ground_truth:
        return 0.0
    
    response_clean = response.strip().lower()
    ground_truth_clean = ground_truth.strip().lower()
    
    # Exact match
    if response_clean == ground_truth_clean:
        return 1.0
    
    # Key fact extraction and matching
    def extract_key_facts(text):
        facts = set()
        
        # Extract capitals
        import re
        capital_match = re.search(r"capital of (\w+) is (\w+)", text, re.IGNORECASE)
        if capital_match:
            facts.add(f"capital_{capital_match.group(1).lower()}_{capital_match.group(2).lower()}")
        
        # Extract chemical symbols
        symbol_match = re.search(r"chemical symbol for (\w+) is (\w+)", text, re.IGNORECASE)
        if symbol_match:
            facts.add(f"symbol_{symbol_match.group(1).lower()}_{symbol_match.group(2).lower()}")
        
        # Extract war dates
        war_match = re.search(r"world war (\w+).*?(\d{4})", text, re.IGNORECASE)
        if war_match:
            facts.add(f"war_{war_match.group(1).lower()}_{war_match.group(2)}")
        
        # Extract birth places
        birth_match = re.search(r"(\w+(?:\s+\w+)*) was born in (\w+)", text, re.IGNORECASE)
        if birth_match:
            facts.add(f"birth_{birth_match.group(1).lower().replace(' ', '_')}_{birth_match.group(2).lower()}")
        
        # Extract heart chambers
        chamber_match = re.search(r"heart has (\w+) chamber", text, re.IGNORECASE)
        if chamber_match:
            facts.add(f"heart_chambers_{chamber_match.group(1).lower()}")
        
        # Extract programming language types
        prog_match = re.search(r"(\w+) is (?:a|an) (\w+) programming language", text, re.IGNORECASE)
        if prog_match:
            facts.add(f"language_{prog_match.group(1).lower()}_{prog_match.group(2).lower()}")
        
        # Extract sun direction
        sun_match = re.search(r"sun rises in the (\w+)", text, re.IGNORECASE)
        if sun_match:
            facts.add(f"sun_direction_{sun_match.group(1).lower()}")
        
        return facts
    
    response_facts = extract_key_facts(response)
    ground_truth_facts = extract_key_facts(ground_truth)
    
    if response_facts and ground_truth_facts:
        # Calculate fact overlap
        overlap = len(response_facts & ground_truth_facts)
        total_facts = len(ground_truth_facts)
        if total_facts > 0:
            return overlap / total_facts
    
    # Fallback to word overlap for partial credit
    response_words = set(response_clean.split())
    ground_truth_words = set(ground_truth_clean.split())
    
    # Remove common words
    stopwords = {'the', 'is', 'are', 'was', 'were', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    response_words -= stopwords
    ground_truth_words -= stopwords
    
    if len(ground_truth_words) == 0:
        return 0.0
    
    overlap = len(response_words & ground_truth_words)
    return overlap / len(ground_truth_words)

def compute_rouge_l(response, ground_truth):
    """Compute ROUGE-L score."""
    scorer = rouge_scorer.RougeScorer(["rougeL"], use_stemmer=True)
    scores = scorer.score(ground_truth, response)
    return scores["rougeL"].fmeasure

def compute_bertscore(response, ground_truth):
    """
    Compute the BERTScore F1 between a generated response and a ground-truth reference.
    
    Parameters:
        response (str): Generated text to evaluate.
        ground_truth (str): Reference text to compare against.
    
    Returns:
        float: BERTScore F1 value in the range [0.0, 1.0], where higher is better.
    """
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
        # Filter out "not available" facts
        valid_facts = [f for f in kg_facts if "not available" not in f.lower()]
        
        if not valid_facts:
            # No valid facts, assume medium confidence
            kg_score = 0.5
        else:
            # Check for exact substring matches
            exact_matches = sum(1 for fact in valid_facts if fact.lower() in output_lower)
            
            # Check for partial matches (key terms from facts present in output)
            partial_match_scores = []
            for fact in valid_facts:
                # Extract key words from fact (excluding common words)
                stopwords = {'the', 'is', 'are', 'was', 'were', 'been', 'have', 'has', 'had', 
                           'this', 'that', 'with', 'from', 'for', 'and', 'or', 'but'}
                
                fact_words = set(word.lower().strip('.,;:!?()[]{}') for word in fact.split() 
                               if len(word) > 2 and word.lower() not in stopwords)
                output_words = set(word.lower().strip('.,;:!?()[]{}') for word in output_text.split() 
                                 if len(word) > 2 and word.lower() not in stopwords)
                
                # Calculate overlap
                if len(fact_words) > 0:
                    overlap = len(fact_words & output_words)
                    overlap_ratio = overlap / len(fact_words)
                    partial_match_scores.append(overlap_ratio)
            
            # Normalize scores
            exact_score = min(exact_matches / len(valid_facts), 1.0)
            partial_score = max(partial_match_scores) if partial_match_scores else 0.0
            
            # If we have high word overlap, boost the score
            # This helps catch cases where the output is factually correct
            if partial_score > 0.5:
                # Strong partial match indicates factual content
                kg_score = 0.5 * exact_score + 0.5 * partial_score
            else:
                # Weight exact matches more heavily when partial is low
                kg_score = 0.7 * exact_score + 0.3 * partial_score
    else:
        # No KG facts available, assume medium confidence
        kg_score = 0.5
    
    # Compute final HVI as weighted combination
    # Higher weight on KG grounding for factual accuracy
    hvi = 0.4 * similarity + 0.6 * kg_score
    
    return hvi