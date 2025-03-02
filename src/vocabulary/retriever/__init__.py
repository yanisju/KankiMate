from .kanji_data import *
# from .meaning.retriever import *
from .sentence.http import SentenceHTTPRetriever
from .sentence.local import SentenceLocalRetriever

from ...constants import RetrieverMode

class DataRetriever():
    """
    A class used to retrieve vocabulary data, including example sentences, translations, meanings, and kanji details.

    The `DataRetriever` class is responsible for fetching and organizing various data associated with a given word.
    This includes example sentences, their translations, word meanings, and detailed kanji information such as readings,
    meanings, and positions within sentences.

    Attributes:
    -----------
    lang_from : str
        The source language code for retrieving data (e.g., 'jpn' for Japanese).
    lang_to : str
        The target language code for retrieving data (e.g., 'eng' for English).

    Methods:
    --------
    get_data(word, word_meaning):
        Retrieves data for the specified word, including example sentences, translations,
        kanji readings, meanings, and positions within sentences.
    """

    def __init__(self, lang_from, lang_to, mode: RetrieverMode):
        self.lang_from = lang_from
        self.lang_to = lang_to
        self.mode = mode
        self.sentence_http_retriever = SentenceHTTPRetriever(self.lang_from, self.lang_to)
        self.sentence_local_retriever = SentenceLocalRetriever()

    def get_data(self, word, word_meaning):
        if self.mode == RetrieverMode.HTTP:
            data = self.sentence_http_retriever.get_sentences(word)
        elif self.mode == RetrieverMode.LOCAL:
            data = self.sentence_local_retriever.get_sentences(word)

        meaning = word_meaning.selected_meaning
        part_of_speech = word_meaning.selected_part_of_speech
        for sentence_data in data:
            transcription = sentence_data[2]
            if transcription:
                kanji_data = self._get_kanji_data(transcription, word, meaning)
                sentence_data.append(kanji_data)
        return data

    def _get_kanji_data(self, transcription, word: str, word_meaning: str):
        kanji_data = get_kanji_reading_meaning_position(transcription)

        if not is_word_in_list(
                kanji_data,
                word):  # Check if the word appears in the kanji data:
            if check_word_contains_kana(word):  # If the word contains kana, update the kanji data accordingly
                kanji_data.update_data_kanji_kana(word)
            # else:
            #     kanji_data.update_data_only_kanji(word)

        if is_word_in_list(
                kanji_data,
                word):  # Check again if the word appears in the updated kanji data
            # Update the word's reading, meaning, and position
            kanji_data.update_kanji_meaning(word, word_meaning)

        return kanji_data
