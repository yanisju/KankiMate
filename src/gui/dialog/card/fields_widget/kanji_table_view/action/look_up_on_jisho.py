from os import path
from PyQt6.QtGui import QAction, QIcon

import webbrowser


class LookupOnJishoAction(QAction):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setText("Lookup on Jisho")

        addon_base_dir = path.realpath(__file__)
        for i in range(8):
            addon_base_dir = path.dirname(addon_base_dir)

        icon_file_path = path.join(addon_base_dir, "data", "icons", "magnifying_glass.png")
        self.setIcon(QIcon(icon_file_path))

        self.triggered.connect(self._action)

    def _action(self):
        for row, _ in self.parent().rows_columns:
            word = self.parent().parent().model().item(row, 0).text()
            if word != "":
                url = "https://jisho.org/search/" + word
                webbrowser.open(url, 0)
