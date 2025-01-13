import pytest
from typing import Tuple
from PyQt6.QtWidgets import QWidget
from src.gui.widget.card_text_view import CardTextView
from src.constants import CardTextViewMode  
from src.vocabulary.sentence.manager import Sentence
from src.vocabulary.sentence.kanji_data import KanjiDataList, KanjiData

@pytest.fixture
def parent_widget():
    return QWidget()

@pytest.fixture
def qtbot_session(qtbot, parent_widget):
    """Fixture pour l'application PyQt."""
    card_text_view = CardTextView(CardTextViewMode.IS_MAIN_WINDOW)
    card_text_view.setParent(parent_widget)
    # card_text_view.show()
    qtbot.addWidget(card_text_view)
    return qtbot, card_text_view

@pytest.fixture
def kanji_data_list1():
    kanji_data_list = KanjiDataList()
    kanji_data_list.add("今", "いま", "now")
    kanji_data_list.add("日", "にち", "day")
    kanji_data_list.add("時", "とき", "time")
    return kanji_data_list

@pytest.fixture
def sentence1(kanji_data_list1):
    return Sentence(
        None,
        "今日はとてもいい天気ですが、少し寒いですね。",
        "Today is very nice weather, but it's a bit cold.",
        kanji_data_list1,
        None
    )

@pytest.fixture
def sentence1_attributes():
    kanjidata1 = KanjiData("天気", "てんき", "weather")
    return ["今日はとてもいい天気ですが、少し寒いですね。",
        "Today is very nice weather, but it's a bit cold.",
        kanjidata1,
        None]

class TestCardTextView:
    def test_initialization(self, qtbot_session: Tuple[QWidget, CardTextView]):
        qtbot, card_text_view = qtbot_session
        
        assert card_text_view.isReadOnly()
        assert card_text_view.hasMouseTracking()

    def test_set_card_view(self, qtbot_session: Tuple[QWidget, CardTextView], sentence1: Sentence):
        qtbot, card_text_view = qtbot_session
        card_text_view.set_card_view(sentence1)
        assert card_text_view.sentence == sentence1
        assert card_text_view.sentence_attributes == sentence1.attributes

    def test_set_card_view_from_attributes_values(self, qtbot_session: Tuple[QWidget, CardTextView], sentence1_attributes: list):
        qtbot, card_text_view = qtbot_session
        card_text_view.set_card_view_from_attributes_values(sentence1_attributes)
        assert card_text_view.attributes_values == sentence1_attributes

    def test_clear(self, qtbot_session: Tuple[QWidget, CardTextView], sentence1: Sentence, sentence1_attributes: list):
        qtbot, card_text_view = qtbot_session
        card_text_view.set_card_view(sentence1)
        card_text_view.set_card_view_from_attributes_values(sentence1_attributes)
        card_text_view.clear()
        assert card_text_view.sentence == None
        assert card_text_view.sentence_attributes == None
        assert card_text_view.attributes_values == None