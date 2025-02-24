from abc import ABC, abstractmethod

class SentenceRetriever(ABC):

    @abstractmethod
    def get_sentences(self, word):
        pass