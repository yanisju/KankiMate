import pytest
from unittest.mock import patch
from typing import List
from src.vocabulary.retriever import DataRetriever
from src.vocabulary.meaning import VocabularyMeaning
from src.vocabulary.sentence.kanji_data import KanjiDataList
from src.constants import RetrieverMode


@pytest.fixture
def mock_get_sentences():
    with patch("src.vocabulary.data_retriever.sentence.http.SentenceHTTPRetriever.get_sentences") as mock:
        mock.return_value = [
            ["彼は日本語がとても上手です。", "He is very good at japanese.", "[彼|かれ]は[日本語|にほん|ご]がとても[上手|じょうず]です。"],
            ["日本語を勉強しています", "I am studying Japanese", "[日本語|にほんご]を[勉強|べんきょう]しています"],
        ]
        yield mock


@pytest.fixture
def kanji_data_list1() -> KanjiDataList:
    kanji_data_list = KanjiDataList()
    kanji_data_list.add("彼", "かれ", "")
    kanji_data_list.add("日本語", "にほんご", "Japanese (language)")
    kanji_data_list.add("上手", "じょうず", "")
    return kanji_data_list


@pytest.fixture
def kanji_data_list2() -> KanjiDataList:
    kanji_data_list = KanjiDataList()
    kanji_data_list.add("日本語", "にほんご", "Japanese (language)")
    kanji_data_list.add("勉強", "べんきょう", "")
    return kanji_data_list


@pytest.fixture
def mock_get_sentences_local():
    with patch("src.vocabulary.data_retriever.sentence.local.SentenceLocalRetriever.get_sentences") as mock:
        mock.return_value = [
            ["彼は日本語がとても上手です。", "He is very good at japanese.", "[彼|かれ]は[日本語|にほん|ご]がとても[上手|じょうず]です。"],
            ["日本語を勉強しています", "I am studying Japanese", "[日本語|にほんご]を[勉強|べんきょう]しています"],
        ]
        yield mock


@pytest.fixture
def vocabulary_meaning() -> VocabularyMeaning:
    return VocabularyMeaning("日本語")


@pytest.fixture
def data_retriever_http(mock_get_sentences: List[List[str]]) -> DataRetriever:
    return DataRetriever("jpn", "eng", RetrieverMode.HTTP)


@pytest.fixture
def data_retriever_local(mock_get_sentences_local: List[List[str]]) -> DataRetriever:
    return DataRetriever("jpn", "eng", RetrieverMode.LOCAL)


def compare_kanji_data_lists(list1: KanjiDataList, list2: KanjiDataList) -> bool:
    # Compare lengths
    if len(list1) != len(list2):
        return False

    # Compare each KanjiData object
    for kanji1, kanji2 in zip(list1, list2):
        if (
            kanji1.word != kanji2.word or
            kanji1.reading != kanji2.reading or
            kanji1.meaning != kanji2.meaning
        ):
            return False

    return True


def test_get_data_http(
    data_retriever_http: DataRetriever, 
    vocabulary_meaning: VocabularyMeaning, 
    kanji_data_list1: KanjiDataList, 
    kanji_data_list2: KanjiDataList
) -> None:
    data = data_retriever_http.get_data("日本語", vocabulary_meaning)
    assert len(data) == 2
    assert compare_kanji_data_lists(data[0].pop(3), kanji_data_list1)
    assert data[0] == ['彼は日本語がとても上手です。', 'He is very good at japanese.', '[彼|かれ]は[日本語|にほん|ご]がとても[上手|じょうず]です。']
    assert compare_kanji_data_lists(data[1].pop(3), kanji_data_list2)
    assert data[1] == ['日本語を勉強しています', 'I am studying Japanese', "[日本語|にほんご]を[勉強|べんきょう]しています"]


def test_get_data_local(
    data_retriever_local: DataRetriever, 
    vocabulary_meaning: VocabularyMeaning, 
    kanji_data_list1: KanjiDataList, 
    kanji_data_list2: KanjiDataList
) -> None:
    data = data_retriever_local.get_data("日本語", vocabulary_meaning)
    assert len(data) == 2
    assert compare_kanji_data_lists(data[0].pop(3), kanji_data_list1)
    assert data[0] == ['彼は日本語がとても上手です。', 'He is very good at japanese.', '[彼|かれ]は[日本語|にほん|ご]がとても[上手|じょうず]です。']
    assert compare_kanji_data_lists(data[1].pop(3), kanji_data_list2)
    assert data[1] == ['日本語を勉強しています', 'I am studying Japanese', "[日本語|にほんご]を[勉強|べんきょう]しています"]
