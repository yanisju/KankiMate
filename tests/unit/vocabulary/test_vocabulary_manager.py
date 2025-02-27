import pytest

from src.vocabulary.manager import VocabularyManager
from src.vocabulary.sentence import Sentence
from src.vocabulary.sentence.kanji_data import KanjiDataList
from src.anki import AnkiManager

from src.constants.exceptions import VocabularyAlreadyExists, VocabularyIsNotValid

@pytest.fixture
def vocabulary_manager():
    return VocabularyManager(AnkiManager())

@pytest.fixture
def valid_words() -> list:
    return ["滋賀県", "綺麗", "飲む", "滅多に"]

@pytest.fixture(params=["12345", "!ののの="])
def invalid_word(request) -> str:
    return request.param

@pytest.fixture
def sentence() -> Sentence:
    kanji_data_list = KanjiDataList()
    return Sentence("test", "これはテストのぶんだ。", "This is a example sentence", kanji_data_list, "テスト")

class TestVocabularyManager:
    def test_initialization(self, vocabulary_manager: VocabularyManager):
        assert vocabulary_manager.vocabularies == {}
        assert vocabulary_manager.vocabulary_model.rowCount() == 0
        assert len(vocabulary_manager.sentence_added_to_deck) == 0

    def test_add_word_valid(self, vocabulary_manager: VocabularyManager, valid_words: list):
        for word in valid_words:
            vocabulary_manager.add_word(word)
        assert list(vocabulary_manager.vocabularies.keys()) == valid_words

    def test_add_word_invalid(self, vocabulary_manager: VocabularyManager, invalid_word: str):
        with pytest.raises(VocabularyIsNotValid):
            vocabulary_manager.add_word(invalid_word)

    def test_add_word_already_exists(self, vocabulary_manager: VocabularyManager, valid_words: str):
        word = valid_words[0]
        with pytest.raises(VocabularyAlreadyExists):
            vocabulary_manager.add_word(word)
            vocabulary_manager.add_word(word)

    def test_add_sentence_to_deck(self, vocabulary_manager: VocabularyManager, sentence: Sentence):
        vocabulary_manager.add_sentence_to_deck(sentence)
        assert len(vocabulary_manager.sentence_added_to_deck) == 1
        assert vocabulary_manager.sentence_added_to_deck[0].sentence == sentence.sentence

    def test_delete_vocabulary(self, vocabulary_manager: VocabularyManager, valid_words: list):
        for word in valid_words:
            vocabulary_manager.add_word(word)
        for i in range(len(valid_words)):
            vocabulary_manager.delete_vocabulary(0)
        vocabularies = list(vocabulary_manager.vocabularies.keys())
        for word in valid_words:
            assert word not in vocabularies
        
    def test_delete_all_vocabularies(self, vocabulary_manager: VocabularyManager, valid_words: list):
        for word in valid_words:
            vocabulary_manager.add_word(word)
        vocabulary_manager.delete_all_vocabularies()
        assert not vocabulary_manager.vocabularies # Check if dict is empty
        assert vocabulary_manager.vocabulary_model.rowCount() == 0