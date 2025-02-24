from os import path

from PyQt6.QtGui import QAction, QIcon

class DeleteMeaning(QAction):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setText("Delete Meaning")

        addon_base_dir = path.realpath(__file__)
        for i in range(7):
            addon_base_dir = path.dirname(addon_base_dir)

        icon_file_path = path.join(addon_base_dir, "data", "icons", "minus.png")
        self.setIcon(QIcon(icon_file_path))
        
        self.triggered.connect(self._action)

    def _action(self):
        rows_columns= self.parent().rows_columns

        model = self.parent().parent().model()
        selection_spinbox = self.parent().parent().parent().parent().bottom.meaning_attributes.selection_spin_box
        for row_index, _ in rows_columns:
            model.takeRow(row_index)
            selection_spinbox.setMaximum(selection_spinbox.maximum() - 1)

        
        