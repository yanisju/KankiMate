from os import path

from PyQt6.QtWidgets import QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton

from aqt import mw

from .widget.deck_selector import DeckSelector
from .widget.model_options import ModelOptions

from ....anki import AnkiManager


class DeckOptionsDialog(QDialog):
    def __init__(self, parent: QWidget, anki_manager: AnkiManager) -> None:
        super().__init__(parent)
        self.anki_manager = anki_manager
        self.setWindowTitle("Deck Options")

        self.modified = False

        self._configure()

        addon_base_dir = path.realpath(__file__)
        for i in range(5):
            addon_base_dir = path.dirname(addon_base_dir)

        css_file_path = path.join(addon_base_dir, "styles", "group_box.css")
        with open(css_file_path, "r") as css_file:
            self.setStyleSheet(css_file.read())

        

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
        if self.modified:
            self._modify_user_config()

            model_name = self.model_options.get_model_name()
            model_front, model_back, model_style = self.model_options.get_model_parameters()
            if self.anki_manager.is_model_existing(model_name):
                self.anki_manager.modify_model_parameters(model_name, model_front, model_back, model_style)
            else:
                self.anki_manager.create_new_model(model_name, model_front, model_back, model_style)

        return super().accept()
    
    def _model_name_is_modified(self):
        model_name = self.model_options.get_model_name()
        if self.anki_manager.is_model_existing(model_name) and not self.anki_manager.is_model_existing_valid(model_name):
            self.confirm_button.setDisabled(True)
        else:
            self.confirm_button.setEnabled(True)

    
    def _is_modified(self):
        self.modified = True

        if not self.model_options.model_name_widget.text_edit.toPlainText():
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