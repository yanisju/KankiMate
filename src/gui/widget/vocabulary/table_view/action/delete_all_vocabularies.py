from os import path
from PyQt6.QtGui import QAction, QIcon


class DeleteAllVocabulariesAction(QAction):
    def __init__(
            self,
            parent,
            vocabulary_manager,
            sentence_rendering_widget,
            sentence_table_view) -> None:
        super().__init__(parent)
        self.vocabulary_manager = vocabulary_manager
        self.sentence_rendering_widget = sentence_rendering_widget
        self.sentence_table_view = sentence_table_view
        self.setText("Delete all Vocabularies")

        addon_base_dir = path.realpath(__file__)
        for i in range(7):
            addon_base_dir = path.dirname(addon_base_dir)

        icon_file_path = path.join(addon_base_dir, "data", "icons", "trashbin.png")
        self.setIcon(QIcon(icon_file_path))

        self.triggered.connect(self._action)

    def _action(self):
        self.vocabulary_manager.delete_all_vocabularies()
        self.sentence_rendering_widget.card_text_view.clear()
        self.sentence_table_view.setModel(None)
