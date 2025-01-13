from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton

from .button.deck_options import DeckOptionsButtons
from .button.generate_deck import GenerateDeckButton
from ....vocabulary.manager import VocabularyManager
from ....constants import SentenceWidgetMode

class SentenceHeader(QWidget):
    def __init__(self, parent: QWidget, mode: SentenceWidgetMode, vocabulary_manager: VocabularyManager) -> None:
        super().__init__(parent)
        self.vocabulary_manager = vocabulary_manager
        layout = QHBoxLayout(self)

        if mode == SentenceWidgetMode.VOCABULARY_SENTENCE:
            label_name = "Sentence List"
        else:
            label_name = "Added Sentence List"
        label = QLabel(label_name, self)
        label.setProperty("class", "title")
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(label)

        if mode == SentenceWidgetMode.ADDED_SENTENCE:
            self.generate_deck_button = GenerateDeckButton(self, vocabulary_manager)
            layout.addWidget(self.generate_deck_button)

            self.deck_options_button = DeckOptionsButtons(
                self, vocabulary_manager.anki_manager)
            layout.addWidget(self.deck_options_button)