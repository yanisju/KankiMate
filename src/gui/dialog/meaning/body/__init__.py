from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QLabel

from .text_view import MeaningTextView
from .table_view import MeaningTableView

class DialogMeaningBody(QGroupBox):
    """
    A group box containing the main content area for displaying word meanings.

    This component consists of:
    - A title label
    - A text view for displaying meaning details
    - A table view for structured representation of meanings
    """

    def __init__(self, parent):
        """
        Initializes the meaning body section.

        Parameters:
        -----------
        parent : QWidget
            The parent widget of this group box.
        """
        super().__init__(parent)
        layout = QVBoxLayout(self)

        # Title label for the section
        label = QLabel("Word Meanings", self)
        label.setProperty("class", "title") 
        layout.addWidget(label, 10)

        # Text view for displaying the meaning in a textual format
        self.meaning_view = MeaningTextView(self)
        layout.addWidget(self.meaning_view, 45)

        # Table view for displaying structured meaning data
        self.table_view = MeaningTableView(self)
        layout.addWidget(self.table_view, 45)
    
    def set_to_new_vocabulary(self, meaning_model):
        """
        Updates the views with a new vocabulary model.

        Parameters:
        -----------
        meaning_model : QAbstractItemModel
            The model containing the meanings to display.
        """

        # Check if table_view already has a model
        table_view_model = self.table_view.model()
        if table_view_model:
            table_view_model.dataChanged.disconnect()

        self.table_view.setModel(meaning_model)  # Update the table view with the new model
        self.meaning_view.set_text(meaning_model)  # Update the text view with the new meaning data

        self.table_view.model().rowsInserted.connect(self._update_text_view)
        self.table_view.model().dataChanged.connect(self._update_text_view)
        self.table_view.model().rowsRemoved.connect(self._update_text_view)
        

    def _update_text_view(self):
        self.meaning_view.set_text(self.table_view.model())
