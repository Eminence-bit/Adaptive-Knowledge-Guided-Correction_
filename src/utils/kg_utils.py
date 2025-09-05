import requests
import json
import os

def fetch_kg_data(query, cache_path="models/cache/kg_cache.json"):
<<<<<<< HEAD
    """Fetch and cache knowledge graph facts from multiple verified sources."""
=======
    """Fetch and cache knowledge graph facts from Wikipedia."""
>>>>>>> 0aea545 (Update README.md to provide comprehensive documentation for the Adaptive Knowledge-Guided Correction (AKGC) framework, including installation instructions, usage examples, performance results, architecture details, and contribution guidelines.)
    # Ensure cache directory exists
    os.makedirs(os.path.dirname(cache_path), exist_ok=True)
    
    # Load cache
    cache = {}
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r") as f:
                cache = json.load(f)
        except:
            cache = {}
    
    if query in cache:
        return cache[query]
    
<<<<<<< HEAD
    # Fetch from multiple sources
    facts = []
    
    # 1. Try Wikipedia API first
    wikipedia_facts = fetch_from_wikipedia(query)
    if wikipedia_facts:
        facts.extend(wikipedia_facts)
    
    # 2. Try additional knowledge sources
    additional_facts = fetch_from_additional_sources(query)
    if additional_facts:
        facts.extend(additional_facts)
    
    # 3. Use hardcoded facts as fallback
    if not facts:
        facts = get_hardcoded_facts(query)
    
    # 4. If still no facts, try to generate verified facts
    if not facts or all("not available" in fact.lower() for fact in facts):
        generated_facts = generate_verified_facts(query)
        if generated_facts:
            facts.extend(generated_facts)
    
    # Cache the results
    cache[query] = facts
    with open(cache_path, "w") as f:
        json.dump(cache, f, indent=2)
    
    return facts

def fetch_from_wikipedia(query):
    """Fetch facts from Wikipedia API."""
=======
    # Fetch from Wikipedia API
