from re import match

def is_word_romaji_kana_or_kanji(word: str) -> bool: 
    pattern = r'^[\u0041-\u005A\u0061-\u007A\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\uFF66-\uFF9F々]+$'
    
    return bool(match(pattern, word))

def get_position_kanji_sentence(sentence, kanji_data_list):
    """Return a dictionnary containing kanjis positions in sentence as keys, and kanjis as values."""
    kanjis = [k for k, *_ in kanji_data_list]
    kanjis_sorted = sorted(kanjis, key=len, reverse=True)

    dict = {}
    for word in kanjis_sorted:
        if word != "" and word in sentence:
            while (sentence.find(word) != -1):
                for i in range(
                        sentence.find(word),
                        sentence.find(word) + len(word)):
                    dict[i] = word

                replacement = "_" * len(word)
                sentence = sentence.replace(word, replacement, 1)
    return dict
