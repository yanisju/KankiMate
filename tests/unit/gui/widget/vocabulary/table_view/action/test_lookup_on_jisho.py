import pytest
from PyQt6.QtWidgets import QWidget
from src.gui.widget.vocabulary.table_view.action.lookup_on_jisho import LookupOnJishoAction
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
def action(vocabulary_table_view_menu, vocabulary_manager, sentence_rendering_widget, sentence_table_view):
    return LookupOnJishoAction(
        vocabulary_table_view_menu,
        vocabulary_manager
    )


def test_lookup_on_jisho_action(qtbot, action: LookupOnJishoAction, vocabulary_manager, sentence_rendering_widget, sentence_table_view):
    assert action.text() == "Lookup on Jisho"
