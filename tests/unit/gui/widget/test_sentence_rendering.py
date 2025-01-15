import pytest
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from src.gui.widget.sentence_rendering import SentenceRenderingWidget
from src.constants import CardTextViewMode
from src.gui.widget.sentence_rendering.header import SentenceRenderingHeader
from src.gui.dialog.card import CardDialog
from src.gui.widget.card_text_view import CardTextView
from src.vocabulary.manager import VocabularyManager
from src.anki import AnkiManager


@pytest.fixture
def parent_widget():
    return QWidget()

@pytest.fixture
def card_dialog(parent_widget):
    anki_manager = AnkiManager()
    vocabulary_manager = VocabularyManager(anki_manager)
    return CardDialog(parent_widget, vocabulary_manager)

@pytest.fixture
def qtbot_session(qtbot, parent_widget, card_dialog):
    """Fixture pour l'application PyQt."""
    card_text_view = SentenceRenderingWidget(parent_widget, )
    card_text_view.setParent(parent_widget)
    qtbot.addWidget(card_text_view)
    return qtbot, card_text_view


@pytest.fixture
def sentence_rendering_widget(qtbot, parent_widget, card_dialog):
    """Fixture pour créer une instance de SentenceRenderingWidget."""
    widget = SentenceRenderingWidget(parent_widget, card_dialog)
    qtbot.addWidget(widget)
    return widget


def test_initialization(sentence_rendering_widget):
    assert isinstance(sentence_rendering_widget, SentenceRenderingWidget)


    assert isinstance(sentence_rendering_widget.layout(), QVBoxLayout)
    assert sentence_rendering_widget.layout().count() == 2


    header = sentence_rendering_widget.layout().itemAt(0).widget()
    card_text_view = sentence_rendering_widget.layout().itemAt(1).widget()
    assert isinstance(header, SentenceRenderingHeader)
    assert isinstance(card_text_view, CardTextView)
    assert card_text_view.mode == CardTextViewMode.IS_MAIN_WINDOW

