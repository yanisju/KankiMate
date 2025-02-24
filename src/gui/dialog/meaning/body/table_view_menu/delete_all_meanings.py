from os import path

from PyQt6.QtGui import QAction, QIcon

class DeleteAllMeanings(QAction):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setText("Delete All Meanings")

        addon_base_dir = path.realpath(__file__)
        for i in range(7):
            addon_base_dir = path.dirname(addon_base_dir)

        icon_file_path = path.join(addon_base_dir, "data", "icons", "trashbin.png")
        self.setIcon(QIcon(icon_file_path))
        
        self.triggered.connect(self._action)

    def _action(self):
        model = self.parent().parent().model()
        for i in range(model.rowCount()):
            model.takeRow(0)

        selection_spinbox = self.parent().parent().parent().parent().bottom.meaning_attributes.selection_spin_box
        selection_spinbox.setMinimum(0)
        selection_spinbox.setMaximum(0)
