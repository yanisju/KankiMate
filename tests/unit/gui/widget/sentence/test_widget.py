import pytest
from PyQt6.QtWidgets import QWidget

from src.gui.central_widget import CentralWidget
from src.gui.widget.sentence.widget import SentenceWidget
from src.gui.widget.sentence.table_view import SentenceTableView
from src.gui.widget.sentence.header import SentenceHeader
from src.constants import CardTextViewMode, SentenceWidgetMode
from src.gui.widget.card_text_view import CardTextView
from src.gui.dialog.card import CardDialog
from src.anki import AnkiManager
from src.vocabulary.manager import VocabularyManager
from src.constants import SentenceWidgetMode

@pytest.fixture
def vocabulary_manager():
    anki_manager = AnkiManager()
    return VocabularyManager(anki_manager)

@pytest.fixture
def parent_widget():
    return QWidget()

@pytest.fixture
def qtbot_session(qtbot, parent_widget, vocabulary_manager):
    card_text_view = CardTextView(CardTextViewMode.IS_MAIN_WINDOW)
    central_widget = CentralWidget(parent_widget, vocabulary_manager)
    card_dialog = CardDialog(central_widget, vocabulary_manager)
    sentence_widget = SentenceWidget(parent_widget, vocabulary_manager, card_text_view, card_dialog, SentenceWidgetMode.VOCABULARY_SENTENCE)
    card_text_view.setParent(parent_widget)
    qtbot.addWidget(sentence_widget)
    return qtbot, sentence_widget

class TestSentenceWidget():
    def test_init_sentence_widget(self, qtbot_session):
        qtbot, sentence_widget = qtbot_session
        assert sentence_widget.mode == SentenceWidgetMode.VOCABULARY_SENTENCE