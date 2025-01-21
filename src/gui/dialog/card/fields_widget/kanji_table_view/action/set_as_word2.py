from os import path

from PyQt6.QtGui import QAction, QIcon


class SetAsWord2Action(QAction):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setText("Set as Word 2")

        addon_base_dir = path.realpath(__file__)
        for i in range(8):
            addon_base_dir = path.dirname(addon_base_dir)

        icon_file_path = path.join(addon_base_dir, "data", "icons", "gear.png")
        self.setIcon(QIcon(icon_file_path))

        self.triggered.connect(self._action)

    def _action(self):
        row, _ = self.parent().rows_columns[0]
        self.parent().parent().parent(
        ).sentence_attributes_widget.word2_combobox.setCurrentIndex(row)
