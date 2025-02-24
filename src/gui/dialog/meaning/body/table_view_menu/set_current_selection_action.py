from os import path

from PyQt6.QtGui import QAction, QIcon

class SetCurrentSelectionAction(QAction):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setText("Set as Current Selection")

        addon_base_dir = path.realpath(__file__)
        for i in range(7):
            addon_base_dir = path.dirname(addon_base_dir)

        icon_file_path = path.join(addon_base_dir, "data", "icons", "gear.png")
        self.setIcon(QIcon(icon_file_path))
        
        self.triggered.connect(self._action)

    def _action(self):
        row, _ = self.parent().rows_columns[0]
        dialog = self.parent().parent().parent().parent()
        dialog.bottom.meaning_attributes.selection_spin_box.setValue(row + 1)