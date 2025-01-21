from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QHBoxLayout, QLabel

from .widget.text_view import MeaningTextView
from .widget.table_view import MeaningTableView

class DialogMeaningBody(QGroupBox):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        label = QLabel("Word Meanings", self)
        label.setProperty("class", "title")
        layout.addWidget(label)

        horizontal_layout = QHBoxLayout()
        layout.addLayout(horizontal_layout)

        self.meaning_view = MeaningTextView(self)
        layout.addWidget(self.meaning_view)

        self.table_view = MeaningTableView(self)
        layout.addWidget(self.table_view)
    
    def set_to_new_vocabulary(self, meaning_model):
        self.table_view.setModel(meaning_model)
        self.meaning_view.set_text(meaning_model)