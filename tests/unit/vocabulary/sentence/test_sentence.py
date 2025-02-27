import pytest
from src.vocabulary.sentence import Sentence
from src.vocabulary.sentence.kanji_data import KanjiDataList

@pytest.fixture
def kanji_data_list() -> KanjiDataList:
    kanji_data = KanjiDataList()
    kanji_data.add("テスト", "てすと", "test")
    kanji_data.add("文章", "ぶんしょう", "sentence",)
    return kanji_data

@pytest.fixture
def sentence_instance(kanji_data_list: KanjiDataList) -> Sentence:
    return Sentence(
        vocabulary="TestVocabulary",
        sentence="これはテストの文章です。",
        translation="This is a test sentence.",
        kanji_data_list=kanji_data_list,
        word="テスト",
        word2="文章",
    )

class TestSentence:
    def test_initialization(self, sentence_instance):
        assert sentence_instance.vocabulary == "TestVocabulary"
        assert sentence_instance.sentence == "これはテストの文章です。"
        assert sentence_instance.translation == "This is a test sentence."
        assert sentence_instance.word == "テスト"
        
        assert sentence_instance.word1_data.word == "テスト"
        assert sentence_instance.word1_data.reading == "てすと"

        assert sentence_instance.word2_data.word == "文章"
        assert sentence_instance.word2_data.meaning == "sentence"


    def test_compute_standard_item(self, sentence_instance: Sentence):
        standard_items = sentence_instance.standard_item
        assert isinstance(standard_items, list)
        assert len(standard_items) == 4
        assert standard_items[0].text() == "これはテストの文章です。"
        assert standard_items[1].text() == "This is a test sentence."
        assert standard_items[2].text() == "テスト"
        assert standard_items[3].text() == "文章"

    def test_update_attributes(self, sentence_instance, kanji_data_list):
        new_attributes = (
            "新しい文章です。",
            "This is a new sentence.",
            kanji_data_list.get_kanji("文章"),
            None,
        )
        sentence_instance.update_attributes(new_attributes)

        assert sentence_instance.sentence == "新しい文章です。"
        assert sentence_instance.translation == "This is a new sentence."
        assert sentence_instance.word1_data.word == "文章"
        assert sentence_instance.word2_data is None

    def test_clone(self, sentence_instance):
        cloned_sentence = sentence_instance.clone()

        assert cloned_sentence is not sentence_instance
        assert cloned_sentence.vocabulary == sentence_instance.vocabulary
        assert cloned_sentence.sentence == sentence_instance.sentence
        assert cloned_sentence.translation == sentence_instance.translation
        assert cloned_sentence.word == sentence_instance.word
        assert cloned_sentence.word2_data.word == sentence_instance.word2_data.word

    def test_position_kanji_initialization(self, kanji_data_list):
        sentence_instance = Sentence(
            vocabulary="TestVocabulary",
            sentence="これはテストの文章です。",
            translation="This is a test sentence.",
            kanji_data_list=kanji_data_list,
            word="テスト",
        )

        assert sentence_instance.position_kanji == {
            3: "テスト",
            4: "テスト",
            5: "テスト",
            7: "文章",
            8: "文章",
        }
