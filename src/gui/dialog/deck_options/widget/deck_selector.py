from aqt import mw

from PyQt6.QtWidgets import QLabel, QHBoxLayout, QWidget, QComboBox

class DeckSelector(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        layout = QHBoxLayout(self)

        label = QLabel("Deck: ")
        label.setProperty("class", "attributes")
        layout.addWidget(label)

        self.combobox = QComboBox(self)
        layout.addWidget(self.combobox)

    def update_combobox(self, user_deck_name: str): # TODO: test if is working
        """Update combobox with deck names, and set it to user deck."""
        self.combobox.clear()
        
        index_deck = -1
        for i, deck_name in enumerate(mw.col.decks.all_names()):
            self.combobox.addItem(deck_name, deck_name)
            if deck_name == user_deck_name:
                    index_deck = i
        self.combobox.setCurrentIndex(index_deck)
    
    def get_deck_name(self) -> str:
        return self.combobox.currentData()
        