#!/usr/bin/env python3
"""
Enhanced Knowledge Graph Utilities with Better Network Handling
- Improved error handling and retries
- Alternative data sources
- Better user agent and headers
- Offline-first approach with graceful degradation
"""

import requests
import json
import os
import time
from typing import List, Dict, Optional

class EnhancedKGManager:
    """Enhanced Knowledge Graph Manager with robust fetching capabilities."""
    
    def __init__(self, cache_path="models/cache/enhanced_kg_cache.json"):
        self.cache_path = cache_path
        self.cache = self.load_cache()
        self.session = self.create_session()
        
        # Enhanced hardcoded knowledge base
        self.enhanced_facts_db = self.load_enhanced_facts_db()
        
    def create_session(self):
        """Create a requests session with proper headers and timeouts."""
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'AKGC-Research-Tool/1.0 (https://github.com/research/akgc; research@example.com)',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9'
        })
        return session
    
    def load_cache(self) -> Dict:
        """Load existing cache or create empty one."""
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
        
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, "r", encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[KG] Warning: Could not load cache: {e}")
        
        return {}
    
    def save_cache(self):
        """Save cache to disk."""
        try:
            with open(self.cache_path, "w", encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[KG] Warning: Could not save cache: {e}")
    
    def load_enhanced_facts_db(self) -> Dict:
        """Load enhanced facts database with more comprehensive coverage."""
        return {
            # Geography - Countries and Cities
            "France": [
                "France is a country in Western Europe.",
                "The capital of France is Paris.",
                "France is known for its culture, cuisine, and landmarks like the Eiffel Tower.",
                "France is a member of the European Union and NATO."
            ],
            "India": [
                "India is a country in South Asia.",
                "The capital of India is New Delhi.",
                "India is the world's largest democracy and second most populous country.",
                "India gained independence from British rule in 1947."
            ],
            "USA": [
                "The United States is a country in North America.",
                "The capital of the USA is Washington D.C.",
                "The USA consists of 50 states and various territories.",
                "The USA is known for its diverse culture and economic power."
            ],
            "China": [
                "China is a country in East Asia.",
                "The capital of China is Beijing.",
                "China is the world's most populous country.",
                "China has the world's second-largest economy."
            ],
            "Japan": [
                "Japan is an island country in East Asia.",
                "The capital of Japan is Tokyo.",
                "Japan is known for its technology and cultural exports.",
                "Japan consists of four main islands: Honshu, Hokkaido, Kyushu, and Shikoku."
            ],
            "Russia": [
                "Russia is the largest country in the world by land area.",
                "The capital of Russia is Moscow.",
                "Russia spans eleven time zones.",
                "Russia is located in both Europe and Asia."
            ],
            "Germany": [
                "Germany is a country in Central Europe.",
                "The capital of Germany is Berlin.",
                "Germany is the most populous member state of the European Union.",
                "Germany is known for its engineering and automotive industry."
            ],
            
            # Cities
            "Paris": [
                "Paris is the capital and largest city of France.",
                "Paris is known as the 'City of Light'.",
                "Famous landmarks include the Eiffel Tower and Louvre Museum.",
                "Paris is located on the Seine River."
            ],
            "Tokyo": [
                "Tokyo is the capital of Japan.",
                "Tokyo is one of the world's most populous metropolitan areas.",
                "Tokyo hosted the Summer Olympics in 1964 and 2021.",
                "Tokyo is a major global financial center."
            ],
            "London": [
                "London is the capital and largest city of England and the United Kingdom.",
                "London is a major global city and financial center.",
                "Famous landmarks include Big Ben and the Tower of London.",
                "London is located on the River Thames."
            ],
            "Beijing": [
                "Beijing is the capital of China.",
                "Beijing is one of the most populous cities in the world.",
                "Beijing hosted the Summer Olympics in 2008 and Winter Olympics in 2022.",
                "Beijing is the political and cultural center of China."
            ],
            
            # Science - Elements and Compounds
            "Water": [
                "Water is a chemical compound with the formula H2O.",
                "Water is essential for all known forms of life.",
                "Water exists in three states: solid (ice), liquid (water), and gas (vapor).",
                "Water covers about 71% of Earth's surface."
            ],
            "Oxygen": [
                "Oxygen is a chemical element with symbol O and atomic number 8.",
                "Oxygen is essential for respiration in most living organisms.",
                "Oxygen makes up about 21% of Earth's atmosphere.",
                "Oxygen was discovered independently by Carl Wilhelm Scheele and Joseph Priestley."
            ],
            "Gold": [
                "Gold is a chemical element with symbol Au and atomic number 79.",
                "Gold is a precious metal known for its resistance to corrosion.",
                "Gold has been used as currency and jewelry for thousands of years.",
                "Gold is highly valued for its rarity and beauty."
            ],
            "Silver": [
                "Silver is a chemical element with symbol Ag and atomic number 47.",
                "Silver is known for its high electrical and thermal conductivity.",
                "Silver has antimicrobial properties.",
                "Silver has been used in coins, jewelry, and photography."
            ],
            "Iron": [
                "Iron is a chemical element with symbol Fe and atomic number 26.",
                "Iron is the most common element on Earth by mass.",
                "Iron is essential for human health as part of hemoglobin.",
                "Iron is the primary component of steel."
            ],
            
            # History - Wars and Events
            "World War II": [
                "World War II lasted from 1939 to 1945.",
                "World War II was the deadliest conflict in human history.",
                "The war ended with the surrender of Japan in September 1945.",
                "World War II involved most of the world's nations."
            ],
            "World War I": [
                "World War I lasted from 1914 to 1918.",
                "World War I was also known as the Great War.",
                "The war ended with the Armistice of Compiègne on November 11, 1918.",
                "World War I resulted in significant political changes in Europe."
            ],
            
            # Historical Figures
            "Napoleon Bonaparte": [
                "Napoleon Bonaparte was a French military and political leader.",
                "Napoleon was Emperor of France from 1804 to 1814.",
                "Napoleon was born in Corsica in 1769.",
                "Napoleon is considered one of the greatest military commanders in history."
            ],
            "Albert Einstein": [
                "Albert Einstein was a German-born theoretical physicist.",
                "Einstein developed the theory of relativity.",
                "Einstein won the Nobel Prize in Physics in 1921.",
                "Einstein was born in Ulm, Germany in 1879."
            ],
            "Julius Caesar": [
                "Julius Caesar was a Roman general and statesman.",
                "Caesar played a critical role in the events that led to the demise of the Roman Republic.",
                "Caesar was assassinated on the Ides of March (March 15) in 44 BC.",
                "Augustus, not Julius Caesar, was the first Roman Emperor."
            ],
            
            # Technology
            "Python": [
                "Python is an interpreted programming language.",
                "Python was created by Guido van Rossum and first released in 1991.",
                "Python is known for its simplicity and readability.",
                "Python is widely used in web development, data science, and artificial intelligence."
            ],
            "Bitcoin": [
                "Bitcoin is a decentralized digital cryptocurrency.",
                "Bitcoin was created in 2009 by an unknown person using the pseudonym Satoshi Nakamoto.",
                "Bitcoin operates on a peer-to-peer network without a central authority.",
                "Bitcoin transactions are recorded on a public ledger called a blockchain."
            ],
            "Quantum Computing": [
                "Quantum computing uses quantum mechanical phenomena to process information.",
                "Quantum computers can potentially solve certain problems exponentially faster than classical computers.",
                "Quantum computing is still in early stages of development.",
                "Major tech companies are investing heavily in quantum computing research."
            ],
            
            # Medicine and Biology
            "Heart": [
                "The human heart has four chambers: two atria and two ventricles.",
                "The heart pumps blood through the circulatory system.",
                "The heart beats approximately 100,000 times per day.",
                "Heart disease is a leading cause of death worldwide."
            ],
            "Insulin": [
                "Insulin is a hormone produced by the beta cells of the pancreas.",
                "Insulin helps regulate blood glucose levels.",
                "Insulin was discovered by Frederick Banting and Charles Best in 1921.",
                "Diabetes occurs when the body cannot produce or properly use insulin."
            ],
            "Common Cold": [
                "The common cold is caused by viruses, not bacteria.",
                "Rhinoviruses are the most common cause of the common cold.",
                "There is no cure for the common cold, only symptom management.",
                "The common cold is highly contagious and spreads through respiratory droplets."
            ],
            
            # Astronomy
            "Sun": [
                "The Sun is the star at the center of our solar system.",
                "The Sun rises in the east and sets in the west.",
                "The Sun is approximately 4.6 billion years old.",
                "The Sun's energy comes from nuclear fusion in its core."
            ],
            "Moon": [
                "The Moon is Earth's only natural satellite.",
                "The Moon orbits around the Earth.",
                "The Moon influences Earth's tides through gravitational forces.",
                "The Moon was likely formed from debris after a Mars-sized object collided with Earth."
            ],
            "Earth": [
                "Earth is the third planet from the Sun.",
                "Earth is the only known planet with life.",
                "Earth has one natural satellite, the Moon.",
                "Earth's atmosphere is composed of approximately 78% nitrogen and 21% oxygen."
            ]
        }
    
    def fetch_wikipedia_with_retry(self, query: str, max_retries: int = 2) -> Optional[List[str]]:
        """Attempt to fetch from Wikipedia with retries and better error handling."""
        
        for attempt in range(max_retries):
            try:
                print(f"[KG] Attempt {attempt + 1}/{max_retries}: Searching Wikipedia for '{query}'")
                
                # Try search API first
                search_url = "https://en.wikipedia.org/w/api.php"
                search_params = {
                    'action': 'query',
                    'list': 'search',
                    'srsearch': query,
                    'format': 'json',
                    'srlimit': 1
                }
                
                search_response = self.session.get(search_url, params=search_params, timeout=5)
                
                if search_response.status_code == 200:
                    search_data = search_response.json()
                    
                    if search_data.get('query', {}).get('search'):
                        best_title = search_data['query']['search'][0]['title']
                        print(f"[KG] Found Wikipedia page: '{best_title}'")
                        
                        # Try to get page summary
                        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{best_title.replace(' ', '_')}"
                        
                        summary_response = self.session.get(summary_url, timeout=5)
                        
                        if summary_response.status_code == 200:
                            summary_data = summary_response.json()
                            facts = []
                            
                            if "extract" in summary_data and summary_data["extract"]:
                                # Clean and truncate extract
                                extract = summary_data["extract"].strip()
                                if len(extract) > 300:
                                    extract = extract[:300] + "..."
                                facts.append(extract)
                            
                            if "description" in summary_data and summary_data["description"]:
                                facts.append(f"Description: {summary_data['description']}")
                            
                            if facts:
                                print(f"[KG] Successfully fetched {len(facts)} facts from Wikipedia")
                                return facts
                        else:
                            print(f"[KG] Wikipedia summary failed: HTTP {summary_response.status_code}")
                    else:
                        print(f"[KG] No Wikipedia search results for '{query}'")
                else:
                    print(f"[KG] Wikipedia search failed: HTTP {search_response.status_code}")
                    
            except requests.exceptions.Timeout:
                print(f"[KG] Wikipedia request timed out (attempt {attempt + 1})")
            except requests.exceptions.ConnectionError:
                print(f"[KG] Wikipedia connection failed (attempt {attempt + 1})")
            except Exception as e:
                print(f"[KG] Wikipedia error (attempt {attempt + 1}): {e}")
            
            if attempt < max_retries - 1:
                time.sleep(1)  # Brief delay before retry
        
        print(f"[KG] All Wikipedia attempts failed for '{query}'")
        return None
    
    def get_enhanced_facts(self, query: str) -> List[str]:
        """Get facts from enhanced database with fuzzy matching."""
        
        # Exact match first
        if query in self.enhanced_facts_db:
            return self.enhanced_facts_db[query]
        
        # Case-insensitive match
        for key, facts in self.enhanced_facts_db.items():
            if query.lower() == key.lower():
                return facts
        
        # Partial matching for common variations
        query_lower = query.lower()
        for key, facts in self.enhanced_facts_db.items():
            key_lower = key.lower()
            if (query_lower in key_lower or key_lower in query_lower) and len(key_lower) > 3:
                return facts
        
        # No match found
        return [f"Information about {query} is not available in the knowledge base."]
    
    def fetch_kg_data(self, query: str) -> List[str]:
        """
        Main method to fetch knowledge graph data with multiple fallback strategies.
        
        Strategy:
        1. Check cache first
        2. Try enhanced facts database
        3. Attempt Wikipedia fetch (with retries)
        4. Fall back to enhanced facts if Wikipedia fails
        5. Cache and return results
        """
        
        # Check cache first
        if query in self.cache:
            print(f"[KG] Cache hit for '{query}'")
            return self.cache[query]
        
        print(f"[KG] Fetching data for new entity: '{query}'")
        
        # Check if we have enhanced facts for this entity
        enhanced_facts = self.get_enhanced_facts(query)
        has_enhanced_facts = not any("not available" in fact.lower() for fact in enhanced_facts)
        
        if has_enhanced_facts:
            print(f"[KG] Using enhanced facts database for '{query}'")
            facts = enhanced_facts
        else:
            print(f"[KG] Attempting Wikipedia fetch for '{query}'")
            # Try Wikipedia fetch
            wikipedia_facts = self.fetch_wikipedia_with_retry(query)
            
            if wikipedia_facts:
                # Combine Wikipedia facts with any relevant enhanced facts
                facts = wikipedia_facts + enhanced_facts[:1]  # Add fallback message
                print(f"[KG] Successfully fetched from Wikipedia")
            else:
                # Fall back to enhanced facts (even if it's just the "not available" message)
                facts = enhanced_facts
                print(f"[KG] Using fallback facts for '{query}'")
        
        # Cache the results
        self.cache[query] = facts
        self.save_cache()
        
        return facts

# Global instance for backward compatibility
_enhanced_kg_manager = None

def get_enhanced_kg_manager():
    """Get or create the global enhanced KG manager instance."""
    global _enhanced_kg_manager
    if _enhanced_kg_manager is None:
        _enhanced_kg_manager = EnhancedKGManager()
    return _enhanced_kg_manager

def fetch_kg_data(query, cache_path="models/cache/kg_cache.json"):
    """Enhanced fetch function with better error handling and fallbacks."""
    manager = get_enhanced_kg_manager()
    return manager.fetch_kg_data(query)

def get_hardcoded_facts(query):
    """Get enhanced hardcoded facts."""
    manager = get_enhanced_kg_manager()
    return manager.get_enhanced_facts(query)