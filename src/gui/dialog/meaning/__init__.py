from PyQt6.QtWidgets import QWidget, QDialog, QVBoxLayout

from .body import DialogMeaningBody
from .bottom import DialogMeaningBottom

from ....vocabulary import Vocabulary


class MeaningDialog(QDialog):
    """
    A dialog window for editing the meaning of a vocabulary word.

    Attributes:
    -----------
    current_selection : int
        Keeps track of the currently selected meaning.
    vocabulary : Vocabulary
        The vocabulary object being edited.
    meaning : VocabularyMeaning
        A cloned version of the vocabulary's meaning, used for modifications.
    body : DialogMeaningBody
        The main content area where meanings are displayed.
    bottom : DialogMeaningBottom
        The bottom section containing controls such as confirm and cancel buttons.
    """

    def __init__(self, parent: QWidget) -> None:
        """
        Initializes the MeaningDialog.

        Parameters:
        -----------
        parent : QWidget
            The parent widget of this dialog.
        """
        super().__init__(parent)
        self.setWindowTitle("Word Meaning Editor")

        # Resize the dialog to 65% of the parent width and 90% of the parent height.
        self.resize(int(parent.parent().width() * 0.65),
                    int(parent.parent().height() * 0.9))
        self.current_selection = 1
        self._init_layout()

    def _init_layout(self):
        """
        Initializes and sets up the layout of the dialog.
        """
        layout = QVBoxLayout(self) 
        self.setLayout(layout)

        # Add the body section that displays vocabulary meanings.
        self.body = DialogMeaningBody(self)
        layout.addWidget(self.body, 75)

        # Add the bottom section that contains the confirm and cancel buttons.
        self.bottom = DialogMeaningBottom(self)

        self.bottom.confirm_button.clicked.connect(self.accept)
        self.bottom.cancel_button.clicked.connect(self.reject)

        layout.addWidget(self.bottom, 25)

    def open(self, vocabulary: Vocabulary):
        """
        Opens the dialog with the provided vocabulary data.

        Parameters:
        -----------
        vocabulary : Vocabulary
            The vocabulary object whose meaning is being edited.
        """
        self.vocabulary = vocabulary
        meaning = vocabulary.meaning

        # Store the current selection and create a clone for modifications.
        self.current_selection = meaning.current_selection
        self.meaning = meaning.clone()
        
        # Update the dialog body and bottom sections with the new vocabulary data.
        self.body.set_to_new_vocabulary(self.meaning.standard_item_model)
        self.bottom.update_content(meaning)
        
        super().open()

    def accept(self):
        """
        Confirms the changes and updates the vocabulary's meaning attributes.
        """
        # Retrieve updated values from the bottom section.
        meaning_model = self.body.table_view.model()
        selection, is_common, jlpt_level, pitch_accent, pitch_pattern = self.bottom.get_values()

        # Apply the changes to the original vocabulary meaning.
        self.vocabulary.update_meaning(meaning_model, selection, is_common, jlpt_level, pitch_accent, pitch_pattern)

        return super().accept()
