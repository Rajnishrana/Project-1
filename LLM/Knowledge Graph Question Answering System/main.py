
from ask_function import ask

if __name__ == '__main__':
    print("Testing intelligent knowledge graph QA system...\n")

    print("Tom Cruise age: ", ask("how old is Tom Cruise"))         # Expected: ~62
    print("Taylor Swift age: ", ask("how old is Taylor Swift"))     # Expected: ~35
    print("London population: ", ask("what is the population of London"))   # Expected: 8799728
    print("New York population: ", ask("what is the population of New York?"))  # Expected: 8804190
    print("Brack Obama age: ", ask("how old is Barack Obama"))

    # These should be dynamically fetched from Wikidata and return current facts
