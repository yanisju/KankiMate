from os import path
from PyQt6.QtWidgets import QTableView, QHeaderView

from .menu import KanjiTableViewMenu

class KanjiTableView(QTableView):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents)
        
        addon_base_dir = path.realpath(__file__)
        for i in range(7):
            addon_base_dir = path.dirname(addon_base_dir)

        css_file_path = path.join(addon_base_dir, "styles", "table_view.css")
        with open(css_file_path, "r") as css_file: 
            self.setStyleSheet(css_file.read())
        self.menu = KanjiTableViewMenu(self)

    def _configure_header_section(self):
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Fixed)
        
        width = self.horizontalHeader().width()
        self.setColumnWidth(0, int(width * 0.15))
        self.setColumnWidth(1, int(width * 0.15))
        self.setColumnWidth(2, int(width * 0.7))
        
        self.horizontalHeader().setStretchLastSection(True)

    def set_to_new_sentence(self, sentence):
        self.kanji_data = sentence.kanji_data_list
        self.setModel(sentence.kanji_data_list.model)
        self.resizeEvent(None)

    def contextMenuEvent(self, event):
        """
        Opens the context menu at the position of the mouse event.

        Args:
        -----
        event : QContextMenuEvent
            The event object containing the position of the mouse click.
        """

        rows_columns = self._get_selected_rows_columns()
        self.menu.set_current_position(rows_columns)
        self.menu.exec(event.globalPos())

    def _get_selected_rows_columns(self):
        model_indexes = self.selectionModel().selectedIndexes()
        row_column_pairs = [(index.row(), index.column())
                            for index in model_indexes]
        row_column_pairs.sort(key=lambda pair: pair[0])
        return row_column_pairs
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._configure_header_section()