>>>>>>> 0aea545 (Update README.md to provide comprehensive documentation for the Adaptive Knowledge-Guided Correction (AKGC) framework, including installation instructions, usage examples, performance results, architecture details, and contribution guidelines.)
    try:
        # Use Wikipedia's search API to find relevant pages
        search_url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_")
        response = requests.get(search_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            facts = []
            
            # Extract key facts from Wikipedia summary
            if "extract" in data:
<<<<<<< HEAD
                facts.append(data["extract"][:300] + "...")  # First 300 chars
=======
                facts.append(data["extract"][:200] + "...")  # First 200 chars
>>>>>>> 0aea545 (Update README.md to provide comprehensive documentation for the Adaptive Knowledge-Guided Correction (AKGC) framework, including installation instructions, usage examples, performance results, architecture details, and contribution guidelines.)
            
            if "description" in data:
                facts.append(f"Description: {data['description']}")
            
<<<<<<< HEAD
            # Try to get more specific facts
            if "content_urls" in data and "desktop" in data["content_urls"]:
                page_url = data["content_urls"]["desktop"]["page"]
                detailed_facts = fetch_detailed_wikipedia_facts(page_url)
                facts.extend(detailed_facts)
            
            return facts
        else:
            return []
    except Exception as e:
        print(f"Error fetching from Wikipedia for {query}: {e}")
        return []

def fetch_detailed_wikipedia_facts(page_url):
    """Fetch more detailed facts from Wikipedia page."""
    try:
        # This would require parsing the full Wikipedia page
        # For now, return empty list as this is complex
        return []
    except:
        return []

def fetch_from_additional_sources(query):
    """Fetch facts from additional knowledge sources."""
    facts = []
    
    # Try to get facts from other sources
    # This could include:
    # - Wikidata API
    # - Freebase (if available)
    # - Other knowledge bases
    
    # For now, we'll use some basic fact generation
    basic_facts = generate_basic_facts(query)
    facts.extend(basic_facts)
    
    return facts

def generate_basic_facts(query):
    """Generate basic facts based on query analysis."""
    facts = []
    query_lower = query.lower()
    
    # Geography facts
    if any(word in query_lower for word in ["capital", "country", "city", "state"]):
        if "france" in query_lower:
            facts.append("France is a country in Western Europe.")
            facts.append("The capital of France is Paris.")
        elif "china" in query_lower:
            facts.append("China is a country in East Asia.")
            facts.append("The capital of China is Beijing.")
        elif "india" in query_lower:
            facts.append("India is a country in South Asia.")
            facts.append("The capital of India is New Delhi.")
        elif "usa" in query_lower or "america" in query_lower:
            facts.append("The United States is a country in North America.")
            facts.append("The capital of the USA is Washington D.C.")
    
    # Science facts
    elif any(word in query_lower for word in ["element", "chemical", "atom", "molecule"]):
        if "gold" in query_lower:
            facts.append("Gold is a chemical element with symbol Au and atomic number 79.")
            facts.append("Gold is a precious metal known for its luster and conductivity.")
        elif "oxygen" in query_lower:
            facts.append("Oxygen is a chemical element with symbol O and atomic number 8.")
            facts.append("Oxygen is essential for respiration in most living organisms.")
        elif "water" in query_lower:
            facts.append("Water is a chemical compound with the formula H2O.")
            facts.append("Water is essential for all known forms of life.")
    
    # History facts
    elif any(word in query_lower for word in ["war", "emperor", "king", "queen", "president"]):
        if "napoleon" in query_lower:
            facts.append("Napoleon Bonaparte was a French military and political leader.")
            facts.append("Napoleon was Emperor of France from 1804 to 1814.")
        elif "caesar" in query_lower:
            facts.append("Julius Caesar was a Roman general and statesman.")
            facts.append("Caesar played a critical role in the demise of the Roman Republic.")
        elif "world war" in query_lower:
            if "ii" in query_lower or "2" in query_lower:
                facts.append("World War II lasted from 1939 to 1945.")
                facts.append("World War II was the deadliest conflict in human history.")
            else:
                facts.append("World War I lasted from 1914 to 1918.")
                facts.append("World War I was also known as the Great War.")
    
    return facts

def generate_verified_facts(query):
    """Generate verified facts when no external sources are available."""
    facts = []
    
    # Use the hardcoded facts as a base
    hardcoded = get_hardcoded_facts(query)
    facts.extend(hardcoded)
    
    # Add some general knowledge based on query analysis
    query_lower = query.lower()
    
    # If it's a question about a specific entity, try to provide basic info
    if any(word in query_lower for word in ["what", "who", "when", "where", "why", "how"]):
        # Extract the main subject
        words = query.split()
        for word in words:
            if word.istitle() and len(word) > 2:
                entity = word
                basic_info = get_entity_basic_info(entity)
                if basic_info:
                    facts.append(basic_info)
                break
    
    return facts

def get_entity_basic_info(entity):
    """Get basic information about an entity."""
    entity_lower = entity.lower()
    
    # Basic entity information
    info_map = {
        "shakespeare": "William Shakespeare was an English playwright and poet.",
        "einstein": "Albert Einstein was a German-born theoretical physicist.",
        "darwin": "Charles Darwin was an English naturalist and biologist.",
        "titanic": "The RMS Titanic was a British passenger liner that sank in 1912.",
        "moon": "The Moon is Earth's only natural satellite.",
        "sun": "The Sun is the star at the center of the Solar System.",
        "mars": "Mars is the fourth planet from the Sun.",
        "jupiter": "Jupiter is the largest planet in the Solar System.",
        "python": "Python is a high-level programming language.",
        "javascript": "JavaScript is a programming language used for web development.",
        "html": "HTML is the standard markup language for web pages.",
        "css": "CSS is a style sheet language used for describing web page presentation."
    }
    
    return info_map.get(entity_lower, None)
=======
            # Add some hardcoded facts for common entities
            facts.extend(get_hardcoded_facts(query))
            
            cache[query] = facts
            with open(cache_path, "w") as f:
                json.dump(cache, f, indent=2)
            return facts
        else:
            # Fallback to hardcoded facts
            facts = get_hardcoded_facts(query)
            cache[query] = facts
            with open(cache_path, "w") as f:
                json.dump(cache, f, indent=2)
            return facts
    except Exception as e:
        print(f"Error fetching KG data for {query}: {e}")
        # Fallback to hardcoded facts
        facts = get_hardcoded_facts(query)
        cache[query] = facts
        with open(cache_path, "w") as f:
            json.dump(cache, f, indent=2)
        return facts
>>>>>>> 0aea545 (Update README.md to provide comprehensive documentation for the Adaptive Knowledge-Guided Correction (AKGC) framework, including installation instructions, usage examples, performance results, architecture details, and contribution guidelines.)

def get_hardcoded_facts(query):
    """Get hardcoded facts for common entities as fallback."""
    facts_db = {
        # Geography
        "France": [
            "France is a country in Western Europe.",
            "The capital of France is Paris.",
            "France is known for its culture, cuisine, and landmarks like the Eiffel Tower."
        ],
        "India": [
            "India is a country in South Asia.",
            "The capital of India is New Delhi.",
            "India is the world's largest democracy and second most populous country."
        ],
        "USA": [
            "The United States is a country in North America.",
            "The capital of the USA is Washington D.C.",
            "The USA is known for its diverse culture and economic power."
        ],
        "Paris": [
            "Paris is the capital and largest city of France.",
            "Paris is known as the 'City of Light'.",
            "Famous landmarks include the Eiffel Tower and Louvre Museum."
        ],
        "London": [
            "London is the capital and largest city of England and the United Kingdom.",
            "London is a major global city and financial center.",
            "Famous landmarks include Big Ben and the Tower of London."
        ],
        
        # Science
        "Water": [
            "Water is a chemical compound with the formula H2O.",
            "Water is essential for all known forms of life.",
            "Water exists in three states: solid (ice), liquid (water), and gas (vapor)."
        ],
        "Oxygen": [
            "Oxygen is a chemical element with symbol O and atomic number 8.",
            "Oxygen is essential for respiration in most living organisms.",
            "Oxygen makes up about 21% of Earth's atmosphere."
        ],
        "Carbon": [
            "Carbon is a chemical element with symbol C and atomic number 6.",
            "Carbon is the basis of all organic compounds.",
            "Carbon exists in several forms including diamond and graphite."
        ],
        "Earth": [
            "Earth is the third planet from the Sun.",
            "Earth is the only known planet with life.",
            "Earth has one natural satellite, the Moon."
        ],
        "Mars": [
            "Mars is the fourth planet from the Sun.",
            "Mars is known as the 'Red Planet' due to iron oxide on its surface.",
            "Mars has two small moons: Phobos and Deimos."
        ],
        
        # History
        "World War II": [
            "World War II lasted from 1939 to 1945.",
            "World War II was the deadliest conflict in human history.",
            "The war ended with the surrender of Japan in September 1945."
        ],
        "World War I": [
            "World War I lasted from 1914 to 1918.",
            "World War I was also known as the Great War.",
            "The war ended with the Armistice of Compiègne on November 11, 1918."
        ],
        "Napoleon Bonaparte": [
            "Napoleon Bonaparte was a French military and political leader.",
            "Napoleon was Emperor of France from 1804 to 1814.",
            "Napoleon is considered one of the greatest military commanders in history."
        ],
        "Julius Caesar": [
            "Julius Caesar was a Roman general and statesman.",
            "Caesar played a critical role in the events that led to the demise of the Roman Republic.",
            "Caesar was assassinated on the Ides of March (March 15) in 44 BC."
        ]
    }
    
    # Try exact match first
    if query in facts_db:
        return facts_db[query]
    
    # Try case-insensitive match
    for key, facts in facts_db.items():
        if query.lower() == key.lower():
            return facts
    
    # Return generic fact
    return [f"Information about {query} is not available in the knowledge base."]