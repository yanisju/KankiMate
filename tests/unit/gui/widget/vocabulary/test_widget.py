import pytest
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from src.gui.widget.vocabulary import VocabularyWidget
from src.gui.widget.sentence_rendering import SentenceRenderingWidget

from src.gui.widget.sentence.table_view import SentenceTableView
from src.constants import CardTextViewMode, SentenceWidgetMode
from src.gui.widget.card_text_view import CardTextView
from src.gui.dialog.card import CardDialog
from src.anki import AnkiManager
from src.vocabulary.manager import VocabularyManager
from src.constants import SentenceWidgetMode

from src.gui.widget.vocabulary.header import VocabularyHeader
from src.gui.widget.vocabulary.table_view import VocabularyTableView

@pytest.fixture
def vocabulary_manager():
    anki_manager = AnkiManager()
    return VocabularyManager(anki_manager)

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
def qtbot_session(qtbot, parent_widget, vocabulary_manager, sentence_rendering_widget, sentence_table_view):
    sentence_widget = VocabularyWidget(parent_widget, vocabulary_manager, sentence_rendering_widget, sentence_table_view)
    qtbot.addWidget(sentence_widget)
    return qtbot, sentence_widget

class TestVocabularyWidget():
    def test_init_vocabulary_widget(self, qtbot_session):
        qtbot, vocabulary_widget = qtbot_session

        layout = vocabulary_widget.layout()
        assert isinstance(layout, QVBoxLayout)
        assert layout.count() == 2  # Header + VocabularyTableView

        # Check child widgets
        header = layout.itemAt(0).widget()
        vocabulary_list_view = layout.itemAt(1).widget()
        
        assert isinstance(header, VocabularyHeader)
        assert isinstance(vocabulary_list_view, VocabularyTableView)