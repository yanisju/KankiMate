import pytest
from PyQt6.QtWidgets import QWidget
from src.gui.widget.vocabulary.table_view.action.delete_all_vocabularies import DeleteAllVocabulariesAction
from src.gui.widget.sentence_rendering import SentenceRenderingWidget
from src.gui.widget.sentence.table_view import SentenceTableView
from src.gui.widget.vocabulary.table_view.menu import VocabularyTableViewMenu
from src.vocabulary.manager import VocabularyManager
from src.constants import SentenceWidgetMode


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
def sentence_rendering_widget(parent_widget):
    return SentenceRenderingWidget(parent_widget, None)


@pytest.fixture
def sentence_table_view(parent_widget, vocabulary_manager, sentence_rendering_widget):
    return SentenceTableView(parent_widget, vocabulary_manager, None, None, SentenceWidgetMode.VOCABULARY_SENTENCE)

@pytest.fixture
def vocabulary_table_view_menu(parent_widget, vocabulary_manager, sentence_rendering_widget, sentence_table_view):
    return VocabularyTableViewMenu(parent_widget, vocabulary_manager, sentence_rendering_widget, sentence_table_view)

@pytest.fixture
def delete_action(vocabulary_table_view_menu, vocabulary_manager, sentence_rendering_widget, sentence_table_view):
    return DeleteAllVocabulariesAction(
        vocabulary_table_view_menu,
        vocabulary_manager,
        sentence_rendering_widget,
        sentence_table_view
    )


def test_delete_all_vocabularies_action(qtbot, delete_action: DeleteAllVocabulariesAction, vocabulary_manager, sentence_rendering_widget, sentence_table_view):
    initial_count = vocabulary_manager.vocabulary_model.rowCount()
    assert initial_count == 2

    parent = delete_action.parent()
    parent.row = 0
    delete_action.trigger()

    assert vocabulary_manager.vocabulary_model.rowCount() == 0

    assert sentence_rendering_widget.card_text_view.toPlainText() == ""
