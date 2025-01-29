from PyQt6.QtWidgets import QMenu

from .action.del_one_vocabulary import DeleteVocabularyAction
from .action.delete_all_vocabularies import DeleteAllVocabulariesAction
from .action.open_meaning_editor import OpenMeaningEditorAction
from .action.lookup_on_jisho import LookupOnJishoAction


class VocabularyTableViewMenu(QMenu):
    """Menu displayed when user right-clicks on vocabulary table view. """

    def __init__(
            self,
            parent,
            vocabulary_manager,
            sentence_rendering_widget,
            sentence_table_view):
        super().__init__(parent)
        self.vocabulary_manager = vocabulary_manager
        self.row = -1
        self.column = -1

        self.set_actions(
            vocabulary_manager,
            sentence_rendering_widget,
            sentence_table_view)

    def set_actions(
            self,
            vocabulary_manager,
            sentence_rendering_widget,
            sentence_table_view):
        self.open_meaning_editor_action = OpenMeaningEditorAction(
            self, self.parent())
        self.addAction(self.open_meaning_editor_action)

        self.addSeparator()

        self.lookup_on_jisho_action = LookupOnJishoAction(
            self, vocabulary_manager)
        self.addAction(self.lookup_on_jisho_action)

        self.addSeparator()

        self.del_one_vocabulary_action = DeleteVocabularyAction(
            self, vocabulary_manager, sentence_rendering_widget, sentence_table_view)
        self.addAction(self.del_one_vocabulary_action)

        self.del_every_vocabulary_action = DeleteAllVocabulariesAction(
            self, vocabulary_manager, sentence_rendering_widget, sentence_table_view)
        self.addAction(self.del_every_vocabulary_action)

    def set_current_position(self, row: int, column: int):
        self.row = row
        self.column = column

        if self.vocabulary_manager.vocabulary_model.rowCount() == 0:
            self.del_every_vocabulary_action.setEnabled(False)
        else:
            self.del_every_vocabulary_action.setEnabled(True)

        if (row == -1):
            self.del_one_vocabulary_action.setEnabled(False)
            self.open_meaning_editor_action.setEnabled(False)
            self.lookup_on_jisho_action.setEnabled(False)
        else:
            self.del_one_vocabulary_action.setEnabled(True)
            self.open_meaning_editor_action.setEnabled(True)
            self.lookup_on_jisho_action.setEnabled(True)
