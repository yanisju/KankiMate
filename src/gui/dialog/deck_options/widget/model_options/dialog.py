from PyQt6.QtWidgets import QDialog, QVBoxLayout, QGroupBox, QTextEdit, QHBoxLayout, QPushButton, QComboBox

from ......constants import ModelDialogOptionsMode

class ModelOptionDialog(QDialog):
    """Dialog for a model option in Anki. (name, front, back or style)"""
    def __init__(self, parent, mode: ModelDialogOptionsMode, deck_selector_combobox: QComboBox):
        super().__init__(parent)

        self.mode = mode
        self.deck_selector_combobox = deck_selector_combobox
        self.parameter_str = "" # Parameter

        layout = QVBoxLayout(self)

        self.group_box = QGroupBox(self)
        group_box_layout = QVBoxLayout(self.group_box)

        self.text_edit = QTextEdit(self)
        self.text_edit.textChanged.connect(self._text_edit_modified)
        group_box_layout.addWidget(self.text_edit)
        layout.addWidget(self.group_box)

        buttons_layout = QHBoxLayout()
        layout.addLayout(buttons_layout)

        self.confirm_button = QPushButton(self)
        self.confirm_button.setText("Confirm")
        self.confirm_button.clicked.connect(self.accept)
        buttons_layout.addWidget(self.confirm_button)

        reject_button = QPushButton(self)
        reject_button.setText("Cancel")
        reject_button.clicked.connect(self.reject)
        buttons_layout.addWidget(reject_button)

    def setTitle(self, mode: ModelDialogOptionsMode):
        if mode == ModelDialogOptionsMode.FRONT_MODEL:
            self.setTitle("Model Front")
            self.group_box.setTitle("Model Front")
        elif mode == ModelDialogOptionsMode.BACK_MODEL:
            self.setTitle("Model Back")
            self.group_box.setTitle("Model Back")
        else:
            self.setTitle("Model Style")
            self.group_box.setTitle("Model Style")

    def open(self):
        self.text_edit.setText(self.parameter_str)
        return super().open()

    def accept(self):
        self.parameter_str = self.text_edit.toPlainText()
        return super().accept()

    def configure(self, parameter_str: str):
        self.parameter_str = parameter_str
        self.text_edit.setText(parameter_str)

    def _text_edit_modified(self):
        if not self.text_edit.toPlainText() and self.mode != ModelDialogOptionsMode.STYLE_MODEL:
            self.confirm_button.setDisabled(True)