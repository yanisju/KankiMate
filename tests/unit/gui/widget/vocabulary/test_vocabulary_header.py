import pytest
from unittest.mock import MagicMock
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget
from src.gui.widget.vocabulary.header import VocabularyHeader
from src.anki import AnkiManager
from src.vocabulary.manager import VocabularyManager

from src.gui.dialog.card import CardDialog
from src.gui.widget.sentence_rendering import SentenceRenderingWidget
from src.gui.widget.vocabulary.table_view import VocabularyTableView
from src.gui.widget.sentence.table_view import SentenceTableView
from src.gui.widget.card_text_view import CardTextView
from src.constants import CardTextViewMode, SentenceWidgetMode


@pytest.fixture
def vocabulary_manager():
    anki_manager = AnkiManager()
    return VocabularyManager(anki_manager)


@pytest.fixture
def vocabulary_list_view():
    return MagicMock()

@pytest.fixture
def parent_parent_widget():
    return QWidget()

@pytest.fixture
def parent_widget(parent_parent_widget):
    return QWidget(parent_parent_widget)

@pytest.fixture
def card_dialog(parent_widget, vocabulary_manager):
    return CardDialog(parent_widget, vocabulary_manager)

@pytest.fixture
def sentence_rendering_widget(parent_widget, card_dialog):
    return SentenceRenderingWidget(parent_widget, card_dialog)

@pytest.fixture
def sentence_table_view(parent_widget, vocabulary_manager, card_dialog):
    card_text_view = CardTextView(CardTextViewMode.IS_MAIN_WINDOW, card_dialog)
    return SentenceTableView(parent_widget, vocabulary_manager, card_text_view, card_dialog, SentenceWidgetMode.VOCABULARY_SENTENCE)

@pytest.fixture
def vocabulary_list_view(parent_widget, vocabulary_manager, sentence_rendering_widget, sentence_table_view):
    return VocabularyTableView(parent_widget, vocabulary_manager, sentence_rendering_widget, sentence_table_view)


@pytest.fixture
def qtbot_session(qtbot, parent_widget, vocabulary_manager, vocabulary_list_view):
    vocabulary_header = VocabularyHeader(parent_widget, vocabulary_manager, vocabulary_list_view)
    qtbot.addWidget(vocabulary_header)
    return qtbot, vocabulary_header


class TestVocabularyHeader:
    def test_init_vocabulary_header(self, qtbot_session):
        qtbot, vocabulary_header = qtbot_session

        layout = vocabulary_header.layout()
        assert isinstance(layout, QHBoxLayout)
        assert layout.count() == 2  # QLabel + AddWordWidget

        label = layout.itemAt(0).widget()
        add_word_button = layout.itemAt(1).widget()
        from src.gui.widget.vocabulary.button.add_word import AddWordWidget
        assert isinstance(label, QLabel)
        assert label.text() == "Vocabulary List"
        assert label.property("class") == "title"
        assert isinstance(add_word_button, AddWordWidget)

    def test_label_properties(self, qtbot_session):
        qtbot, vocabulary_header = qtbot_session

        label = vocabulary_header.layout().itemAt(0).widget()
        assert label.text() == "Vocabulary List"
        assert label.property("class") == "title"

