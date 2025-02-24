from PyQt6.QtWidgets import QComboBox, QLabel, QFormLayout, QWidget
from ......constants import VocabularyPitchAccent


class PitchAccentComboBox(QWidget):
    """
    A custom widget containing a combo box for selecting the pitch accent of a word.
    """
    def __init__(self, parent=None):
        """
        Initializes the PitchAccentComboBox widget.

        Parameters:
        -----------
        parent : QWidget, optional
            The parent widget of this widget (default is None).
        """
        super().__init__(parent)

        layout = QFormLayout(self)

        label = QLabel("Pitch Accent: ")
        label.setProperty("class", "attributes")

        self.combobox = QComboBox(self)

        self._init_combobox()
        layout.addRow(label, self.combobox)

    def _init_combobox(self):
        """
        Initializes the combo box with predefined pitch accent options.
        """
        # Add pitch accent items to the combo box with their corresponding constant values
        self.combobox.addItem("頭高 / あたまだか", VocabularyPitchAccent.ATAMADAKA)
        self.combobox.addItem("中高 / なかだか", VocabularyPitchAccent.NAKADAKA)
        self.combobox.addItem("尾高 / おだか", VocabularyPitchAccent.ODAKA)
        self.combobox.addItem("平板 / へいばん", VocabularyPitchAccent.HEIBAN)
        self.combobox.addItem("Unknown", VocabularyPitchAccent.UNKNOWN)

    def set_combobox(self, pitch_accent):
        """
        Sets the selected item in the combo box based on the given pitch accent value.

        Parameters:
        -----------
        pitch_accent : VocabularyPitchAccent
            The pitch accent to set in the combo box.
        """
        self.combobox.setCurrentIndex(pitch_accent.value)
