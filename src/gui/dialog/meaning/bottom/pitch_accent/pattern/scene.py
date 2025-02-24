from .items import *

class PitchPatternScene(QGraphicsScene):
    """
    A scene that displays the pitch pattern of a word, visualizing syllables and their pitch accent.

    This class is used to represent the pitch pattern of a word, where each syllable is
    displayed along with its corresponding pitch accent (high or low). The transition
    lines indicate pitch changes between syllables. Users can click on syllables to toggle
    their pitch state (high ↔ low).
    """

    def __init__(self, parent):
        """
        Initializes the scene with the given parent and sets the appropriate scene rect size.

        Args:
            parent (QWidget): The parent widget to which this scene is attached.
        """
        super().__init__(parent)

        height = parent.parent().parent().parent().height() * 0.275 * 0.4
        self.setSceneRect(0, 0, parent.width(), height)

    def set_word(self, kana_reading: str, pitch_pattern: list[bool]):
        """
        Sets the word and its pitch pattern, and draws the corresponding pitch graph.

        Args:
            word (str): The word whose pitch pattern needs to be visualized.
            pitch_pattern (list[bool]): A list of booleans representing the pitch (True for high, False for low)
                                         for each syllable in the word.
        """
        self.y_low = self.sceneRect().height() * 0.7
        self.y_high = self.sceneRect().height() * 0.3

        self.syllables = list(kana_reading)
        self.pitch_pattern = pitch_pattern
        self.syllable_items: list[PitchSyllableItem] = []
        self.transition_lines: list[PitchTransitionLine] = []

        self._draw_pitch_graph()

    def _draw_pitch_graph(self):
        """
        Draws the pitch graph based on the current word and pitch pattern.

        Clears the scene and re-draws the syllables and pitch transition lines.
        """
        self.clear()
        self.syllable_items.clear()
        self.transition_lines.clear()

        # Calculer la largeur totale du mot pour le centrage
        total_width = sum(QGraphicsTextItem(syl).boundingRect().width() for syl in self.syllables)
        x_start = (self.sceneRect().width() * 0.525 - total_width) / 2  # Centrage horizontal

        for i, syllable in enumerate(self.syllables):
            syllable_item = PitchSyllableItem(self, syllable, x_start, self.height(), self.pitch_pattern[i], self.y_low, self.y_high)
            x_start += syllable_item.text_item.boundingRect().width()
            self.syllable_items.append(syllable_item)

        for i in range(len(self.syllables) - 1):
            transition_line = PitchTransitionLine(self.syllable_items[i].x_end, self.y_low, self.y_high)
            self.addItem(transition_line)
            self.transition_lines.append(transition_line)

        self.update_pitch_transitions()


    def mousePressEvent(self, event):
        """
        Handles mouse press events to toggle the pitch of the clicked syllable.

        If a syllable is clicked, its pitch is toggled (high ↔ low) and the pitch transition
        lines are updated accordingly.

        Args:
            event (QGraphicsSceneMouseEvent): The mouse press event.
        """
        mouse_x = event.scenePos().x()

        for i, syllable_item in enumerate(self.syllable_items):
            if syllable_item.x_start <= mouse_x < syllable_item.x_end:
                self.pitch_pattern[i] = not self.pitch_pattern[i]
                syllable_item.pitch_line.toggle_pitch()
                self.update_pitch_transitions()
                break

        super().mousePressEvent(event)

    def update_pitch_transitions(self):
        """
        Updates the visibility of pitch transition lines based on the current pitch pattern.

        Transition lines are visible only when the pitch changes between consecutive syllables.
        """
        for i in range(len(self.syllables) - 1):
            self.transition_lines[i].setVisible(self.pitch_pattern[i] != self.pitch_pattern[i + 1])
