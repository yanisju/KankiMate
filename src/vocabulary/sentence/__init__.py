from PyQt6.QtGui import QStandardItem

from ..str_utils import get_position_kanji_sentence
from .kanji_data import KanjiDataList


class Sentence():
    """
    Represents a single sentence in the context of vocabulary learning.

    Attributes:
    -----------
    vocabulary : Vocabulary
        The vocabulary class associated with this sentence.
    word : str
        The primary word in the sentence that is the focus of the vocabulary learning.
    sentence : str
        The sentence itself.
    translation : str
        The English translation of the sentence.
    word1_data : tuple
        A tuple containing the first word's kanji, reading, meaning, and position in the sentence.
    word2_data : tuple or None
        A tuple containing the second word's kanji, reading, meaning, and position in the sentence, or None if there is no second word.
    attributes : tuple
        A tuple containing the sentence, translation, word1_data, and word2_data.
    kanji_data_list : dict
        A dictionary containing kanji as keys and their readings, meanings, and positions as values.
    position_kanji_sentence : dict
        A dictionary containing the positions of kanji in the sentence as keys and the corresponding kanji as values.
    standard_item : list or None
        A list of QStandardItems representing the sentence data for insertion into a model, or None if not yet computed.
    """

    def __init__(self, vocabulary, sentence: str, translation: str, kanji_data_list: KanjiDataList, word: str, word2: str = None, has_audio: bool = None):
        self.vocabulary = vocabulary
        self.word = word
        self.sentence = sentence
        self.translation = translation
        self.kanji_data_list = kanji_data_list
        self.kanji_data_list.bound_to_sentence(self)
        
        self.position_kanji = {} # Dict containg positions in text as keys and kanjis as values.
        self._update_position_kanji()

        self.word1_data = kanji_data_list.get_kanji(word)
        self.word2_data = kanji_data_list.get_kanji(word2)

        self.has_audio = has_audio

        self.attributes = (sentence,
            translation,
            self.word1_data,
            self.word2_data)

        self.standard_item = None  # QStandardItem in order to be inserted in the model
        self.compute_standard_item()

    def compute_standard_item(self): # TODO: class does not contain standard item, but method return it directly
        """Update standard item to insert in Sentence model, based on current sentences attributes. """
        word1_kanji, word2_kanji = None, None
        if self.word1_data is not None:
            word1_kanji = self.word1_data.word
        if self.word2_data is not None:
            word2_kanji = self.word2_data.word
        self.standard_item = [
            QStandardItem(
                self.sentence),
            QStandardItem(
                self.translation),
            QStandardItem(word1_kanji),
            QStandardItem(word2_kanji)]

    def update_attributes(self, attributes: list):
        """
        Updates the sentence attributes.

        Args:
        -----
        attributes : tuple
            A tuple containing the sentence, translation, word1_data, and word2_data.
        """

        self.sentence, self.translation, self.word1_data, self.word2_data = attributes
        self.attributes = attributes

        self.position_kanji = get_position_kanji_sentence(
            self.sentence, self.kanji_data_list)

    def _update_position_kanji(self):
        self.position_kanji = get_position_kanji_sentence(
            self.sentence, self.kanji_data_list)

    def clone(self):
        """
        Creates and returns a new Sentence instance with the same attributes.

        Returns:
        --------
        Sentence
            A new Sentence instance with the same attributes as the original.
        """
        vocabulary, sentence, translation, kanji_data_list, word1_data, word2_data = self.vocabulary, self.sentence, self.translation, self.kanji_data_list, self.word1_data, self.word2_data
        if word1_data:
            word1, *_ = word1_data
        else:
            word1 = None
        if word2_data:
            word2, *_ = word2_data
        else:
            word2 = None
        new_kanji_data = kanji_data_list.clone()
        new_sentence = Sentence(
            vocabulary,
            sentence,
            translation,
            new_kanji_data,
            word1,
            word2)
        return new_sentence

    def get_sentence_furigana(self) -> str:
        sentence_furigana = ""
        i = 0

        while i < len(self.sentence):
            matched = False

            for kanji_data in self.kanji_data_list:
                if self.sentence[i:i+len(kanji_data.word)] == kanji_data.word:
                    sentence_furigana += f" {kanji_data.word}[{kanji_data.reading}]"
                    i += len(kanji_data.word)
                    matched = True
                    break  

            if not matched:
                sentence_furigana += self.sentence[i]
                i += 1

        return sentence_furigana.strip() 
