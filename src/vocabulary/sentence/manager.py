from . import Sentence
from ..model.sentence import SentenceModel

from .kanji_data import KanjiDataList


class SentenceManager(list):
    def __init__(self, vocabulary=None) -> None:
        super().__init__()
        self.vocabulary = vocabulary
        self.sentences_model = SentenceModel(self)

    def append(self, sentence: Sentence):
        super().append(sentence)
        self.sentences_model.append_sentence(sentence)

    def append_from_sentence_data(self,
            sentence_str: str,
            translation_str: str,
            kanjis_data):
        if not self.vocabulary:
            word = None
        else:
            word = self.vocabulary.word
        new_sentence = Sentence(
            self.vocabulary,
            sentence_str,
            translation_str,
            kanjis_data,
            word)
        super().append(new_sentence)
        self.sentences_model.append_sentence(new_sentence)

    def append_empty_sentence(self):
        if self.vocabulary is not None:
            word = self.vocabulary.word
        else:
            word = None
        empty_sentence = Sentence(self.vocabulary, "", "", KanjiDataList(), word)
        self.append(empty_sentence)

    def sort_by_sentence_length(self):
        self.sentences_model.remove_all_rows()
        self.sort(key=lambda sentence: len(sentence.sentence))
        for sentence in self:
            self.sentences_model.append_sentence(sentence)

    def pop(self, index):
        """
        Deletes a sentence from the sentences list based on its position.

        Args:
        -----
        index : int
            The index of the sentence to be deleted.
        """
        self.sentences_model.remove_row(index)
        return super().pop(index)
        

    def clear(self):
        super().clear()
        self.sentences_model.remove_all_rows()

    def update_meaning(self, new_vocabulary_meaning: str):
        """
        Update meaning of related vocabulary in kanjis list.
        """

        for sentence in self:
            sentence.kanji_data_list.update_kanji_meaning(self.vocabulary.word, new_vocabulary_meaning)