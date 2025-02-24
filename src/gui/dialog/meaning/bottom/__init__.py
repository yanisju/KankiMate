from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QSizePolicy
from typing import Tuple

from .meaning_attributes import MeaningAttributes
from .pitch_accent import PitchAccentWidget

from .....vocabulary.meaning import VocabularyMeaning

from .....constants import VocabularyJLPTLevel, VocabularyPitchAccent


class DialogMeaningBottom(QWidget):
    """
    A custom QWidget for the bottom part of the dialog, which contains meaning attributes,
    pitch accent widgets, and confirm/cancel buttons.
    """
    def __init__(self, parent):
        """
        Initializes the bottom part of the meaning dialog with the following:
        - Meaning attributes (e.g., common, JLPT level)
        - Pitch accent widget
        - Buttons (Confirm, Cancel)

        Parameters:
        -----------
        parent : QWidget
            The parent widget of this dialog.
        """
        super().__init__(parent)

        layout = QHBoxLayout(self)

        self.meaning_attributes = MeaningAttributes(self, parent)
        layout.addWidget(self.meaning_attributes, 25)

        self.pitch_accent_widget = PitchAccentWidget(self)
        layout.addWidget(self.pitch_accent_widget, 60)

        buttons_layout = QVBoxLayout()
        buttons_layout.addStretch()

        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        buttons_layout.addWidget(self.confirm_button)
        buttons_layout.addWidget(self.cancel_button)

        buttons_layout.addStretch()
        layout.addLayout(buttons_layout, 15)

    def update_content(self, meaning: VocabularyMeaning):
        """
        Updates the content of the meaning attributes and pitch accent widget based on the provided meaning.

        Parameters:
        -----------
        meaning : Meaning
            The meaning object containing the data to update the widgets.
        """
        self.meaning_attributes.update_content(meaning.current_selection,
                                               len(meaning.meanings),
                                               meaning.is_common,
                                               meaning.jlpt_level)
        
        self.pitch_accent_widget.update_content(meaning.kana_reading,
                                                meaning.pitch_accent,
                                                meaning.pitch_pattern)

    def get_values(self) -> Tuple[int, bool, VocabularyJLPTLevel, VocabularyPitchAccent, list[bool]]:
        """
        Retrieves the values from the meaning attributes and pitch accent widgets.

        Returns:
        --------
        Tuple[int, bool, VocabularyJLPTLevel, VocabularyPitchAccent, list[bool]]
            The values representing the current selection, common flag, JLPT level,
            pitch accent, and pitch pattern.
        """
        selection, is_common, jlpt_level = self.meaning_attributes.get_values()
        pitch_accent, pitch_pattern = self.pitch_accent_widget.get_values()

        return selection, is_common, jlpt_level, pitch_accent, pitch_pattern
