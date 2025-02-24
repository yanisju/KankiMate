from PyQt6.QtWidgets import QTableView, QHeaderView

from ....dialog.card import CardDialog

from .menu import SentenceTableViewMenu

from .....constants import SentenceWidgetMode, CardDialogMode


class SentenceTableView(QTableView):
    """Table view for the different sentences of one vocabulary."""

    def __init__(self, central_widget, vocabulary_manager, card_text_view, card_dialog: CardDialog, sentence_widget_mode: SentenceWidgetMode):
        super().__init__(central_widget)

        self.setEditTriggers(self.EditTrigger.NoEditTriggers)  # Disable editing
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents)
        self.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents)

        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectItems)
        self.setSelectionMode(QTableView.SelectionMode.SingleSelection)

        self.sentence_widget_mode = sentence_widget_mode

        self.menu = SentenceTableViewMenu(
            self,
            vocabulary_manager,
            card_text_view,
            sentence_widget_mode)
        self.card_text_view = card_text_view
        self.card_dialog = card_dialog

        self.clicked.connect(self.clicked_action)
        self.doubleClicked.connect(self.double_clicked_action)

    def _configure_header_section(self):
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Fixed)
        
        width = self.horizontalHeader().width()
        self.setColumnWidth(0, int(width * 0.4))
        self.setColumnWidth(1, int(width * 0.4))
        self.setColumnWidth(2, int(width * 0.1))
        self.setColumnWidth(3, int(width * 0.08))
        
        self.horizontalHeader().setStretchLastSection(True)

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

    def clicked_action(self):
        """When a sentence is clicked, update card view."""
        row = self.currentIndex().row()
        sentence_clicked = self.model().get_sentence_by_row(row)
        self.card_text_view.set_card_view(sentence_clicked)

        if self.sentence_widget_mode == SentenceWidgetMode.VOCABULARY_SENTENCE:
            card_dialog_mode = CardDialogMode.IS_VOCABULARY
        elif self.sentence_widget_mode == SentenceWidgetMode.ADDED_SENTENCE:
            card_dialog_mode = CardDialogMode.IS_ADDED

        self.card_dialog.sentence_changed(self.model(), sentence_clicked, row, card_dialog_mode)

    def double_clicked_action(self):
        """When a sentence is double-clicked, opens a new CardDialog to edit its fields."""
        if self.sentence_widget_mode == SentenceWidgetMode.VOCABULARY_SENTENCE:
            self.card_dialog.open(CardDialogMode.IS_VOCABULARY)
        elif self.sentence_widget_mode == SentenceWidgetMode.ADDED_SENTENCE:
            self.card_dialog.open(CardDialogMode.IS_ADDED)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._configure_header_section()