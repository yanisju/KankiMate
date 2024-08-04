def get_position_kanji_sentence(sentence, kanjis):
    """Return a dictionnary containing positions in sentence as keys, and kanjis as values."""
    kanjis_sorted = sorted(kanjis, key=len, reverse=True)

    dict = {}
    for word in kanjis_sorted:
        while(sentence.find(word) != -1):
            for i in range(sentence.find(word), sentence.find(word) + len(word)):
                dict[i] = word
            
            replacement = "_" * len(word)
            sentence = sentence.replace(word, replacement, 1)
    return dict