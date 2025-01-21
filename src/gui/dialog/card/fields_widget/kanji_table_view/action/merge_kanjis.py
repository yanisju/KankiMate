from os import path
from PyQt6.QtGui import QAction, QIcon


class MergeKanjisAction(QAction):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setText("Merge Kanjis")
        
        addon_base_dir = path.realpath(__file__)
        for i in range(8):
            addon_base_dir = path.dirname(addon_base_dir)

        icon_file_path = path.join(addon_base_dir, "data", "icons", "merge.png")
        self.setIcon(QIcon(icon_file_path))

        self.triggered.connect(self._action)

    def _action(self):
        rows_columns = self.parent().rows_columns
        rows = []
        for i in range(len(rows_columns)):
            rows.append(rows_columns[i][0])
        self.parent().parent().kanji_data.merge_kanjis(rows)
