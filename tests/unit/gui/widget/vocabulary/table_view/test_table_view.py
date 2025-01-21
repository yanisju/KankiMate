import pytest

from src.anki import AnkiManager
from src.vocabulary.manager import VocabularyManager

from PyQt6.QtWidgets import QWidget, QTableView
from src.gui.widget.vocabulary.table_view import VocabularyTableView
from src.gui.dialog.card import CardDialog
from src.gui.widget.sentence_rendering import SentenceRenderingWidget
from src.constants import CardTextViewMode, SentenceWidgetMode
from src.gui.widget.card_text_view import CardTextView
from src.gui.widget.sentence.table_view import SentenceTableView
from src.gui.widget.vocabulary.table_view.menu import VocabularyTableViewMenu
from src.gui.dialog.meaning import MeaningDialog


@pytest.fixture
def vocabulary_manager():
    anki_manager = AnkiManager()
    vocabulary_manager = VocabularyManager(anki_manager)
    vocabulary_manager.add_word("天気")
    vocabulary_manager.add_word("苔")

    return vocabulary_manager

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
def qtbot_session(
    qtbot, parent_widget, vocabulary_manager, sentence_rendering_widget, sentence_table_view
):
    vocabulary_table_view = VocabularyTableView(
        parent_widget,
        vocabulary_manager,
        sentence_rendering_widget,
        sentence_table_view,
    )
    qtbot.addWidget(vocabulary_table_view)
    return qtbot, vocabulary_table_view


class TestVocabularyTableView:
    def test_init_vocabulary_table_view(self, qtbot_session):
        qtbot, table_view = qtbot_session

        assert isinstance(table_view, QTableView)

        assert table_view.model() == table_view.vocabulary_manager.vocabulary_model

        assert isinstance(table_view.menu, VocabularyTableViewMenu)
        assert isinstance(table_view.meaning_dialog, MeaningDialog)

    def test_double_clicked_opens_meaning_dialog(self, qtbot_session):
        qtbot, table_view = qtbot_session

        model_index = table_view.currentIndex()
        table_view.doubleClicked.emit(model_index)

    def test_meaning_dialog_confirm_action(self, qtbot_session):
        qtbot, table_view = qtbot_session

        table_view.meaning_dialog.confirm_button_clicked_signal.emit(table_view.model(), 2)

    # TODO: Continue tests when development is over


    # def test_selection_changed_updates_sentence_view(self, qtbot_session):
    #     """Teste la mise à jour de la vue des phrases lors d'un changement de sélection."""
    #     qtbot, table_view = qtbot_session

    #     # Simule un changement de sélection
    #     mock_row = 1
    #     mock_sentence_model = MagicMock()
    #     table_view.currentIndex = MagicMock(return_value=QModelIndex())
    #     table_view.vocabulary_manager.__getitem__.return_value.sentence_manager.sentences_model = (
    #         mock_sentence_model
    #     )

    #     table_view._selection_changed_action()

    #     # Vérifie que la vue des phrases a été mise à jour
    #     table_view.sentence_table_view.setModel.assert_called_once_with(mock_sentence_model)
