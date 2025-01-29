from PyQt6.QtWidgets import QLabel, QFormLayout, QWidget, QLineEdit

class NameModelOptions(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        layout = QFormLayout(self)

        label = QLabel("Model Name: ")
        label.setProperty("class", "attributes")
        self.text_edit = QLineEdit(self)

        layout.addRow(label, self.text_edit)