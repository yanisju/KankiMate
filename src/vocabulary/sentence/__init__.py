from PyQt6.QtGui import QStandardItem
from ..str_utils import get_position_kanji_sentence
from .kanji_data import KanjiDataList

class Sentence:
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
    kanji_data_list : KanjiDataList
        An instance of KanjiDataList containing kanji-related information.
    position_kanji : dict
        A dictionary mapping the positions of kanji in the sentence to the corresponding kanji characters.
    standard_item : list[QStandardItem] or None
        A list of QStandardItems representing the sentence data for insertion into a model, or None if not yet computed.
    """

    def __init__(self, vocabulary, sentence: str, translation: str, kanji_data_list: KanjiDataList, 
                 word: str, word2: str = None, has_audio: bool = None):
        """
        Initializes a Sentence instance.

        Parameters:
        -----------
        vocabulary : Vocabulary
            The vocabulary instance associated with this sentence.
        sentence : str
            The sentence to be stored.
        translation : str
            The English translation of the sentence.
        kanji_data_list : KanjiDataList
            The list containing kanji information for this sentence.
        word : str
            The main vocabulary word in the sentence.
        word2 : str, optional
            An additional vocabulary word in the sentence (default is None).
        has_audio : bool, optional
            Indicates if the sentence has an associated audio file (default is None).
        """
        self.vocabulary = vocabulary
        self.word = word
        self.sentence = sentence
        self.translation = translation
        self.kanji_data_list = kanji_data_list
        self.kanji_data_list.bound_to_sentence(self)
        
        self.position_kanji = {}  # Dictionary storing kanji positions in the sentence.
        self._update_position_kanji()

        self.word1_data = kanji_data_list.get_kanji(word)
        self.word2_data = kanji_data_list.get_kanji(word2)

        self.has_audio = has_audio

        self.attributes = (sentence, translation, self.word1_data, self.word2_data)

        self.standard_item = None  # Stores QStandardItem elements for model insertion.
        self.compute_standard_item()

    def compute_standard_item(self):
        """
        Computes and updates the standard item list for insertion into a sentence model.

        The list contains QStandardItem elements representing:
        - The sentence
        - The translation
        - The primary word's kanji (if available)
        - The secondary word's kanji (if available)
        """
        word1_kanji, word2_kanji = None, None
        if self.word1_data is not None:
            word1_kanji = self.word1_data.word
        if self.word2_data is not None:
            word2_kanji = self.word2_data.word
        self.standard_item = [
            QStandardItem(self.sentence),
            QStandardItem(self.translation),
            QStandardItem(word1_kanji),
            QStandardItem(word2_kanji)
        ]

    def update_attributes(self, attributes: tuple):
        """
        Updates the sentence attributes.

        Parameters:
        -----------
        attributes : tuple
            A tuple containing the updated sentence, translation, word1_data, and word2_data.
        """
        self.sentence, self.translation, self.word1_data, self.word2_data = attributes
        self.attributes = attributes

        self.position_kanji = get_position_kanji_sentence(self.sentence, self.kanji_data_list)

    def _update_position_kanji(self):
        """Updates the position_kanji dictionary based on the current sentence."""
        self.position_kanji = get_position_kanji_sentence(self.sentence, self.kanji_data_list)

    def clone(self):
        """
        Creates and returns a new Sentence instance with the same attributes.

        Returns:
        --------
        Sentence
            A new Sentence instance that is a deep copy of the current one.
        """
        vocabulary, sentence, translation, kanji_data_list, word1_data, word2_data = (
            self.vocabulary, self.sentence, self.translation, self.kanji_data_list, self.word1_data, self.word2_data
        )
        word1 = word1_data[0] if word1_data else None
        word2 = word2_data[0] if word2_data else None

        new_kanji_data = kanji_data_list.clone()
        return Sentence(vocabulary, sentence, translation, new_kanji_data, word1, word2)

    def get_sentence_furigana(self) -> str:
        """
        Returns the sentence with furigana annotations for kanji.

        Returns:
        --------
        str
            The sentence with furigana annotations in the format "kanji[reading]".
        """
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

    def get_sentence_bold(self) -> str:
        """
        Returns the sentence with the primary word in bold.

        Returns:
        --------
        str
            The sentence with the primary word enclosed in <b> tags.
        """
        word1 = self.word1_data.word
        word1_index = self.sentence.find(word1)
        
        if word1_index == -1:
            return self.sentence
        
        return (self.sentence[:word1_index] + 
                '<b>' + self.sentence[word1_index: word1_index + len(word1)] + '</b>' + 
                self.sentence[word1_index + len(word1):])

    def get_sentence_furigana_bold(self) -> str:
        """
        Returns the sentence with furigana and the primary word in bold.

        Returns:
        --------
        str
            The sentence with furigana annotations, where the primary word is enclosed in <b> tags.
        """
        sentence = self.get_sentence_furigana()
        word1 = self.word1_data.word
        word1_reading = self.word1_data.reading
        word1_index = sentence.find(word1)

        if word1_index == -1:
            return sentence

        word1_furigana_length = word1_index + len(word1) + len(word1_reading) + 2
        return (sentence[:word1_index] + 
                '<b>' + sentence[word1_index: word1_furigana_length] + '</b>' + 
                sentence[word1_furigana_length:])
