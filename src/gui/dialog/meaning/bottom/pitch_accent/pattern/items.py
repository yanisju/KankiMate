from PyQt6.QtWidgets import QGraphicsScene, QGraphicsTextItem, QGraphicsLineItem
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QFont


class PitchSyllableItem:
    """
    Represents a syllable with its pitch accent line, visualized in a graphics scene.

    This class combines a `SyllableTextItem` for displaying the syllable as text and
    a `PitchLineItem` for displaying its associated pitch accent. The syllable's
    pitch is represented by a high or low pitch line.
    """

    def __init__(self, scene: QGraphicsScene, syllable: str, x_start: float, parent_height: float, is_high_pitch: bool, y_low: float, y_high: float):
        """
        Initializes a PitchSyllableItem, adding the text and pitch line to the given scene.

        Args:
            scene (QGraphicsScene): The scene to which the graphical items will be added.
            syllable (str): The syllable to display.
            x_start (float): The starting x-coordinate for placing the syllable text.
            parent_height (float): The height of the parent container to position the text vertically.
            is_high_pitch (bool): A flag indicating whether the pitch is high (True) or low (False).
            y_low (float): The y-coordinate for the low pitch.
            y_high (float): The y-coordinate for the high pitch.
        """
        self.text_item = SyllableTextItem(syllable, x_start, parent_height)
        scene.addItem(self.text_item)

        x_end = x_start + self.text_item.boundingRect().width()
        self.pitch_line = PitchLineItem(x_start, x_end, y_low, y_high, is_high_pitch)
        scene.addItem(self.pitch_line)

    @property
    def x_start(self):
        """ Returns the starting x-coordinate of the syllable. """
        return self.text_item.x()

    @property
    def x_end(self):
        """ Returns the ending x-coordinate of the syllable. """
        return self.x_start + self.text_item.boundingRect().width()


class SyllableTextItem(QGraphicsTextItem):
    """
    Represents the text of a syllable as a graphical item.

    This class is used to display a syllable in a graphics scene, positioning it
    vertically within the available space.
    """

    def __init__(self, syllable: str, x_start: float, parent_height: int):
        """
        Initializes a graphical text item for the syllable.

        Args:
            syllable (str): The text of the syllable to display.
            x_start (float): The starting x-coordinate to position the text.
            parent_height (int): The height of the parent container to vertically center the text.
        """
        super().__init__(syllable)
        self.setFont(QFont("Arial", 20))

        y_pos = (parent_height - self.boundingRect().height()) / 2
        self.setPos(QPointF(x_start, y_pos))


class PitchLineItem(QGraphicsLineItem):
    """
    Represents a pitch line (high or low) associated with a syllable.

    The pitch line is visualized as a horizontal line at either a high or low y-coordinate,
    indicating the pitch of the syllable.
    """

    def __init__(self, x_start: float, x_end: float, y_low: float, y_high: float, is_high_pitch: bool):
        """
        Initializes a pitch line for the syllable.

        Args:
            x_start (float): The starting x-coordinate of the line.
            x_end (float): The ending x-coordinate of the line.
            y_low (float): The y-coordinate for the low pitch line.
            y_high (float): The y-coordinate for the high pitch line.
            is_high_pitch (bool): Flag indicating whether the pitch is high (True) or low (False).
        """
        self.is_high_pitch = is_high_pitch
        self.y_low = y_low
        self.y_high = y_high

        y_pos = y_high if is_high_pitch else y_low
        super().__init__(x_start, y_pos, x_end, y_pos)

    def toggle_pitch(self):
        """
        Toggles the pitch state between high and low.

        This method changes the pitch from high to low or vice versa, and updates the
        position of the pitch line accordingly.
        """
        self.is_high_pitch = not self.is_high_pitch
        y_pos = self.y_high if self.is_high_pitch else self.y_low
        self.setLine(self.line().x1(), y_pos, self.line().x2(), y_pos)


class PitchTransitionLine(QGraphicsLineItem):
    """
    Represents a vertical line marking a pitch transition between two syllables.

    This class is used to visualize the transition point where the pitch changes
    between two syllables.
    """

    def __init__(self, x: float, y_low: float, y_high: float):
        """
        Initializes a vertical transition line between pitch levels.

        Args:
            x (float): The x-coordinate for the transition line.
            y_low (float): The y-coordinate for the lower pitch level.
            y_high (float): The y-coordinate for the higher pitch level.
        """
        super().__init__(x, y_low, x, y_high)
