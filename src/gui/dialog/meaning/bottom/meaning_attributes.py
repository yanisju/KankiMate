from PyQt6.QtWidgets import QGroupBox, QSpinBox, QFormLayout, QLabel, QCheckBox, QComboBox, QVBoxLayout
from PyQt6.QtCore import Qt

from typing import Tuple

from .word_audio_player_button import WordAudioPlayerButton
from .....constants import VocabularyJLPTLevel


class MeaningAttributes(QGroupBox):
    """
    A custom widget that displays word attributes such as:
    - Current selection (SpinBox)
    - Is common (CheckBox)
    - JLPT level (ComboBox)
    """
    def __init__(self, parent, meaning_dialog) -> None:
        """
        Initializes the widget, setting the parent and the reference to the meaning dialog.

        Parameters:
        -----------
        parent : QWidget
            The parent widget of this widget.

        meaning_dialog : QWidget
            The reference to the meaning dialog which contains this widget.
        """
        super().__init__(parent)
        self.meaning_dialog = meaning_dialog

        layout = QVBoxLayout(self)

        label = QLabel("Word Attributes", self)
        label.setProperty("class", "title")
        layout.addWidget(label)

        layout.addStretch()

        form_layout = QFormLayout()
        layout.addLayout(form_layout)

        # Initialize the widgets (SpinBox, CheckBox, ComboBox) and add them to the form layout
        # self._init_word_audio_player(form_layout)
        self._init_selection_spin_box(form_layout)
        self._init_is_common_check_box(form_layout)
        self._init_jlpt_level_combo_box(form_layout)

        layout.addStretch()

    def _init_word_audio_player(self, layout: QFormLayout):
        label = QLabel("Listen: ", self)
        label.setProperty("class", "attributes")

        self.word_audio_player_button = WordAudioPlayerButton(self)

        layout.addRow(label, self.word_audio_player_button)

    def _init_selection_spin_box(self, layout: QFormLayout):
        """
        Initializes the SpinBox widget for selecting the current selection.

        Parameters:
        -----------
        layout : QFormLayout
            The form layout to add the widget to.
        """
        label = QLabel("Current Selection: ", self)
        label.setProperty("class", "attributes")

        self.selection_spin_box = QSpinBox(self)
        self.selection_spin_box.setMinimum(1)
        self.selection_spin_box.valueChanged.connect(self._set_current_selection)

        layout.addRow(label, self.selection_spin_box)

    def _init_is_common_check_box(self, layout: QFormLayout):
        """
        Initializes the CheckBox widget for the 'Is Common?' attribute.

        Parameters:
        -----------
        layout : QFormLayout
            The form layout to add the widget to.
        """
        label = QLabel("Is Common ?", self)
        label.setProperty("class", "attributes")

        self.is_common_check_box = QCheckBox(self)

        layout.addRow(label, self.is_common_check_box)

    def _init_jlpt_level_combo_box(self, layout: QFormLayout):
        """
        Initializes the ComboBox widget for selecting the JLPT level.

        Parameters:
        -----------
        layout : QFormLayout
            The form layout to add the widget to.
        """
        label = QLabel("JLPT Level: ", self)
        label.setProperty("class", "attributes")

        # Create the ComboBox and add JLPT levels as items
        self.jlpt_level_combo_box = QComboBox(self)
        self.jlpt_level_combo_box.addItem("Unknown", VocabularyJLPTLevel.UNKNOWN)
        self.jlpt_level_combo_box.addItem("N1", VocabularyJLPTLevel.JLPT_N1)
        self.jlpt_level_combo_box.addItem("N2", VocabularyJLPTLevel.JLPT_N2)
        self.jlpt_level_combo_box.addItem("N3", VocabularyJLPTLevel.JLPT_N3)
        self.jlpt_level_combo_box.addItem("N4", VocabularyJLPTLevel.JLPT_N4)
        self.jlpt_level_combo_box.addItem("N5", VocabularyJLPTLevel.JLPT_N5)

        # Add the label and ComboBox to the form layout
        layout.addRow(label, self.jlpt_level_combo_box)

    def update_content(self, current_selection: int, row_length: int, is_common: bool, jlpt_level: VocabularyJLPTLevel):
        """
        Updates the content of the widgets with the provided data.

        Parameters:
        -----------
        current_selection : int
            The current selection value.

        row_length : int
            The maximum value for the selection SpinBox.

        is_common : bool
            Whether the word is common.

        jlpt_level : VocabularyJLPTLevel
            The JLPT level.
        """
        # Update the SpinBox value and set its maximum value
        self.selection_spin_box.setValue(current_selection)
        self.selection_spin_box.setMaximum(row_length)

        # Toggle the state of the CheckBox based on whether the word is common
        if is_common and not self.is_common_check_box.isChecked() or not is_common and self.is_common_check_box.isChecked():
            self.is_common_check_box.toggle()

        # Set the ComboBox index based on the JLPT level
        self.jlpt_level_combo_box.setCurrentIndex(jlpt_level.value)

    def _set_current_selection(self, new_current_selection):
        """
        Updates the current selection in the meaning dialog.

        Parameters:
        -----------
        new_current_selection : int
            The new value for the current selection.
        """
        self.meaning_dialog.current_selection = new_current_selection

    def get_values(self) -> Tuple[int, bool, VocabularyJLPTLevel]:
        """
        Retrieves the values from the widgets.

        Returns:
        --------
        Tuple[int, bool, VocabularyJLPTLevel]
            The current selection, common status, and JLPT level.
        """
        # Get the current value of the SpinBox
        selection = self.selection_spin_box.value()

        # Get the status of the 'Is Common?' CheckBox
        if self.is_common_check_box.checkState() == Qt.CheckState.Checked:
            is_common = True
        else:
            is_common = False

        # Get the current data of the JLPT level ComboBox
        jlpt_level = self.jlpt_level_combo_box.currentData()

        return selection, is_common, jlpt_level
