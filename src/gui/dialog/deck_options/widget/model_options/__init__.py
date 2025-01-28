from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QPushButton
from PyQt6.QtCore import pyqtSignal

from .name import NameModelOptions
from .dialog import ModelOptionDialog

from ......constants import ModelDialogOptionsMode

class ModelOptions(QGroupBox):
    is_modified = pyqtSignal()

    def __init__(self, parent, deck_selector_combobox):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.model_name_widget = NameModelOptions(self)
        self.model_name_widget.text_edit.textChanged.connect(self._is_parameter_modified)
        layout.addWidget(self.model_name_widget)

        modify_button_front = QPushButton(self)
        self.modify_button_front_dialog = ModelOptionDialog(self, ModelDialogOptionsMode.FRONT_MODEL, deck_selector_combobox)
        self.modify_button_front_dialog.confirm_button.clicked.connect(self._is_parameter_modified)
        modify_button_front.clicked.connect(self.modify_button_front_dialog.open)
        modify_button_front.setText("Modify Model Front")
        layout.addWidget(modify_button_front)

        modify_button_back = QPushButton(self)
        self.modify_button_back_dialog = ModelOptionDialog(self, ModelDialogOptionsMode.BACK_MODEL, deck_selector_combobox)
        self.modify_button_back_dialog.confirm_button.clicked.connect(self._is_parameter_modified)
        modify_button_back.clicked.connect(self.modify_button_back_dialog.open)
        modify_button_back.setText("Modify Model Back")
        layout.addWidget(modify_button_back)

        modify_button_style = QPushButton(self)
        self.modify_button_style_dialog = ModelOptionDialog(self, ModelDialogOptionsMode.STYLE_MODEL, deck_selector_combobox)
        self.modify_button_style_dialog.confirm_button.clicked.connect(self._is_parameter_modified)
        modify_button_style.clicked.connect(self.modify_button_style_dialog.open)
        modify_button_style.setText("Modify Model Style")
        layout.addWidget(modify_button_style)

    def configure(self, model_name: str, model_front: str, model_back: str, model_style: str):
        self.model_name_widget.text_edit.setText(model_name)

        self.modify_button_front_dialog.configure(model_front)
        self.modify_button_back_dialog.configure(model_back)
        self.modify_button_style_dialog.configure(model_style)

    def get_model_name(self):
        return self.model_name_widget.text_edit.toPlainText()
        
    def get_model_parameters(self):
        model_front = self.modify_button_front_dialog.parameter_str
        model_back = self.modify_button_back_dialog.parameter_str
        model_style = self.modify_button_style_dialog.parameter_str
        return model_front, model_back, model_style
    
    def _is_parameter_modified(self):
        """Emit signal if one of the parameter is modified. """
        self.is_modified.emit()