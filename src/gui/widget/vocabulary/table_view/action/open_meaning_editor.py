from os import path
from PyQt6.QtGui import QAction, QIcon


class OpenMeaningEditorAction(QAction):
    def __init__(self, parent, table_view) -> None:
        super().__init__(parent)
        self.table_view = table_view
        self.setText("Open Meaning Editor")
        
        addon_base_dir = path.realpath(__file__)
        for i in range(7):
            addon_base_dir = path.dirname(addon_base_dir)

        icon_file_path = path.join(addon_base_dir, "data", "icons", "editor.png")
        self.setIcon(QIcon(icon_file_path))

        self.triggered.connect(self._action)

    def _action(self):
        self.table_view._double_clicked()
