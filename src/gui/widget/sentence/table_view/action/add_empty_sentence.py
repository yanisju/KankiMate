from os import path
from PyQt6.QtGui import QAction, QIcon


class AddEmptySentenceAction(QAction):
    def __init__(self, parent, vocabulary_manager):
        super().__init__(parent)
        self.vocabulary_manager = vocabulary_manager
        self.setText("Add Empty Sentence")

        addon_base_dir = path.realpath(__file__)
        for i in range(7):
            addon_base_dir = path.dirname(addon_base_dir)

        icon_file_path = path.join(addon_base_dir, "data", "icons", "plus.png")
        self.setIcon(QIcon(icon_file_path))

        self.triggered.connect(self._action)

    def _action(self):
        sentence_manager = self.parent().parent().model().sentence_manager
        sentence_manager.append_empty_sentence()
