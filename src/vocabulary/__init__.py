from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtCore import QObject, pyqtSignal

from .sentence.manager import SentenceManager

from .retriever.meaning import MeaningRetriever

from ..constants import VocabularyPitchAccent, VocabularyJLPTLevel


class Vocabulary(QObject):
    """
    Represents a single vocabulary word and its associated example sentences.

    Attributes:
    -----------
    word : str
        The vocabulary word itself.
    sentence_retriever : DataRetriever
        An instance responsible for retrieving sentences and related data for the vocabulary word.
    quick_init : boolean
        TODO: complete
    """

    standard_item_modified = pyqtSignal(str, list)

    def __init__(self, word: str, sentence_retriever, meaning_retriever: MeaningRetriever):
        super().__init__()
        self.word = word
        
        self.sentence_retriever = sentence_retriever

        self.meaning_retriever = meaning_retriever
        self.meaning = meaning_retriever.retrieve(word)

        self.sentence_manager = SentenceManager(self)
        self.sentence_manager.sentences_model.modified.connect(
            self.set_standard_item)

        self._get_data()

        self.standard_item = [QStandardItem(self.word),
                              QStandardItem(self.meaning.selected_meaning),
                              QStandardItem(self.meaning.selected_part_of_speech),
                              QStandardItem(str(len(self.sentence_manager)))]

    def _get_data(self):
        """
        Retrieves data associated with the vocabulary word.

        This method uses the sentence_retriever to obtain sentences, their translations,
        kanji data, the meaning of the word, and parts of speech. It then populates
        the sentences attribute with Sentence objects."""

        sentences_data = self.sentence_retriever.get_data(
            self.word, self.meaning)  # Retrieve sentences from DataRetriever

        for one_sentence_data in sentences_data:
            sentence, translation, transcription, kanji_data = one_sentence_data
            self.sentence_manager.append_from_sentence_data(
                sentence, translation, kanji_data)
        self.sentence_manager.sort_by_sentence_length()

    def update_meaning(self, meaning_model: QStandardItemModel, selection: int, is_common: bool, jlpt_level: VocabularyJLPTLevel, pitch_accent: VocabularyPitchAccent, pitch_pattern: list[bool]):
        """ Updates vocabulary meaning and refresh interface. """

        meanings, parts_of_speech = [], []
        for i in range(meaning_model.rowCount()):
            meaning, part_of_speech = meaning_model.takeRow(0)
            meanings.append(meaning)
            parts_of_speech.append(part_of_speech)

        self.meaning.meanings = meanings
        self.meaning.parts_of_speech = parts_of_speech

        self.meaning.standard_item_model = meaning_model

        self.meaning.current_selection = selection
        self.meaning.is_common = is_common
        self.meaning.jlpt_level = jlpt_level
        self.meaning.pitch_accent = pitch_accent
        self.meaning.pitch_pattern = pitch_pattern
        self.set_standard_item()

    def remove_sentence(self, row):
        """
        Deletes a sentence from the sentences list based on its position.

        Args:
        -----
        row : int
            The index of the sentence to be deleted.
        """
        self.sentence_manager.pop(row)

    def remove_all_sentence(self):
        self.sentence_manager.clear()

    def set_standard_item(self):
        self.standard_item = [QStandardItem(self.word),
                              QStandardItem(self.meaning.selected_meaning),
                              QStandardItem(self.meaning.selected_part_of_speech),
                              QStandardItem(str(len(self.sentence_manager)))]
        self.standard_item_modified.emit(self.word, self.standard_item)
