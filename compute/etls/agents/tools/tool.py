from typing import Callable
import json



class Tool:
    def __init__(self, name: str, description: str, action: Callable):
        self.name = name
        self.description = description
        self.action = action

    def execute(self, *args, **kwargs):
        """Execute the action of the tool. Receives any arguments and keyword arguments needed for the action.
        """
        return self.action(*args, **kwargs)
    
    def __str__(self):
        return f'{self.name}: {self.description}'
    

class SmartKeyWordConceptRegistry(Tool):
    """Stores keywords related to concepts in a dictionary.

    """

    def __init__(self):
        super().__init__(
            name="Smart Keyword Concept Registry",
            description="Stores keywords related to concepts in a dictionary. Pass the concept and a list of keywords to store them.",
            action=self._store_more_keywords
        )

        self._keywords_file = 'keywords.json'

    def _store_more_keywords(self, input: dict, *args, **kwargs):
        """Store more keywords for a concept in the registry, ensuring only new keywords are added.

        Args:
            concept (str): The concept to store keywords for.
            keywords (list[str]): The list of keywords to store.
        """
        concept = input.get('concept')
        keywords = input.get('keywords')

        with open(self._keywords_file, 'r') as file:
            keywords_dict = json.load(file)

        if concept in keywords_dict:
            existing_keywords = set(keywords_dict[concept])
            new_keywords = [keyword for keyword in keywords if keyword not in existing_keywords]
            keywords_dict[concept].extend(new_keywords)
        else:
            keywords_dict[concept] = keywords

        with open(self._keywords_file, 'w') as file:
            json.dump(keywords_dict, file)


class SmartKeyWordConceptFetcher(Tool):
    def __init__(self):
        super().__init__(
            name="Smart Keyword Concept Fetcher",
            description="Fetches keywords related to concepts from the registry.",
            action=self._fetch_keywords
        )

        self._keywords_file = 'keywords.json'

    def _fetch_keywords(self, concept: str, *args, **kwargs):
        """Fetch keywords for a concept from the registry.

        Args:
            concept (str): The concept to fetch keywords for.

        Returns:
            list[str]: The list of keywords for the concept.
        """
        try:
            with open(self._keywords_file, 'r') as file:
                keywords_dict = json.load(file)
        except FileNotFoundError:
            # create the file if it doesn't exist
            with open(self._keywords_file, 'w') as file:
                json.dump({}, file)
            return []

        return keywords_dict.get(concept, [])
