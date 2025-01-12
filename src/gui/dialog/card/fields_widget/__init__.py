from os import path

from PyQt6.QtWidgets import QVBoxLayout, QGroupBox, QSizePolicy
from PyQt6.QtCore import QSize
from .sentence_attributes import SentenceAttributesWidget
from .kanji_table_view import KanjiTableView


class FieldsWidget(QGroupBox):
    def __init__(self, parent, card_view):
        super().__init__(parent)
        self.card_view = card_view

        addon_base_dir = path.realpath(__file__)
        for i in range(6):
            addon_base_dir = path.dirname(addon_base_dir)

        css_file_path = path.join(addon_base_dir, "styles", "fields_group_box.css")

        with open(css_file_path, "r") as css_file:
            self.setStyleSheet(css_file.read())

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding)

        # All QLineEdit for each fields of the vocabulary.
        self.field_widget_list = []

        self._init_layout()

    def _init_layout(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.sentence_attributes_widget = SentenceAttributesWidget(
            self, self.card_view)
        layout.addWidget(self.sentence_attributes_widget)

        # View containg kanjis and theirs readings + meanings
        self.kanji_table_view = KanjiTableView(self)
        layout.addWidget(self.kanji_table_view)

    def set_to_new_sentence(self, sentence):
        """Fill each fields for the card with the current items."""
        self.kanji_table_view.set_to_new_sentence(sentence)
        self.sentence_attributes_widget.set_to_new_sentence(sentence)

    def sizeHint(self):
        width = int(self.parentWidget().width() * 0.6)
        height = int(self.parentWidget().height())
        return QSize(width, height)
