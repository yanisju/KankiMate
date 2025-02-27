from os import path

from PyQt6.QtWidgets import QTextEdit, QSizePolicy
from PyQt6.QtCore import QSize

from ....vocabulary.sentence import Sentence
from .sentences import *

from ....constants import CardTextViewMode


class CardTextView(QTextEdit):
    """Text view of the card in Anki."""

    def __init__(self, mode: CardTextViewMode, card_dialog=None) -> None:
        super().__init__()
        self.mode = mode
        self.sentence = None
        self.card_dialog = card_dialog

        self.setReadOnly(True)
        self.setMouseTracking(True)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding)

        addon_base_dir = path.realpath(__file__)
        for i in range(5):
            addon_base_dir = path.dirname(addon_base_dir)

        css_file_path = path.join(addon_base_dir, "styles", "text_view.css")

        with open(css_file_path, "r") as css_file: 
            self.setStyleSheet(css_file.read())

    def set_card_view(self, sentence: Sentence):
        """Set card view, based on vocabulary fields."""

        self.sentence = sentence
        self.sentence_attributes = sentence.attributes

        card_text = get_text(self.sentence_attributes)
        self.setHtml(card_text)

    def set_card_view_from_attributes_values(self, attributes_values: list):
        """Refresh view, based on card fields values."""
        self.attributes_values = attributes_values
        card_text = get_text(attributes_values)
        self.setHtml(card_text)

    def mouseMoveEvent(self, event):
        """Show transcription when mouse howers a kanji."""
        super().mouseMoveEvent(event)
        if self.sentence is not None:
            show_transcription(self,
                               event,
                               len(self.sentence.attributes[0]),
                               self.sentence.position_kanji,
                               self.sentence.kanji_data_list)

    def mouseDoubleClickEvent(self, mouse_event):
        if self.mode == CardTextViewMode.IS_MAIN_WINDOW and self.sentence is not None:
            self.card_dialog.open()

    def clear(self):
        self.sentence = None
        self.sentence_attributes = None
        self.attributes_values = None
        super().clear()

    def sizeHint(self):
        return QSize(int(self.parent().width() * 0.5),
                     int(self.parent().height()))
