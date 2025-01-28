from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QLabel

from .....constants.exceptions import VocabularyAlreadyExists, VocabularyIsNotValid

class AddWordWidget(QWidget):
    """Button to add a single word."""

    def __init__(self, vocabulary_manager, vocabulary_list_view) -> None:
        super().__init__()
        self.vocabulary_manager = vocabulary_manager

        layout = QHBoxLayout(self)

        formLayout = QFormLayout()
        self.line_edit = QLineEdit()
        label = QLabel("Enter Vocabulary:")
        label.setProperty("class", "attributes")
        formLayout.addRow(label, self.line_edit)
        self.button = QPushButton("  Confirm  ")
        self.button.setEnabled(False)

        layout.addLayout(formLayout)
        layout.addWidget(self.button)

        self.line_edit.textEdited.connect(self.get_text)

        self.line_edit.returnPressed.connect(self.add_word_to_manager)
        self.button.clicked.connect(
            self.add_word_to_manager)  # Add word to manager
        self.button.clicked.connect(
            vocabulary_list_view.scrollToBottom)  # Scroll to bottom

        self.setSizePolicy(
            QSizePolicy.Policy.Maximum,
            QSizePolicy.Policy.Fixed)

    def get_text(self, text: str):
        self.text = text.strip()
        if self.text == "":
            self.button.setEnabled(False)
        else:
            self.button.setEnabled(True)

    def add_word_to_manager(self):
        try:
            self.vocabulary_manager.add_word(self.text)
        except VocabularyAlreadyExists as exception:
            QMessageBox.critical(self.parent(), "Importation Error", f"{exception}")
        except VocabularyIsNotValid as exception:
            QMessageBox.critical(self.parent(), "Importation Error", f"{exception}")
        except Exception as e:
            QMessageBox.critical(self.parent(), "Importation Error", f"An exception has occured: {e}")
