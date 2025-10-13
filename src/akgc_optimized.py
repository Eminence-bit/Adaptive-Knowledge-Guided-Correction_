#!/usr/bin/env python3
"""
Optimized AKGC Algorithm with Enhanced Performance
- Batch processing for efficiency
- Better entity extraction
- Improved correction strategies
- Memory optimization
"""

import numpy as np
import torch
import yaml
from transformers import DistilBertModel, DistilBertTokenizer, AutoModelForCausalLM, AutoTokenizer
from utils.metrics import compute_hvi, compute_accuracy, compute_rouge_l, compute_bertscore
import requests
from torch.cuda.amp import autocast, GradScaler
import re
from typing import List, Dict, Tuple
import time

class OptimizedAKGC:
    """Optimized AKGC Algorithm with enhanced performance."""
    
    def __init__(self, config_path="src/utils/config.yaml"):
        self.config = self.load_config(config_path)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.scaler = GradScaler() if self.device == "cuda" else None
        
        # Load models
        self.model, self.tokenizer = self.load_model(self.config["model"], self.device)
        self.llm, self.llm_tokenizer = self.load_llm(self.device)
        
        # Entity extraction patterns (compiled for efficiency)
        self.entity_patterns = self.compile_entity_patterns()
        
        # Knowledge base cache
        self.kg_cache = {}
        
    def load_config(self, path):
        with open(path, "r") as f:
            return yaml.safe_load(f)
    
    def load_model(self, model_name, device):
        model = DistilBertModel.from_pretrained(model_name)
        tokenizer = DistilBertTokenizer.from_pretrained(model_name)
        model = model.to(device)
        model.eval()
        
        if device == "cuda":
            model = model.half()
        
        return model, tokenizer
    
    def load_llm(self, device):
        llm = AutoModelForCausalLM.from_pretrained("distilgpt2")
        llm_tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
        llm = llm.to(device)
        llm.eval()
        
        if device == "cuda":
            llm = llm.half()
        
        return llm, llm_tokenizer
    
    def compile_entity_patterns(self):
        """Compile regex patterns for efficient entity extraction."""
        patterns = {
            'geo': [
                re.compile(r"capital of ([A-Za-z ]+?)(?:\s+is|\s+was|\s+becomes|$)", re.IGNORECASE),
                re.compile(r"country ([A-Za-z ]+?)(?:\s+is|\s+was|\s+has|$)", re.IGNORECASE),
                re.compile(r"city ([A-Za-z ]+?)(?:\s+is|\s+was|\s+has|$)", re.IGNORECASE),
            ],
            'science': [
                re.compile(r"element ([A-Za-z ]+?)(?:\s+is|\s+has|\s+has|$)", re.IGNORECASE),
                re.compile(r"chemical ([A-Za-z ]+?)(?:\s+is|\s+has|\s+has|$)", re.IGNORECASE),
                re.compile(r"planet ([A-Za-z ]+?)(?:\s+is|\s+has|\s+has|$)", re.IGNORECASE),
            ],
            'history': [
                re.compile(r"war ([A-Za-z ]+?)(?:\s+is|\s+was|\s+ended|$)", re.IGNORECASE),
                re.compile(r"emperor ([A-Za-z ]+?)(?:\s+is|\s+was|\s+ruled|$)", re.IGNORECASE),
            ]
        }
        return patterns
    
    def extract_entity_optimized(self, prompt: str) -> str:
        """Optimized entity extraction using compiled patterns."""
        # Check for special multi-word entities first
        special_patterns = [
            (re.compile(r"World War (I{1,3}|[12])", re.IGNORECASE), "world_war"),
            (re.compile(r"Napoleon Bonaparte", re.IGNORECASE), "name"),
            (re.compile(r"Julius Caesar", re.IGNORECASE), "name"),
        ]
        
        for pattern, ptype in special_patterns:
            match = pattern.search(prompt)
            if match:
                if ptype == "world_war":
                    roman = match.group(1).upper()
                    return self.normalize_entity_name(f"World War {roman}")
                return self.normalize_entity_name(match.group(0))
        
        # Check for astronomy patterns
        if re.search(r"(?:the\s+)?sun\s+rises", prompt, re.IGNORECASE):
            return self.normalize_entity_name("Sun")
        if re.search(r"(?:the\s+)?moon\s+(?:is|orbits)", prompt, re.IGNORECASE):
            return self.normalize_entity_name("Moon")
        
        # Check for science patterns (atomic number, elements, etc.)
        science_match = re.search(r"([A-Z][a-z]+)\s+(?:is|has)\s+atomic\s+number", prompt)
        if science_match:
            return self.normalize_entity_name(science_match.group(1))
        
        science_match = re.search(r"([A-Z][a-z]+)\s+is\s+made\s+of", prompt)
        if science_match:
            return self.normalize_entity_name(science_match.group(1))
        
        # Try each pattern category
        for category, patterns in self.entity_patterns.items():
            for pattern in patterns:
                match = pattern.search(prompt)
                if match:
                    entity = match.group(1).strip()
                    entity = entity.replace("the ", "").replace("The ", "")
                    # Remove trailing verbs
                    entity = re.sub(r'\s+(is|was|has|ended|became|born).*$', '', entity, flags=re.IGNORECASE)
                    return self.normalize_entity_name(entity)
        
        # Fallback: extract first meaningful word
        words = prompt.split()
        for i, word in enumerate(words):
            # Skip common articles and prepositions
            if word.lower() in ["the", "a", "an", "of", "in", "on", "at"]:
                continue
            if word.istitle() and len(word) > 2:
                if i + 1 < len(words) and words[i + 1].istitle():
                    return self.normalize_entity_name(f"{word} {words[i + 1]}")
                return self.normalize_entity_name(word)
        
        return self.normalize_entity_name(words[0] if words else "Unknown")
    
    def normalize_entity_name(self, entity: str) -> str:
        """Normalize entity names to standard forms."""
        entity = entity.strip()
        
        # Enhanced mappings
        mappings = {
            # Geography
            "france": "France", "india": "India", "usa": "USA",
            "united states": "USA", "america": "USA", "uk": "United Kingdom",
            "united kingdom": "United Kingdom", "britain": "United Kingdom",
            "germany": "Germany", "japan": "Japan", "china": "China",
            "russia": "Russia", "brazil": "Brazil", "canada": "Canada",
            "australia": "Australia", "paris": "Paris", "london": "London",
            
            # Science
            "water": "Water", "oxygen": "Oxygen", "carbon": "Carbon",
            "hydrogen": "Hydrogen", "nitrogen": "Nitrogen", "earth": "Earth",
            "mars": "Mars", "jupiter": "Jupiter", "saturn": "Saturn", "sun": "Sun",
            
            # History
            "world war ii": "World War II", "world war 2": "World War II",
            "wwii": "World War II", "world war i": "World War I",
            "world war 1": "World War I", "wwi": "World War I",
            "napoleon": "Napoleon Bonaparte", "hitler": "Adolf Hitler",
            "caesar": "Julius Caesar"
        }
        
        entity_lower = entity.lower()
        return mappings.get(entity_lower, entity.title())
    
    def fetch_kg_data_optimized(self, entity: str) -> List[str]:
        """Optimized KG data fetching with caching."""
        if entity in self.kg_cache:
            return self.kg_cache[entity]
        
        # Import and use the fixed KG utils
        from utils.kg_utils import fetch_kg_data as kg_fetch
        facts = kg_fetch(entity)
        
        # Cache the results
        self.kg_cache[entity] = facts
        return facts
    
    def compute_context_similarity_optimized(self, input_text: str, output_text: str) -> float:
        """Optimized context similarity computation."""
        input_ids = self.tokenizer(input_text, return_tensors="pt", truncation=True, max_length=512).to(self.device)
        output_ids = self.tokenizer(output_text, return_tensors="pt", truncation=True, max_length=512).to(self.device)
        
        with torch.no_grad():
            with autocast(enabled=self.device == "cuda"):
                input_emb = self.model(**input_ids).last_hidden_state.mean(dim=1).cpu().numpy()
                output_emb = self.model(**output_ids).last_hidden_state.mean(dim=1).cpu().numpy()
        
        from scipy.spatial.distance import cosine
        return 1 - cosine(input_emb[0], output_emb[0])
    
    def generate_llm_response_optimized(self, prompt: str, max_length: int = 64) -> str:
        """Optimized LLM response generation."""
        inputs = self.llm_tokenizer(prompt, return_tensors="pt").to(self.device)
        with torch.no_grad():
            with autocast(enabled=self.device == "cuda"):
                outputs = self.llm.generate(
                    **inputs, 
                    max_length=max_length, 
                    num_return_sequences=1,
                    do_sample=True,
                    temperature=0.7,
                    pad_token_id=self.llm_tokenizer.eos_token_id
                )
        response = self.llm_tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
    
    def adaptive_correction_optimized(self, prompt: str, 
                                    sim_threshold: float = 0.8, 
                                    hvi_threshold: float = 0.7) -> Tuple[str, bool, float]:
        """Optimized adaptive correction with enhanced logic."""
        # Generate initial response
        response = self.generate_llm_response_optimized(prompt)
        
        # Compute context similarity
        similarity = self.compute_context_similarity_optimized(prompt, response)
        
        # Extract entity and fetch KG facts
        entity = self.extract_entity_optimized(prompt)
        kg_facts = self.fetch_kg_data_optimized(entity)
        
        if not kg_facts:
            kg_facts = [f"No verified facts found for {entity}."]
        
        # Compute HVI
        hvi = compute_hvi(similarity, kg_facts, response)
        
        factual = True
        
        # Check if response is semantically supported by KG facts
        stopwords = {'the', 'is', 'are', 'was', 'were', 'been', 'have', 'has', 'had', 
                    'this', 'that', 'with', 'from', 'for', 'and', 'or', 'but', 'a', 'an'}
        response_words = set(word.lower().strip('.,;:!?') for word in response.split() 
                            if len(word) > 2 and word.lower() not in stopwords)
        
        # Check if response has strong overlap with any KG fact AND no contradictions
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
        
        # Enhanced correction logic: Apply correction only if HVI is low AND no KG support
        if hvi < hvi_threshold and not kg_supports_response:
            factual = False
            
            # Smart fact selection based on prompt content
            best_fact = self.select_best_fact(prompt, kg_facts)
            if best_fact and "not available" not in best_fact.lower():
                response = best_fact
            else:
                valid_facts = [f for f in kg_facts if "not available" not in f.lower()]
                if valid_facts:
                    response = f"Based on available facts: {'. '.join(valid_facts[:2])}"
        
        return response, factual, hvi
    
    def select_best_fact(self, prompt: str, kg_facts: List[str]) -> str:
        """
        Select the most relevant fact for correction using semantic matching.
        
        This implements a multi-stage selection process:
        1. Direct keyword matching for high-priority terms
        2. Word overlap scoring
        3. Semantic relevance based on shared entities
        """
        if not kg_facts:
            return None
        
        prompt_lower = prompt.lower()
        
        # Stage 1: Priority keyword matching
        priority_keywords = {
            'capital': ['capital', 'city'],
            'element': ['element', 'atomic', 'chemical'],
            'war': ['war', 'battle', 'conflict'],
            'born': ['born', 'birth'],
            'ended': ['ended', 'finished'],
            'number': ['number', 'atomic'],
            'made': ['made', 'composed', 'consists'],
        }
        
        for key, synonyms in priority_keywords.items():
            if any(syn in prompt_lower for syn in synonyms):
                for fact in kg_facts:
                    fact_lower = fact.lower()
                    if any(syn in fact_lower for syn in synonyms):
                        return fact
        
        # Stage 2: Word overlap scoring
        prompt_words = set(word.lower() for word in prompt.split() 
                          if len(word) > 3 and word.lower() not in 
                          ['the', 'is', 'are', 'was', 'were', 'been', 'have', 'has', 'had', 'this', 'that'])
        
        best_fact = None
        best_score = 0
        
        for fact in kg_facts:
            fact_words = set(word.lower() for word in fact.split() 
                           if len(word) > 3 and word.lower() not in 
                           ['the', 'is', 'are', 'was', 'were', 'been', 'have', 'has', 'had', 'this', 'that'])
            
            overlap = len(prompt_words & fact_words)
            score = overlap / max(len(prompt_words), 1)
            
            if score > best_score:
                best_score = score
                best_fact = fact
        
        # Stage 3: Return best fact or first fact as fallback
        return best_fact if best_fact else kg_facts[0]
    
    def batch_process(self, prompts: List[str]) -> List[Dict]:
        """Process multiple prompts in batch for efficiency."""
        results = []
        
        for prompt in prompts:
            response, factual, hvi = self.adaptive_correction_optimized(prompt)
            results.append({
                "prompt": prompt,
                "response": response,
                "factual": factual,
                "hvi": hvi
            })
        
        return results

def main():
    """Test the optimized AKGC algorithm."""
    print("Initializing Optimized AKGC...")
    akgc = OptimizedAKGC()
    
    # Test cases
    test_prompts = [
        "The capital of France is Florida.",
        "Water is made of hydrogen and oxygen.",
        "World War II ended in 1945.",
        "The capital of India is Mumbai.",
        "Oxygen has atomic number 8."
    ]
    
    print("\nTesting Optimized AKGC...")
    results = akgc.batch_process(test_prompts)
    
    for result in results:
        print(f"\nPrompt: {result['prompt']}")
        print(f"Response: {result['response']}")
        print(f"Factual: {result['factual']}")
        print(f"HVI: {result['hvi']:.3f}")

if __name__ == "__main__":
    main()
