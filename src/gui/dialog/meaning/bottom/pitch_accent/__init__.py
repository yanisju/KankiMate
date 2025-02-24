from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QLabel
from typing import Tuple

from .pattern import PitchPatternWidget
from .combobox import PitchAccentComboBox

from ......constants import VocabularyPitchAccent


class PitchAccentWidget(QGroupBox):
    """
    A custom widget that allows the user to select and visualize the pitch accent and pattern of a word.
    """
    def __init__(self, parent):
        """
        Initializes the PitchAccentWidget, setting up the layout and child widgets.

        Parameters:
        -----------
        parent : QWidget
            The parent widget of this widget.
        """
        super().__init__(parent)

        layout = QVBoxLayout(self)

        label = QLabel("Word Pitch Accent", self)
        label.setProperty("class", "title")
        layout.addWidget(label)

        layout.addStretch()

        self.pitch_accent_combo_box = PitchAccentComboBox(self)
        layout.addWidget(self.pitch_accent_combo_box)
        
        self.pitch_pattern = PitchPatternWidget(self)
        layout.addWidget(self.pitch_pattern)

        layout.addStretch()

    def update_content(self, kana_reading: str, pitch_accent: VocabularyPitchAccent, pitch_pattern: list[bool]):
        """
        Updates the content of the widget with the given word's pitch accent and pitch pattern.

        Parameters:
        -----------
        word : str
            The word whose pitch accent and pattern are being displayed.

        pitch_accent : VocabularyPitchAccent
            The pitch accent of the word.

        pitch_pattern : list[bool]
            A list representing the pitch pattern of the word.
        """
        # Update the combo box with the given pitch accent
        self.pitch_accent_combo_box.set_combobox(pitch_accent)
        
        # Update the pitch pattern widget with the word's pitch pattern
        self.pitch_pattern.update_content(kana_reading, pitch_pattern)

    def get_values(self) -> Tuple[VocabularyPitchAccent, list[bool]]:
        """
        Retrieves the current values from the widget.

        Returns:
        --------
        Tuple[VocabularyPitchAccent, list[bool]]
            The current pitch accent and pitch pattern selected in the widget.
        """
        # Get the selected pitch accent from the combo box
        pitch_accent = self.pitch_accent_combo_box.combobox.currentData()

        # Get the pitch pattern from the pitch pattern widget
        pitch_pattern = self.pitch_pattern.pitch_pattern_scene.pitch_pattern

        return pitch_accent, pitch_pattern
