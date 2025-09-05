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
    """Compute Hallucination Vulnerability Index (HVI)."""
    kg_score = 1.0 if any(fact in output_text for fact in kg_facts) else 0.5
    return 0.6 * similarity + 0.4 * kg_score