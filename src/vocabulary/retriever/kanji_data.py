import re

from ..sentence.kanji_data import KanjiDataList


def check_char_is_kana(char):
    if ord(char) >= 12352 and ord(char) <= 12543:
        return True
    else:
        return False


def check_word_contains_kana(word: str):
    for char in word:
        if check_char_is_kana(char):
            return True
    return False


def is_word_in_list(kanji_data, word: str):
    is_in_list = False
    for i in range(len(kanji_data)):
        if word == kanji_data[i].word:
            is_in_list = True
    return is_in_list


def find_kanjis_in_dict(kanjis_data: dict, kanji_to_find: str):
    """
    Finds and returns a tuple of kanji characters from a dictionary that matches a specific kanji string.

    Args:
    -----
    kanjis_data : dict
        A dictionary where kanji characters are keys.
    kanji_to_find : str
        The kanji string to find in the dictionary.

    Returns:
    --------
    tuple
        A tuple of kanji characters found in the dictionary, or None if not found.
    """
    merged_keys = ""
    for key in kanjis_data.keys():  # Merge all kanjis in one string
        merged_keys += key
    if kanji_to_find in merged_keys:
        position_start = merged_keys.index(kanji_to_find)
        position_end = position_start + len(kanji_to_find) - 1

        current_position = 0
        kanjis_in_dict = []
        for key in kanjis_data.keys():
            pass
            if current_position >= position_start and current_position <= position_end:
                kanjis_in_dict.append(key)
            current_position += len(key)
        return tuple(kanjis_in_dict)
    else:
        return None


def get_kanji_reading_meaning_position(sentence: str):
    pattern = r'\[([^\|\[\]]+)\|([^\[\]]+)\]'
    result = re.findall(pattern, sentence)
    kanji_data = KanjiDataList()
    for match in result:
        kanji, reading = match
        reading = reading.replace('|', '')
        kanji_data.add(kanji, reading, "")
    return kanji_data
