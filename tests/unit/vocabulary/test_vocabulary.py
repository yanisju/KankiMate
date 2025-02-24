import pytest

from src.vocabulary import Vocabulary
from src.vocabulary.retriever import DataRetriever

from src.constants import RetrieverMode

@pytest.fixture
def data_retriever():
    return DataRetriever("jpn", "eng", RetrieverMode.LOCAL)

@pytest.fixture(params=["食べる", "不可能", "脳", "散らかす", "貧しい"])
def vocabulary(request, data_retriever):
    word = request.param
    return Vocabulary(word, data_retriever)

class TestVocabularies:
    def test_initialization(self, vocabulary: Vocabulary):
        pass