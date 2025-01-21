import pytest
from PyQt6.QtWidgets import QWidget
from src.vocabulary.manager import VocabularyManager
from src.gui.widget.sentence.table_view import SentenceTableView
from src.constants import SentenceWidgetMode, CardTextViewMode
from src.gui.widget.sentence.table_view import SentenceTableViewMenu
from src.gui.widget.card_text_view import CardTextView
from src.gui.widget.sentence.table_view.action.delete_all_sentences import DeleteAllSentenceAction

@pytest.fixture
def vocabulary_manager():
    vocabulary_manager = VocabularyManager(None)  
    vocabulary_manager.add_word("天気")
    vocabulary_manager.add_word("住所")
    return vocabulary_manager

@pytest.fixture
def parent_widget():
    return QWidget()

@pytest.fixture
def sentence_table_view(parent_widget, vocabulary_manager):
    sentence_table_view = SentenceTableView(parent_widget, vocabulary_manager, None, None, SentenceWidgetMode.VOCABULARY_SENTENCE)
    vocabulary_sentences_model = vocabulary_manager[0].sentence_manager.sentences_model
    sentence_table_view.setModel(vocabulary_sentences_model)
    return sentence_table_view

@pytest.fixture
def card_text_view():
    return CardTextView(CardTextViewMode.IS_MAIN_WINDOW, None)

@pytest.fixture
def sentence_table_view_menu(sentence_table_view, vocabulary_manager, card_text_view):
    return SentenceTableViewMenu(sentence_table_view, vocabulary_manager, card_text_view, SentenceWidgetMode.VOCABULARY_SENTENCE)

@pytest.fixture
def action(sentence_table_view_menu, vocabulary_manager):
    return DeleteAllSentenceAction(
        sentence_table_view_menu,
        vocabulary_manager,
    )

def test_delete_all_sentences_action(qtbot, action: DeleteAllSentenceAction, vocabulary_manager, sentence_table_view):
    assert action.text() == "Delete all Sentences"
    assert callable(action.parent().parent().model().sentence_manager.clear)
