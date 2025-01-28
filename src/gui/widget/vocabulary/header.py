from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import QSize

from .button.add_word import AddWordWidget

from ....vocabulary.manager import VocabularyManager

class VocabularyHeader(QWidget):
    def __init__(self, parent: QWidget, vocabulary_manager: VocabularyManager, vocabulary_list_view) -> None:
        super().__init__(parent)
        layout = QHBoxLayout(self)
        
        label = QLabel("Vocabulary List", self)
        label.setContentsMargins(0,0,0,0)
        label.setProperty("class", "title")
        layout.addWidget(label)

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        
        add_word_button = AddWordWidget(
            vocabulary_manager, vocabulary_list_view)
        add_word_button.layout().setContentsMargins(0,0,0,0)
        add_word_button.setContentsMargins(0,0,0,0)
        layout.addWidget(add_word_button)

    def sizeHint(self):
        width = int(self.parentWidget().width())
        height = int(self.parentWidget().height() * 0.2)
        return QSize(width, height)