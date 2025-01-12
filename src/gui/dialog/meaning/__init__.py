from os import path

from PyQt6.QtWidgets import QWidget, QDialog, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtCore import pyqtSignal

from .widget.header import DialogMeaningHeader
from .widget.meaning import MeaningWidget


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

        self.header = DialogMeaningHeader(self)
        layout.addWidget(self.header)

        self.meaning_widget = MeaningWidget(self)
        layout.addWidget(self.meaning_widget)

        buttons_layout = QHBoxLayout()  # Layout for bottom buttons
        layout.addLayout(buttons_layout)
        self._init_buttons_layout(buttons_layout)

    def _init_buttons_layout(self, layout):
        self.confirm_button = QPushButton("Confirm")
        cancel_button = QPushButton("Cancel")
        layout.addWidget(self.confirm_button)
        layout.addWidget(cancel_button)
        self.confirm_button.clicked.connect(self._confirm_button_clicked)
        cancel_button.clicked.connect(self.reject)

    def _confirm_button_clicked(self):
        self.confirm_button_clicked_signal.emit(self.table_view.model(),
                                                self.current_selection)
        self.accept()

    def open(self, vocabulary):
        self.vocabulary = vocabulary
        meaning_object = vocabulary.meaning_object

        self.current_selection = meaning_object.current_selection
        self.meaning_model = meaning_object.clone_model()
        
        self.meaning_widget.set_to_new_vocabulary(self.meaning_model)

        self.header.selection_spin_box.refresh(
            self.current_selection,
            self.meaning_model.rowCount())
        super().open()
