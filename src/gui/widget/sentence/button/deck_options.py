from PyQt6.QtWidgets import QPushButton

from ....dialog.deck_options import DeckOptionsDialog

class DeckOptionsButtons(QPushButton):
    def __init__(self, parent):
        super().__init__("Options", parent)
        self.deck_option_dialog = DeckOptionsDialog(self.parent())
        self.clicked.connect(self.deck_option_dialog.open)
