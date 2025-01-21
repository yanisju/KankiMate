from os import path
from PyQt6.QtGui import QAction, QIcon


class DeleteAllSentenceAction(QAction):
    def __init__(self, parent, card_text_view):
        super().__init__(parent)
        self.card_text_view = card_text_view
        self.setText("Delete all Sentences")

        addon_base_dir = path.realpath(__file__)
        for i in range(7):
            addon_base_dir = path.dirname(addon_base_dir)

        icon_file_path = path.join(addon_base_dir, "data", "icons", "trashbin.png")
        self.setIcon(QIcon(icon_file_path))

        self.triggered.connect(self._action)

    def _action(self):
        sentence_manager = self.parent().parent().model().sentence_manager

        if self.card_text_view.sentence in sentence_manager:
            self.card_text_view.clear()
        sentence_manager.clear()
