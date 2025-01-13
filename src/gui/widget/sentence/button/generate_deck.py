from PyQt6.QtWidgets import QPushButton
from .....vocabulary.manager import VocabularyManager

class GenerateDeckButton(QPushButton):
    def __init__(self, parent, vocabulary_manager: VocabularyManager):
        super().__init__("Generate Deck", parent)
        self.setEnabled(False)
        self.vocabulary_manager = vocabulary_manager

        self.clicked.connect(vocabulary_manager.generate_deck)
        vocabulary_manager.sentence_added_to_deck.sentences_model.modified.connect(self.enable_disable)
        
    def enable_disable(self):
        if len(self.vocabulary_manager.sentence_added_to_deck) == 0:
            self.setEnabled(False)
        else:
            self.setEnabled(True)