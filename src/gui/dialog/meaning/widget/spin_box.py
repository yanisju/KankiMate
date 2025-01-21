from PyQt6.QtWidgets import QWidget, QSpinBox, QHBoxLayout, QLabel

class MeaningSpinBox(QWidget):
    def __init__(self, meaning_dialog) -> None:
        super().__init__(None)
        self.meaning_dialog = meaning_dialog

        layout = QHBoxLayout(self)
        label = QLabel("Current Selection: ", self)
        label.setProperty("class", "attributes")
        layout.addWidget(label)

        self.spin_box = QSpinBox()
        self.spin_box.setMinimum(1)
        self.spin_box.valueChanged.connect(self._set_current_selection)
        layout.addWidget(self.spin_box)

    def refresh(self, current_selection: int, row_length: int):
        """Refresh values and set maximum of SpinBox."""
        self.spin_box.setValue(current_selection)
        self.spin_box.setMaximum(row_length)

    def _set_current_selection(self, new_current_selection):
        self.meaning_dialog.current_selection = new_current_selection