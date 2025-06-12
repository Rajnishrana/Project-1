# utils.py

import re

def parse_question(question: str) -> tuple[str, str]:
    """
    Simple rule-based parser to extract intent and entity from the question.
    Returns: (entity_name, intent)
    """
    question = question.lower().strip().replace('?', '')

    if "how old is" in question:
        entity = question.replace("how old is", "").strip()
        return entity, "age"

    elif "what is the population of" in question:
        entity = question.replace("what is the population of", "").strip()
        return entity, "population"

    else:
        return question, "unknown"


def map_intent_to_property(intent: str) -> str:
    """
    Maps intent types to Wikidata property IDs.
    """
    mapping = {
        "age": "P569",          # Date of birth (we will use this and optionally P570)
        "population": "P1082"   # Population
    }
    return mapping.get(intent, "")
