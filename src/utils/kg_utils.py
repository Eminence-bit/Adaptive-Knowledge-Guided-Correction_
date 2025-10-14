import requests
import json
import os

def fetch_kg_data(query, cache_path="models/cache/kg_cache.json"):
    """
    Retrieve facts for a query from Wikipedia and persist the results in a local cache.
    
    Attempts to fetch a short summary and description for the query from the Wikipedia REST API. If the remote fetch fails or returns a non-200 status, the function uses predefined hardcoded facts as a fallback. In all cases the resulting list of fact strings is saved to the JSON cache at `cache_path` and returned.
    
    Parameters:
        query (str): The entity or topic to look up.
        cache_path (str): Path to a JSON file used to read/write cached query results. Defaults to "models/cache/kg_cache.json".
    
    Returns:
        list: A list of fact strings for the query; may include a truncated Wikipedia extract, a "Description: ..." line, and/or hardcoded fallback facts.
    """
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
    
    # Fetch from Wikipedia API
    try:
        # Use Wikipedia's search API to find relevant pages
        search_url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_")
        response = requests.get(search_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            facts = []
            
            # Extract key facts from Wikipedia summary
            if "extract" in data:
                facts.append(data["extract"][:250] + "...")  # First 250 chars
            
            if "description" in data:
                facts.append(f"Description: {data['description']}")
            
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

def get_hardcoded_facts(query):
    """
    Return predefined factual statements for common entities as a fallback when external data is unavailable.
    
    Looks up `query` in an internal repository of common-entity facts using an exact match first, then a case-insensitive match. If no entry is found, returns a single-item list containing an informative message.
    
    Parameters:
        query (str): The entity name to look up.
    
    Returns:
        list[str]: A list of fact strings for the matched entity, or a single-item list with an informational message if no facts are available.
    """
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