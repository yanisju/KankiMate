from PyQt6.QtWidgets import QWidget, QTableView, QHeaderView

from .table_view_menu import MeaningTableViewMenu


class MeaningTableView(QTableView):
    """
    A custom QTableView for displaying word meanings.
    """

    def __init__(self, parent: QWidget) -> None:
        """
        Initializes the table view.

        Parameters:
        -----------
        parent : QWidget
            The parent widget of this table view.
        """
        super().__init__(parent)

        self.menu = MeaningTableViewMenu(self)
    
    def _configure_header_section(self):
        """
        Configures the horizontal header.
        """
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

        # Get the current width of the header
        width = self.horizontalHeader().width()
        
        # Set proportional column widths
        self.setColumnWidth(0, int(width * 0.8))
        self.setColumnWidth(1, int(width * 0.2))

        # Ensure the last column stretches if needed
        self.horizontalHeader().setStretchLastSection(True)
    
    def resizeEvent(self, event):
        """
        Handles resize events and updates the column widths dynamically.
        """
        super().resizeEvent(event)
        self._configure_header_section()  # Adjust column sizes when resized

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