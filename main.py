import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
import requests
from scipy.spatial.distance import cosine
import torch

# Load lightweight model
model = AutoModelForCausalLM.from_pretrained("distilgpt2")
tokenizer = AutoTokenizer.from_pretrained("distilgpt2")

# Use mixed precision for efficiency
model = model.to(device="cuda" if torch.cuda.is_available() else "cpu")
model.eval()

def fetch_kg_data(query, api_url="https://api.wikipedia.org"):
    # Placeholder: Fetch facts from Wikipedia or similar API
    try:
        response = requests.get(api_url, params={"query": query}, timeout=5)
        return response.json().get("facts", [])
    except:
        return []

def compute_context_similarity(input_text, output_text):
    # Encode texts for context comparison
    input_ids = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512).to(model.device)
    output_ids = tokenizer(output_text, return_tensors="pt", truncation=True, max_length=512).to(model.device)
    with torch.no_grad():
        input_emb = model(**input_ids).last_hidden_state.mean(dim=1).cpu().numpy()
        output_emb = model(**output_ids).last_hidden_state.mean(dim=1).cpu().numpy()
    return 1 - cosine(input_emb[0], output_emb[0])

def compute_hvi(similarity, kg_facts, output_text):
    # Hallucination Vulnerability Index: Combine context drift and KG alignment
    kg_score = 1.0 if any(fact in output_text for fact in kg_facts) else 0.5
    return 0.6 * similarity + 0.4 * kg_score  # Weighted combination

def adaptive_correction(prompt, sim_threshold=0.8, hvi_threshold=0.7):
    # Generate initial response
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512).to(model.device)
    with torch.no_grad():
        output = model.generate(**inputs, max_length=50, num_return_sequences=1)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    
    # Compute context similarity
    similarity = compute_context_similarity(prompt, response)
    
    # Fetch KG facts
    kg_facts = fetch_kg_data(prompt)
    
    # Compute HVI
    hvi = compute_hvi(similarity, kg_facts, response)
    
    if hvi < hvi_threshold:
        # Correct using KG facts
        corrected_prompt = f"{prompt} Based on facts: {', '.join(kg_facts[:3])}"
        inputs = tokenizer(corrected_prompt, return_tensors="pt", truncation=True, max_length=512).to(model.device)
        with torch.no_grad():
            output = model.generate(**inputs, max_length=50)
        response = tokenizer.decode(output[0], skip_special_tokens=True)
        return response, False, hvi
    return response, True, hvi

# Example usage
prompt = "The capital of France is flower."
response, is_factual, hvi = adaptive_correction(prompt)
print(f"Response: {response}\nFactual: {is_factual}\nHVI: {hvi:.2f}")