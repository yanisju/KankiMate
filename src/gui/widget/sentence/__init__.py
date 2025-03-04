from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QGroupBox

from .header import SentenceHeader
from ....vocabulary.manager import VocabularyManager
from .table_view import SentenceTableView
from ..card_text_view import CardTextView
from ...dialog.card import CardDialog

from ....constants import SentenceWidgetMode


class SentenceWidget(QGroupBox):
    def __init__(self,
            parent: QWidget,
            vocabulary_manager: VocabularyManager,
            card_text_view: CardTextView,
            card_dialog: CardDialog,
            mode: SentenceWidgetMode) -> None:
        super().__init__(parent)

        self.vocabulary_manager = vocabulary_manager
        self.mode = mode
        
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding)
        layout = QVBoxLayout()
        self.setLayout(layout)

        header = SentenceHeader(self, mode, vocabulary_manager)
        layout.addWidget(header)

        self.sentence_table_view = SentenceTableView(parent, vocabulary_manager, card_text_view, card_dialog, mode)
        if mode == SentenceWidgetMode.ADDED_SENTENCE:
            self.sentence_table_view.setModel(vocabulary_manager.sentence_added_to_deck.sentences_model)

        layout.addWidget(self.sentence_table_view)

    def sizeHint(self):
        if self.mode == SentenceWidgetMode.VOCABULARY_SENTENCE:
            width = int(self.parentWidget().width() * 0.6)
            height = int(self.parentWidget().height() * 0.4)
        else:
            width = int(self.parentWidget().width() * 0.4)
            height = int(self.parentWidget().height() * 0.75)
        return QSize(width, height)
