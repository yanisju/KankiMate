from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton

from aqt import mw

from .widget.deck_selector import DeckSelector
from .widget.model_options import ModelOptions

from ....anki import AnkiManager


class DeckOptionsDialog(QDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setWindowTitle("Deck and Model Options")

        self.modified = False

        self._configure()

    def _configure(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.deck_selector = DeckSelector(self)
        self.deck_selector.combobox.currentIndexChanged.connect(self._is_modified)
        layout.addWidget(self.deck_selector)

        self.model_options = ModelOptions(self, self.deck_selector.combobox)
        self.model_options.is_modified.connect(self._is_modified)
        layout.addWidget(self.model_options)

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

    def open(self):
        self.modified = False

        config = mw.addonManager.getConfig(__name__)
        self.deck_selector.update_combobox(config["deck_name"])
        self.model_options.configure(config["model_name"], config["model_front"], config["model_back"], config["model_style"])
        super().open()

    def accept(self):
        model_is_correct = True

        if self.modified:
            model_name = self.model_options.get_model_name()
            model_front, model_back, model_style = self.model_options.get_model_parameters()

            if AnkiManager.is_model_existing(model_name):
                model_is_correct = AnkiManager.modify_model_parameters(model_name, model_front, model_back, model_style)
            else:
                model_is_correct = AnkiManager.create_new_model(model_name, model_front, model_back, model_style)

            if model_is_correct:
                self._modify_user_config()
                super().accept()
        else:
            super().accept()
    
    def _model_name_is_modified(self):
        model_name = self.model_options.get_model_name()
        if AnkiManager.is_model_existing(model_name) and not AnkiManager.is_model_existing_valid(model_name):
            self.confirm_button.setDisabled(True)
        else:
            self.confirm_button.setEnabled(True)

    
    def _is_modified(self):
        self.modified = True

        if not self.model_options.model_name_widget.text_edit.text():
            self.confirm_button.setDisabled(True)
        else:
            self.confirm_button.setEnabled(True)
            
    
    def _modify_user_config(self):
        config = mw.addonManager.getConfig(__name__)
        config["deck_name"] = self.deck_selector.get_deck_name()

        model_name = self.model_options.get_model_name()
        model_front, model_back, model_style = self.model_options.get_model_parameters()
        config["model_name"] = model_name
        config["model_front"] = model_front
        config["model_back"] = model_back
        config["model_style"] = model_style
        mw.addonManager.writeConfig(__name__, config)