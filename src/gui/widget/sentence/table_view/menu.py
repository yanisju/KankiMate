from PyQt6.QtWidgets import QMenu
from .action.open_card_editor import OpenMeaningEditorAction
from .action.add_sentence_to_deck import AddSentenceToDeckAction
from .action.delete_one_sentence import DeleteOneSentenceAction
from .action.delete_all_sentences import DeleteAllSentenceAction
from .action.add_empty_sentence import AddEmptySentenceAction

from .....constants import SentenceWidgetMode


class SentenceTableViewMenu(QMenu):
    """Menu displayed when user right-clicks on sentence table view. """

    def __init__(
            self,
            parent,
            vocabulary_manager,
            card_text_view,
            sentence_widget_mode):
        super().__init__(parent)
        self.row = -1
        self.column = -1
        self.sentence_widget_mode = sentence_widget_mode
        self._actions = []
        self._set_actions(vocabulary_manager, card_text_view)

    def _set_actions(self, vocabulary_manager, card_text_view):
        """Set actions data and behaviors."""

        self.open_card_editor_action = OpenMeaningEditorAction(self)
        self._actions.append(self.open_card_editor_action)
        self.addAction(self.open_card_editor_action)

        if self.sentence_widget_mode == SentenceWidgetMode.VOCABULARY_SENTENCE:
            self.add_sentence_to_deck_action = AddSentenceToDeckAction(
                self, vocabulary_manager)
            self._actions.append(self.add_sentence_to_deck_action)
            self.addAction(self.add_sentence_to_deck_action)

        self.addSeparator()

        self.add_empty_sentence_action = AddEmptySentenceAction(
            self, vocabulary_manager)
        self._actions.append(self.add_empty_sentence_action)
        self.addAction(self.add_empty_sentence_action)

        self.addSeparator()

        self.del_one_sentence_action = DeleteOneSentenceAction(
            self, card_text_view)
        self._actions.append(self.del_one_sentence_action)
        self.addAction(self.del_one_sentence_action)

        self.del_all_sentence_action = DeleteAllSentenceAction(
            self, card_text_view)
        self._actions.append(self.del_all_sentence_action)
        self.addAction(self.del_all_sentence_action)

    def set_current_position(self, row: int, column: int):
        self.row = row
        self.column = column

        if self.parent().model() is None:
            for action in self._actions:
                action.setEnabled(False)
        else:
            self.add_empty_sentence_action.setEnabled(True)
            if self.parent().model().rowCount() == 0:
                self.del_all_sentence_action.setEnabled(False)
                self.open_card_editor_action.setEnabled(False)
                if self.sentence_widget_mode == SentenceWidgetMode.VOCABULARY_SENTENCE:
                    self.add_sentence_to_deck_action.setEnabled(False)
            else:
                self.del_all_sentence_action.setEnabled(True)
                self.open_card_editor_action.setEnabled(True)
                if self.sentence_widget_mode == SentenceWidgetMode.VOCABULARY_SENTENCE:
                    self.add_sentence_to_deck_action.setEnabled(True)

        if (row == -1):
            self.del_one_sentence_action.setEnabled(False)
            self.open_card_editor_action.setEnabled(False)
            if self.sentence_widget_mode == SentenceWidgetMode.VOCABULARY_SENTENCE:
                self.add_sentence_to_deck_action.setEnabled(False)
        else:
            self.del_one_sentence_action.setEnabled(True)
            self.del_one_sentence_action.setEnabled(True)
            if self.sentence_widget_mode == SentenceWidgetMode.VOCABULARY_SENTENCE:
                self.add_sentence_to_deck_action.setEnabled(True)
