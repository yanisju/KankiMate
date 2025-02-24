from PyQt6.QtWidgets import QMenu

from .set_current_selection_action import SetCurrentSelectionAction
from .add_empty_meaning import AddEmptyMeaning
from .delete_meaning import DeleteMeaning
from .delete_all_meanings import DeleteAllMeanings

class MeaningTableViewMenu(QMenu):
    """Menu displayed when user right-clicks on sentence table view. """

    def __init__(self, parent):
        super().__init__(parent)
        self.rows_columns = []
        self._set_actions()

    def _set_actions(self):
        """Set actions data and behaviors."""
        self.set_current_selection_action = SetCurrentSelectionAction(self)
        self.addAction(self.set_current_selection_action)

        self.add_empty_meaning = AddEmptyMeaning(self)
        self.addAction(self.add_empty_meaning)

        self.delete_meaning_action = DeleteMeaning(self)
        self.addAction(self.delete_meaning_action)

        self.delete_all_meanings_action = DeleteAllMeanings(self)
        self.addAction(self.delete_all_meanings_action)

    def set_current_position(self, rows_columns: list):
        self.rows_columns = rows_columns

        if (len(rows_columns) == 0):
            self.set_current_selection_action.setEnabled(False)
            self.delete_meaning_action.setEnabled(False)
            self.delete_all_meanings_action.setEnabled(False)
        else:
            self.set_current_selection_action.setEnabled(True)
            self.delete_meaning_action.setEnabled(True)
            self.delete_all_meanings_action.setEnabled(True)