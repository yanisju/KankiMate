from os import path
from PyQt6.QtGui import QAction, QIcon


class OpenMeaningEditorAction(QAction):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setText("Open Card Editor")

        addon_base_dir = path.realpath(__file__)
        for i in range(7):
            addon_base_dir = path.dirname(addon_base_dir)

        icon_file_path = path.join(addon_base_dir, "data", "icons", "editor.png")
        self.setIcon(QIcon(icon_file_path))
        self.triggered.connect(self._action)

    def _action(self):
        self.parent().parent().double_clicked_action()
