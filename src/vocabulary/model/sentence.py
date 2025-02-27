from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtCore import pyqtSignal, Qt

from ..sentence import Sentence


class SentenceModel(QStandardItemModel):
    """
    A model that manages and displays sentences with their associated data.

    This class is an extension of QStandardItemModel designed to handle sentences, including their translations
    and key words, in a structured table format.

    Attributes:
    -----------
    sentences : list
        A list containing the Sentence objects currently held by the model.

    Methods:
    --------
    append_sentence(sentence):
        Adds a new sentence to the model.
    modify_row(sentence, row):
        Modifies an existing sentence in the model at the specified row.
    refresh(sentences):
        Clears and repopulates the model with a new list of sentences.
    get_sentence_by_row(row):
        Retrieves a sentence by its row index in the model.
    remove_row(row):
        Removes a sentence from the model and its corresponding row.
    """

    modified = pyqtSignal()

    def __init__(self, sentence_manager):
        """
        Initializes the SentenceModel with a predefined structure of four columns.
        """
        super().__init__(0, 4)
        self.sentence_manager = sentence_manager
        self._configure()

    def _configure(self):
        """
        Configures the model headers to label each column.
        """
        self.setHeaderData(0, Qt.Orientation.Horizontal, "Sentence")
        self.setHeaderData(1, Qt.Orientation.Horizontal, "Meaning")
        self.setHeaderData(2, Qt.Orientation.Horizontal, "Word 1")
        self.setHeaderData(3, Qt.Orientation.Horizontal, "Word 2")

    def append_sentence(self, sentence: Sentence):
        """
        Adds a new sentence to the model.

        This method appends a Sentence object to the model and updates the corresponding row with the sentence's data.

        Args:
        -----
        sentence : Sentence
            The Sentence object to be added to the model.
        """
        sentence.compute_standard_item()
        self.appendRow(sentence.standard_item)
        self.modified.emit()

    def modify_row(self, sentence: Sentence, row: int):
        """
        Modifies an existing sentence in the model at the specified row.

        This method updates the Sentence object and its display data in the model at the given row index.

        Args:
        -----
        sentence : Sentence
            The Sentence object with updated data.
        row : int
            The index of the row to be modified.
        """
        self.sentence_manager[row] = sentence
        for j in range(len(sentence.standard_item)):
            sentence.compute_standard_item()
            self.setItem(row, j, sentence.standard_item[j])

    def get_sentence_by_row(self, row):
        """
        Retrieves a sentence by its row index in the model.

        Args:
        -----
        row : int
            The index of the row for which to retrieve the sentence.

        Returns:
        --------
        Sentence
            The Sentence object corresponding to the given row index.
        """
        return self.sentence_manager[row]

    def remove_row(self, row):
        """
        Removes a sentence from the model and its corresponding row.

        This method deletes a sentence from the model and removes its associated row.

        Args:
        -----
        row : int
            The index of the row to be removed.
        """
        self.removeRow(row)
        self.modified.emit()

    def remove_all_rows(self):
        self.removeRows(0, self.rowCount())
        self.modified.emit()
