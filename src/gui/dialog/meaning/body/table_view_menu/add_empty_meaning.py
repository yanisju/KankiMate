from os import path

from PyQt6.QtGui import QAction, QIcon

from PyQt6.QtGui import QStandardItem

class AddEmptyMeaning(QAction):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setText("Add Empty Vocabulary")

        addon_base_dir = path.realpath(__file__)
        for i in range(7):
            addon_base_dir = path.dirname(addon_base_dir)

        icon_file_path = path.join(addon_base_dir, "data", "icons", "plus.png")
        self.setIcon(QIcon(icon_file_path))
        
        self.triggered.connect(self._action)

    def _action(self):
        model = self.parent().parent().model()
        model.appendRow([QStandardItem(""), QStandardItem("")])

        selection_spinbox = self.parent().parent().parent().parent().bottom.meaning_attributes.selection_spin_box
        selection_spinbox.setMaximum(selection_spinbox.maximum() + 1)
        if selection_spinbox.value() == 0:
            selection_spinbox.setValue(1)
