import pytest
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel
from src.gui.widget.sentence.header import SentenceHeader
from src.anki import AnkiManager
from src.vocabulary.manager import VocabularyManager
from src.vocabulary.sentence.sentence import Sentence
from src.constants import SentenceWidgetMode

@pytest.fixture
def vocabulary_manager():
    anki_manager = AnkiManager()
    return VocabularyManager(anki_manager)


@pytest.fixture
def parent_widget():
    return QWidget()


@pytest.fixture
def sentence_header_vocabulary(qtbot, parent_widget, vocabulary_manager):
    sentence_header = SentenceHeader(
        parent=parent_widget,
        mode=SentenceWidgetMode.VOCABULARY_SENTENCE,
        vocabulary_manager=vocabulary_manager,
    )
    qtbot.addWidget(sentence_header)
    return sentence_header


@pytest.fixture
def sentence_header_added(qtbot, parent_widget, vocabulary_manager):
    sentence_header = SentenceHeader(
        parent=parent_widget,
        mode=SentenceWidgetMode.ADDED_SENTENCE,
        vocabulary_manager=vocabulary_manager,
    )
    qtbot.addWidget(sentence_header)
    return sentence_header

class TestSentenceHeader():
    def test_initialization_vocabulary_sentence(self, sentence_header_vocabulary):
        label = sentence_header_vocabulary.findChild(QLabel)
        assert label is not None
        assert label.text() == "Sentence List"
        assert not hasattr(sentence_header_vocabulary, "generate_deck_button")
        assert not hasattr(sentence_header_vocabulary, "deck_options_button")

    def test_initialization_added_sentence(self, sentence_header_added):
        label = sentence_header_added.findChild(QLabel)
        assert label is not None
        assert label.text() == "Queue Sentence List"

        generate_deck_button = sentence_header_added.findChild(QPushButton)
        assert generate_deck_button is not None
        assert not generate_deck_button.isEnabled()

        deck_options_button = getattr(sentence_header_added, "deck_options_button", None)
        assert deck_options_button is not None