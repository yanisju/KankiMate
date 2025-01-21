from os import path
from PyQt6.QtGui import QAction, QIcon


class DeleteOneKanjiAction(QAction):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setText("Delete Kanji")

        addon_base_dir = path.realpath(__file__)
        for i in range(8):
            addon_base_dir = path.dirname(addon_base_dir)

        icon_file_path = path.join(addon_base_dir, "data", "icons", "minus.png")
        self.setIcon(QIcon(icon_file_path))

        self.triggered.connect(self._action)

    def _action(self):
        for row, _ in reversed(self.parent().rows_columns):
            self.parent().parent().kanji_data.remove_by_row(row)
