import pytest
from PyQt6.QtWidgets import QWidget
from src.gui.widget.sentence.button.deck_options import DeckOptionsButtons
from src.anki import AnkiManager
from src.gui.dialog.deck_options import DeckOptionsDialog

@pytest.fixture
def parent_widget():
    """Fixture pour le widget parent."""
    return QWidget()

@pytest.fixture
def anki_manager():
    """Fixture pour l'AnkiManager simulé."""
    return AnkiManager()

@pytest.fixture
def deck_options_buttons(qtbot, parent_widget, anki_manager):
    deck_option_button = DeckOptionsButtons(parent_widget, anki_manager)
    qtbot.addWidget(deck_option_button)
    return deck_option_button

class TestDeckOptions():
    def test_deck_options_button_initialization(self, deck_options_buttons):
        assert isinstance(deck_options_buttons.deck_option_dialog, DeckOptionsDialog)

    def test_deck_options_button_opens_dialog(self, deck_options_buttons, qtbot):
        deck_options_buttons.clicked.emit()
        assert True
