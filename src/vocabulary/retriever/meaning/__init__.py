from abc import ABC, abstractmethod

from ...meaning import VocabularyMeaning

class MeaningRetriever(ABC):
    """Abstract class for retrieving word information such as:
    - Meanings (definitions),
    - Part of speech,
    - Common word indicator,
    - JLPT level.
    """

    @abstractmethod
    def retrieve(self, word: str) -> VocabularyMeaning:
        """Retrieve word information including meanings, part of speech, 
        common word status, and JLPT level.

        Args:
            word (str): The word to search for.

        Returns:
            dict: A dictionary containing the retrieved information.
        """
        pass
    
    @abstractmethod
    def _fetch_from_api(self, word: str) -> list:
        """Fetch raw data from an API or external source.

        Args:
            word (str): The word to query.

        Returns:
            list: A list containing raw data from the source.
        """
        pass

    @abstractmethod
    def _format_data(self, data: list) -> dict:
        """Format raw data into a structured dictionary.

        Args:
            data (list): The raw data retrieved from the API.

        Returns:
            dict: A formatted dictionary containing the extracted meanings,
                  part of speech, common word indicator, and JLPT level.
        """
        pass
