from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QGroupBox

from .header import SentenceRenderingHeader
from ..card_text_view import CardTextView

from ....constants import CardTextViewMode


class SentenceRenderingWidget(QWidget):
    def __init__(self, parent: QWidget, card_dialog) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding)

        # header = SentenceRenderingHeader(self)
        # layout.addWidget(header)

        self.card_text_view = CardTextView(
            CardTextViewMode.IS_MAIN_WINDOW, card_dialog)  # View for retrieved words
        layout.addWidget(self.card_text_view)

    def sizeHint(self):
        width = int(self.parentWidget().width())
        height = int(self.parentWidget().height() * 0.3)
        return QSize(width, height)
