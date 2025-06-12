# wikidata_api.py

import requests

def search_entity(name: str) -> str:
    """
    Search Wikidata for the entity name and return the top Q-ID.
    """
    url = "https://www.wikidata.org/w/api.php"
    params = {
        'action': 'wbsearchentities',
        'format': 'json',
        'language': 'en',
        'search': name
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['search']:
            return data['search'][0]['id']  # Return top result
    return ""


def run_sparql(query: str, endpoint: str = 'https://query.wikidata.org/sparql') -> dict:
    """
    Run a SPARQL query and return the first result as a dict.
    """
    headers = {'Accept': 'application/sparql-results+json'}
    response = requests.get(endpoint, params={'query': query}, headers=headers)

    if response.status_code == 200:
        data = response.json()
        results = data.get('results', {}).get('bindings', [])
        if results:
            result = {}
            for key, value in results[0].items():
                result[key] = value['value']
            return result
    return {}
