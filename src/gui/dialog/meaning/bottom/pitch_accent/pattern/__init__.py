from PyQt6.QtWidgets import QWidget, QLabel, QGraphicsView, QFormLayout
from PyQt6.QtCore import Qt

from .scene import PitchPatternScene

class PitchPatternWidget(QWidget):
    """
    A widget that displays a pitch pattern for a word, using a graphical view.

    Attributes:
        pitch_pattern_scene (PitchPatternScene): The scene that handles the pitch pattern.
        pitch_pattern_view (QGraphicsView): The view used to display the pitch pattern scene.
    """
    
    def __init__(self, parent):
        """
        Initializes the PitchPatternWidget with the necessary layout and view setup.

        Args:
            parent (QWidget): The parent widget to which this widget belongs.
        """
        super().__init__(parent)

        layout = QFormLayout(self)

        label = QLabel("Pitch Pattern: ")
        label.setProperty("class", "attributes")

        self.pitch_pattern_scene = PitchPatternScene(self)
        self.pitch_pattern_view = QGraphicsView(self.pitch_pattern_scene)

        self.pitch_pattern_view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        layout.addRow(label, self.pitch_pattern_view)

    def update_content(self, kana_reading: str, pitch_pattern: list[bool]):
        """
        Updates the pitch pattern display with a new word and its pitch pattern.

        Args:
            word (str): The word whose pitch pattern is to be displayed.
            pitch_pattern (list[bool]): The pitch pattern to be visualized.
        """
        self.pitch_pattern_scene.set_word(kana_reading, pitch_pattern)
