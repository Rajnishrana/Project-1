
from utils import parse_question, map_intent_to_property
from wikidata_api import search_entity, run_sparql
from reasoning import calculate_age

def ask(question: str, endpoint: str = 'https://query.wikidata.org/sparql') -> str:
    entity_name, intent = parse_question(question)
    entity_id = search_entity(entity_name)

    if not entity_id:
        return "Entity not found"

    property_id = map_intent_to_property(intent)

    if intent == "age":
        query = f"""
        SELECT ?birthDate ?deathDate WHERE {{
            wd:{entity_id} wdt:P569 ?birthDate .
            OPTIONAL {{ wd:{entity_id} wdt:P570 ?deathDate . }}
        }}
        """
        results = run_sparql(query, endpoint)
        if not results:
            return "Data not found"
        birth = results.get('birthDate')
        death = results.get('deathDate')
        return str(calculate_age(birth, death))

    elif intent == "population":
        query = f"""
        SELECT ?population WHERE {{
            wd:{entity_id} wdt:P1082 ?population .
        }} ORDER BY DESC(?population) LIMIT 1
        """
        results = run_sparql(query, endpoint)
        if not results or "population" not in results:
            return "Data not found"
        return str(results["population"])

    else:
        return "Unsupported question type"
