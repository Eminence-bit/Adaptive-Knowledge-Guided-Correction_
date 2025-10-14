import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
import requests
from scipy.spatial.distance import cosine
import torch
import sys
sys.path.insert(0, 'src')

from akgc_algorithm import extract_entity
from utils.kg_utils import fetch_kg_data
from utils.metrics import compute_hvi

# Load lightweight model
model = AutoModelForCausalLM.from_pretrained("distilgpt2")
tokenizer = AutoTokenizer.from_pretrained("distilgpt2")

# Use mixed precision for efficiency
model = model.to(device="cuda" if torch.cuda.is_available() else "cpu")
model.eval()

def compute_context_similarity(input_text, output_text):
    # Encode texts for context comparison
    input_ids = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512).to(model.device)
    output_ids = tokenizer(output_text, return_tensors="pt", truncation=True, max_length=512).to(model.device)
    with torch.no_grad():
        input_emb = model(**input_ids, output_hidden_states=True).hidden_states[-1].mean(dim=1).cpu().numpy()
        output_emb = model(**output_ids, output_hidden_states=True).hidden_states[-1].mean(dim=1).cpu().numpy()
    return 1 - cosine(input_emb[0], output_emb[0])

def adaptive_correction(prompt, sim_threshold=0.8, hvi_threshold=0.7):
    # Generate initial response
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512).to(model.device)
    with torch.no_grad():
        output = model.generate(**inputs, max_length=50, num_return_sequences=1)
    original_response = tokenizer.decode(output[0], skip_special_tokens=True)
    
    # Compute context similarity
    similarity = compute_context_similarity(prompt, original_response)
    
    # Extract entity and fetch KG facts
    entity = extract_entity(prompt)
    kg_facts = fetch_kg_data(entity)
    
    # Compute HVI using the proper metrics
    hvi = compute_hvi(similarity, kg_facts, original_response)
    
    final_response = original_response
    correction_applied = False
    
    if hvi < hvi_threshold:
        # Correct using KG facts - directly use the most relevant fact
        prompt_lower = prompt.lower()
        best_fact = None
        
        # Priority-based selection of correction fact
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
        
        if not best_fact and kg_facts:
            # Fallback to first valid fact
            best_fact = next((fact for fact in kg_facts if "not available" not in fact.lower()), kg_facts[0])
        
        if best_fact:
            final_response = best_fact
            correction_applied = True
    
    return original_response, final_response, correction_applied, hvi

# Example usage
prompt = "The capital of France is flower."
original_response, final_response, correction_applied, hvi = adaptive_correction(prompt)
print(f"Prompt: {prompt}")
print(f"Original response: {original_response}")
print(f"Final response: {final_response}")
print(f"Correction applied: {correction_applied}")
print(f"HVI: {hvi:.2f}")