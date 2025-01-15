from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget

from .widget.vocabulary import VocabularyWidget
from .widget.sentence import SentenceWidget
from .widget.sentence_rendering import SentenceRenderingWidget

from .dialog.card import CardDialog

from ..constants import SentenceWidgetMode


class CentralWidget(QWidget):
    def __init__(self, parent: QWidget, vocabulary_manager) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)

        card_dialog = CardDialog(self, vocabulary_manager)
        sentence_rendering_widget = SentenceRenderingWidget(self, card_dialog)
        card_dialog.sentence_modified.connect(
            sentence_rendering_widget.card_text_view.set_card_view)
        sentence_widget = SentenceWidget(
            self,
            vocabulary_manager,
            sentence_rendering_widget.card_text_view,
            card_dialog,
            SentenceWidgetMode.VOCABULARY_SENTENCE)

        vocabulary_sentence_deck_layout = QHBoxLayout()
        layout.addLayout(vocabulary_sentence_deck_layout)

        vocabulary_and_its_sentence_layout = QVBoxLayout()
        vocabulary_sentence_deck_layout.addLayout(vocabulary_and_its_sentence_layout)

        vocabulary_widget = VocabularyWidget(
                self,
                vocabulary_manager,
                sentence_rendering_widget,
                sentence_widget.sentence_table_view)
        vocabulary_and_its_sentence_layout.addWidget(vocabulary_widget)
        vocabulary_and_its_sentence_layout.addWidget(sentence_widget)
        
        added_sentence_widget = SentenceWidget(
            self,
            vocabulary_manager,
            sentence_rendering_widget.card_text_view,
            card_dialog,
            SentenceWidgetMode.ADDED_SENTENCE)
        vocabulary_sentence_deck_layout.addWidget(added_sentence_widget)

        layout.addWidget(sentence_rendering_widget)
