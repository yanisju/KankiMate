from os import path
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QStandardItemModel


class MeaningTextView(QTextEdit):
    """
    A custom QTextEdit widget for displaying word meanings in HTML format.
    """
    def __init__(self, parent) -> None:
        """
        Initializes the text view widget as read-only.

        Parameters:
        -----------
        parent : QWidget
            The parent widget of this text view.
        """
        super().__init__(parent)
        self.setReadOnly(True)

    def set_text(self, model: QStandardItemModel):
        """
        Sets the content of the text view from a given QStandardItemModel.
        
        Parameters:
        -----------
        model : QStandardItemModel
            A model containing the word meanings and parts of speech to display.
        """
        # Get the base directory of the addon by traversing up from the current file
        addon_base_dir = path.realpath(__file__)
        for i in range(6):
            addon_base_dir = path.dirname(addon_base_dir)

        html_file_path = path.join(addon_base_dir, "styles", "text_view.html")
        with open(html_file_path, "r") as html_file:
            text = html_file.read()

        # Iterate through the rows of the model and build the content
        for i in range(model.rowCount()):
            # Extract meaning and part of speech from the model
            meaning = model.item(i, 0).text()
            part_of_speech = model.item(i, 1).text()
            
            # Append the formatted text for each entry
            text += self._get_text_line(i, meaning, part_of_speech)

        # Set the HTML content to be displayed in the QTextEdit widget
        self.setHtml(text)

    def _get_text_line(self, index, meaning, part_of_speech):
        """
        Generates an HTML line for a word meaning entry.

        Parameters:
        -----------
        index : int
            The index of the current entry in the model.
        meaning : str
            The meaning of the word.
        part_of_speech : str
            The part of speech associated with the word.

        Returns:
        --------
        str
            The HTML string for displaying a single entry with its index, meaning, 
            and part of speech.
        """

        return f"""
            <div class='entry'>
                <span class='index'>{index + 1}.</span>
                <span class='meaning'>{meaning}</span>
                <span class='part-of-speech'>({part_of_speech})</span>
            </div>
        """