from os import path

from PyQt6.QtWidgets import QWidget, QDialog, QVBoxLayout
from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtCore import pyqtSignal

from .body import DialogMeaningBody
from .bottom import DialogMeaningBottom


class MeaningDialog(QDialog):
    confirm_button_clicked_signal = pyqtSignal(QStandardItemModel, int)

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setWindowTitle("Word Meaning Editor")

        addon_base_dir = path.realpath(__file__)
        for i in range(5):
            addon_base_dir = path.dirname(addon_base_dir)

        css_file_path = path.join(addon_base_dir, "styles", "group_box.css")

        with open(css_file_path, "r") as css_file:
            self.setStyleSheet(css_file.read())

        self.resize(int(parent.parent().width() * 0.8),
                    int(parent.parent().height() * 0.8))
        self.current_selection = 1
        self._init_layout()

    def _init_layout(self):
        layout = QVBoxLayout(self)  # Main layout of Dialog
        self.setLayout(layout)

        self.body = DialogMeaningBody(self)
        layout.addWidget(self.body)

        self.bottom = DialogMeaningBottom(self)
        layout.addWidget(self.bottom)

    def open(self, vocabulary):
        self.vocabulary = vocabulary
        meaning_object = vocabulary.meaning_object

        self.current_selection = meaning_object.current_selection
        self.meaning_model = meaning_object.clone_model()
        
        self.body.set_to_new_vocabulary(self.meaning_model)

        self.bottom.spin_box.refresh(
            self.current_selection,
            self.meaning_model.rowCount())
        super().open()
