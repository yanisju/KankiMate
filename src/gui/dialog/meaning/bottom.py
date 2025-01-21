from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from .widget.spin_box import MeaningSpinBox

class DialogMeaningBottom(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        layout = QHBoxLayout(self)

        self.spin_box = MeaningSpinBox(parent)
        layout.addWidget(self.spin_box)

        self.confirm_button = QPushButton("Confirm")
        self.cancel_button = QPushButton("Cancel")
        layout.addWidget(self.confirm_button)
        layout.addWidget(self.cancel_button)

        self.confirm_button.clicked.connect(self._confirm_button_clicked)
        self.cancel_button.clicked.connect(parent.reject)

    def _confirm_button_clicked(self):
        self.parent().confirm_button_clicked_signal.emit(self.parent().table_view.model(),
                                                self.parent().current_selection)
        self.parent().accept()
