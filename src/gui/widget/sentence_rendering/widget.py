from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QGroupBox

from .header import SentenceRenderingHeader
from ..card_text_view import CardTextView

from ....constants import CardTextViewMode


class SentenceRenderingWidget(QGroupBox):
    def __init__(self, parent: QWidget, card_dialog) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        with open("styles/group_box.css", "r") as css_file:
            self.setStyleSheet(css_file.read())

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding)

        header = SentenceRenderingHeader(self)
        layout.addWidget(header)

        self.card_text_view = CardTextView(
            CardTextViewMode.IS_MAIN_WINDOW, card_dialog)  # View for retrieved words
        layout.addWidget(self.card_text_view)

    def sizeHint(self):
        width = int(self.parentWidget().width())
        height = int(self.parentWidget().height() * 0.35)
        return QSize(width, height)