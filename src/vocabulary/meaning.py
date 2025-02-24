from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtCore import Qt

from ..constants import VocabularyPitchAccent


class VocabularyMeaning:
    """
    A class to represent the meanings and part-of-speech information for a vocabulary word.
    """

    def __init__(self, word: str, kana_reading: str, meanings: list, parts_of_speech: list, is_common: bool, jlpt_level: str, pitch_accent: VocabularyPitchAccent, pitch_pattern: list[bool], audio: str, current_selection: int = 1) -> None:
        """
        Initializes the VocabularyMeaning instance.
        """
        self.word = word
        self.kana_reading = kana_reading
        self.meanings = meanings  
        self.parts_of_speech = parts_of_speech 

        self.standard_item_model = QStandardItemModel(0, 2)
        self.standard_item_model.setHeaderData(0, Qt.Orientation.Horizontal, "Meaning")
        self.standard_item_model.setHeaderData(1, Qt.Orientation.Horizontal, "Part of Speech")

        for i in range(len(self.meanings)):
            self.standard_item_model.appendRow([QStandardItem(meanings[i]), QStandardItem(parts_of_speech[i])])

        self.is_common = is_common
        self.jlpt_level = jlpt_level

        self.pitch_accent = pitch_accent
        self.pitch_pattern = pitch_pattern

        self.audio = audio

        self.current_selection = current_selection
        

    def add(self, meaning: str, part_of_speech: str):
        """ Adds a new meaning and part of speech. """
        self.meanings.append(meaning)
        self.parts_of_speech.append(part_of_speech)
        self.standard_item_model.appendRow([QStandardItem(meaning), QStandardItem(part_of_speech)])

    def remove(self, index: int):
        """ Removes a meaning and its part of speech at the specified index. """
        del self.meanings[index]
        del self.parts_of_speech[index]
        self.standard_item_model.removeRow(index)

    def remove_all(self):
        """ Clears all meanings and parts of speech. """
        self.meanings.clear()
        self.parts_of_speech.clear()
        self.standard_item_model.clear()

    def __getitem__(self, index: int):
        """ Returns the meaning and part of speech as a tuple. """
        return self.meanings[index], self.parts_of_speech[index]

    def __setitem__(self, index: int, meaning_part_of_speech: tuple):
        """ Updates the meaning and part of speech at a given index. """
        meaning, part_of_speech = meaning_part_of_speech
        self.meanings[index] = meaning
        self.parts_of_speech[index] = part_of_speech
        self.standard_item_model.setItem(index, 0, QStandardItem(meaning))
        self.standard_item_model.setItem(index, 1, QStandardItem(part_of_speech))

    @property
    def selected_meaning(self) -> str:
        """Returns the currently selected meaning."""
        if self.meanings:
            return self.meanings[self.current_selection - 1]
        else:
            return ""
    
    @property
    def selected_part_of_speech(self) -> str:
        """Returns the part of speech for the currently selected meaning."""
        if self.parts_of_speech:
            return self.parts_of_speech[self.current_selection - 1]
        else:
            return ""

    def clone(self):
        return VocabularyMeaning(self.word,
                                 self.kana_reading,
                                 self.meanings,
                                 self.parts_of_speech,
                                 self.is_common,
                                 self.jlpt_level,
                                 self.pitch_accent,
                                 self.pitch_pattern,
                                 self.audio,
                                 self.current_selection)
