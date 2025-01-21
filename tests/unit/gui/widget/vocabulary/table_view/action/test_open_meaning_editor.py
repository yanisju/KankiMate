import pytest
from PyQt6.QtWidgets import QWidget
from src.gui.widget.vocabulary.table_view.action.open_meaning_editor import OpenMeaningEditorAction
from src.gui.widget.vocabulary.table_view import VocabularyTableView
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
def parent_parent_widget():
    return QWidget()

@pytest.fixture
def parent_widget(parent_parent_widget):
    return QWidget(parent_parent_widget)


@pytest.fixture
def sentence_rendering_widget(parent_widget):
    return SentenceRenderingWidget(parent_widget, None)

@pytest.fixture
def sentence_table_view(parent_widget, vocabulary_manager, sentence_rendering_widget):
    return SentenceTableView(parent_widget, vocabulary_manager, None, None, SentenceWidgetMode.VOCABULARY_SENTENCE)


@pytest.fixture
def vocabulary_table_view(parent_widget, vocabulary_manager, sentence_rendering_widget, sentence_table_view):
    return VocabularyTableView(parent_widget, vocabulary_manager, sentence_rendering_widget, sentence_table_view)


@pytest.fixture
def vocabulary_table_view_menu(parent_widget, vocabulary_manager, sentence_rendering_widget, sentence_table_view):
    return VocabularyTableViewMenu(parent_widget, vocabulary_manager, sentence_rendering_widget, sentence_table_view)

@pytest.fixture
def action(vocabulary_table_view_menu, vocabulary_table_view):
    return OpenMeaningEditorAction(
        vocabulary_table_view_menu,
        vocabulary_table_view
    )


def test_lookup_on_jisho_action(qtbot, action: OpenMeaningEditorAction, vocabulary_manager, sentence_rendering_widget, sentence_table_view):
    assert action.text() == "Open Meaning Editor"
    assert callable(action.table_view._double_clicked)
