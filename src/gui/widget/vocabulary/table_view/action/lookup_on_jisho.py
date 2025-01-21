from os import path
from PyQt6.QtGui import QAction, QIcon

import webbrowser


class LookupOnJishoAction(QAction):
    def __init__(self, parent, vocabulary_manager) -> None:
        super().__init__(parent)
        self.vocabulary_manager = vocabulary_manager
        self.setText("Lookup on Jisho")

        addon_base_dir = path.realpath(__file__)
        for i in range(7):
            addon_base_dir = path.dirname(addon_base_dir)

        icon_file_path = path.join(addon_base_dir, "data", "icons", "magnifying_glass.png")
        self.setIcon(QIcon(icon_file_path))

        self.triggered.connect(self._action)

    def _action(self):
        word = self.vocabulary_manager.get_word(self.parent().row)
        url = "https://jisho.org/search/" + word
        webbrowser.open(url, 0)
