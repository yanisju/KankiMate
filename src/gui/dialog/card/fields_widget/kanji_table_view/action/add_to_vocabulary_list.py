from os import path

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMessageBox


class AddToVocabularyListAction(QAction):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setText("Add to Vocabulary List")
        
        addon_base_dir = path.realpath(__file__)
        for i in range(8):
            addon_base_dir = path.dirname(addon_base_dir)

        icon_file_path = path.join(addon_base_dir, "data", "icons", "plus.png")
        self.setIcon(QIcon(icon_file_path))

        self.triggered.connect(self._action)

    def _action(self):
        wrong_words = 0
        for row, _ in self.parent().rows_columns:
            word = self.parent().parent().model().item(row, 0).text()
            if word == "":
                wrong_words += 1
            else:
                try:
                    self.parent().parent().parent().parent().vocabulary_manager.add_word(word)
                except BaseException:
                    wrong_words += 1

        if wrong_words != 0:
            QMessageBox.critical(
                self.parent().parent(),
                "Error",
                f"{wrong_words} words can't be imported.")
