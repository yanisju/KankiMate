from os import path
from PyQt6.QtGui import QAction, QIcon


class DeleteAllKanjisAction(QAction):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setText("Delete All Kanjis")

        addon_base_dir = path.realpath(__file__)
        for i in range(8):
            addon_base_dir = path.dirname(addon_base_dir)

        icon_file_path = path.join(addon_base_dir, "data", "icons", "trashbin.png")
        self.setIcon(QIcon(icon_file_path))
        
        self.triggered.connect(self._action)

    def _action(self):
        self.parent().parent().kanji_data.clear()
