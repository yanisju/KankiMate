from os import path
from PyQt6.QtWidgets import QTableView, QHeaderView

from .menu import VocabularyTableViewMenu
from ....dialog.meaning import MeaningDialog


class VocabularyTableView(QTableView):
    """
    A custom QTableView for displaying and managing vocabulary items in a table format.

    This class is designed to allow users to view vocabulary words,
    display a context menu, edit word meanings through a dialog interface and interact with VocabularyManager.

    Attributes:
    -----------
    vocabulary_manager : VocabularyManager
        The manager responsible for handling the vocabulary data and model.
    menu : VocabularyTableViewMenu
        The context menu for interacting with table items.
    meaning_dialog : MeaningDialog
        A dialog for viewing and modifying vocabulary meanings.

    Methods:
    --------
    contextMenuEvent(event):
        Displays a context menu at the position of the mouse event.

    _double_clicked():
        Opens the `MeaningDialog` when a row in the table is double-clicked.

    _meaning_dialog_confirm_action(model: QStandardItemModel, current_selection: int):
        Updates the vocabulary item based on the confirmed selection from the `MeaningDialog`.
    """

    def __init__(
            self,
            parent,
            vocabulary_manager,
            sentence_rendering_widget,
            sentence_table_view) -> None:
        """
        Initializes the VocabularyTableView instance with the given vocabulary manager.

        Args:
        -----
        vocabulary_manager : VocabularyManager
            The manager responsible for providing the vocabulary data model and operations.
        """
        super().__init__(parent)
        
        self._configure_header_section()
        
        addon_base_dir = path.realpath(__file__)
        for i in range(6):
            addon_base_dir = path.dirname(addon_base_dir)

        css_file_path = path.join(addon_base_dir, "styles", "table_view.css")

        with open(css_file_path, "r") as css_file:
            self.setStyleSheet(css_file.read())

        self.vocabulary_manager = vocabulary_manager
        self.sentence_table_view = sentence_table_view
        self.setModel(vocabulary_manager.vocabulary_model)
        self.setEditTriggers(self.EditTrigger.NoEditTriggers)

        self.menu = VocabularyTableViewMenu(
            self,
            vocabulary_manager,
            sentence_rendering_widget,
            sentence_table_view)
        self.meaning_dialog = MeaningDialog(parent)
        self.meaning_dialog.confirm_button_clicked_signal.connect(
            self._meaning_dialog_confirm_action)
        self.doubleClicked.connect(self._double_clicked)

        # Change sentence view when a different word is selected
        view_item_selection = self.selectionModel()
        view_item_selection.selectionChanged.connect(
            self._selection_changed_action)

    def contextMenuEvent(self, event):
        """
        Opens the context menu at the position of the mouse event.

        Args:
        -----
        event : QContextMenuEvent
            The event object containing the position of the mouse click.
        """
        row = self.rowAt(event.pos().y())
        column = self.columnAt(event.pos().x())

        self.menu.set_current_position(row, column)
        self.menu.exec(event.globalPos())

    def _configure_header_section(self):
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Fixed)
        
        self.hideColumn(0)
        
        width = self.horizontalHeader().width()
        self.setColumnWidth(0, int(width * 0.10))
        self.setColumnWidth(1, int(width * 0.65))
        self.setColumnWidth(2, int(width * 0.15))
        self.setColumnWidth(3, int(width * 0.10))
        
        self.horizontalHeader().setStretchLastSection(True)

    def _double_clicked(self):
        """
        Handles the event when a table row is double-clicked.

        Opens the `MeaningDialog` to allow editing of the vocabulary item's meaning.
        """
        row = self.currentIndex().row()
        vocabulary = self.vocabulary_manager[row]
        self.meaning_dialog.open(vocabulary)

    def _meaning_dialog_confirm_action(self, model, current_selection: int):
        """
        Handles the confirmation of a new meaning selection from the `MeaningDialog`.

        Args:
        -----
        model : QStandardItemModel
            The data model containing the updated meanings.
        current_selection : int
            The index of the selected meaning from the dialog.

        Modifies the selected vocabulary item's meaning and updates the table view.
        """
        row = self.currentIndex().row()
        meaning_row = current_selection - 1

        meaning, part_of_speech = model.item(
            meaning_row, 0).text(), model.item(
            meaning_row, 1).text()
        self.vocabulary_manager[row].meaning_object[meaning_row] = (
            meaning, part_of_speech)
        self.vocabulary_manager[row].meaning_object.current_selection = current_selection
        self.vocabulary_manager[row].set_standard_item()

    def _selection_changed_action(self):
        selection_row = self.currentIndex().row()
        vocabulary_sentences_model = self.vocabulary_manager[
            selection_row].sentence_manager.sentences_model
        self.sentence_table_view.setModel(vocabulary_sentences_model)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._configure_header_section()