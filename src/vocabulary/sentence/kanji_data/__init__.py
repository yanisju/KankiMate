from .str_utils import *
from .model.kanji_data import KanjiDataModel
from .model.combobox import KanjiDataComboBoxModel
from .kanji_data import KanjiData

from ....constants import KanjiDataComboBoxModelMode


class KanjiDataList(list[KanjiData]):
    # List containing Kanjis(kanjis, reading, meaning)

    def __init__(self) -> None:
        self.model = KanjiDataModel()
        self.first_combobox_model = KanjiDataComboBoxModel(
            KanjiDataComboBoxModelMode.FIRST_COMBO_BOX)
        self.second_combobox_model = KanjiDataComboBoxModel(
            KanjiDataComboBoxModelMode.SECOND_COMBO_BOX)

    def bound_to_sentence(self, sentence):
        self.sentence = sentence
        self.model.itemChanged.connect(self._model_is_modified)

    def _find_kanji_index(self, word):
        for index, kanji in enumerate(self):
            if kanji.word == word:
                return index
        return -1

    def get_kanji(self, kanji: str):
        index = self._find_kanji_index(kanji)
        if index == -1:
            return None
        return self[index]

    def add(self, kanji: str, reading: str, meaning: str):
        kanji_index = self._find_kanji_index(kanji)
        if kanji_index == -1:
            new_kanji = KanjiData(kanji, reading, meaning)
            self.append(new_kanji)
            self.model.add_row(new_kanji)
            self.first_combobox_model.appendRow(new_kanji)
            self.second_combobox_model.appendRow(new_kanji)
        else:
            pass  # TODO: change ?

    def add_empty(self):
        new_kanji = KanjiData("", "", "")
        self.append(new_kanji)
        self.model.add_row(new_kanji)
        self.first_combobox_model.append_empty_row()
        self.second_combobox_model.append_empty_row()

    def insert(self, row: int, kanji: str, reading: str, meaning: str):
        kanji_data = KanjiData(kanji, reading, meaning)
        super().insert(row, kanji_data)
        self.model.insertRow(row, kanji_data.get_item())
        self.first_combobox_model.insertRow(row, kanji_data)
        self.second_combobox_model.insertRow(row, kanji_data)

    def remove_by_row(self, row: int):
        row_deleted = self.pop(row)
        self.model.remove(row)
        self.first_combobox_model.takeRow(row)
        self.first_combobox_model.actualize_items_text()
        self.second_combobox_model.takeRow(row)
        self.second_combobox_model.actualize_items_text()
        return row_deleted

    def remove(self, kanji: str):
        # TODO: check if kanji already exists + remove from model
        row = self._find_kanji_index(kanji)
        if row != -1:
            self.remove_by_row(row)
        else:
            raise IndexError

    def clear(self):
        super().clear()
        self.model.clear()
        self.first_combobox_model.clear()
        self.second_combobox_model.clear()

    def update_data_kanji_kana(self, word: str):
        """Update dictionnary if word contains both kanjis and kanas."""
        word_reading = ""
        first_kanji = True
        word_meaning = ""

        for i in range(len(word)):  # For each char of word
            if check_char_is_kana(word[i]):
                word_reading += word[i]
            else:
                try:
                    _, reading, meaning = self.remove(word[i])

                    word_reading += reading
                    if first_kanji:
                        word_meaning = meaning
                        first_kanji = False
                except BaseException:  # Sometimes, word doesn't appear completely in sentence
                    pass
        self.add(word, word_reading, word_meaning)

    def update_data_only_kanji(self, word: str):
        """
        Updates kanji data for a word composed solely of kanji characters by merging data.

        Args:
        -----
        word : str
            The word composed solely of kanji characters to update in the dictionary.

        Raises:
        -------
        Exception
            If the word is not found in the kanji data.
        """
        try:
            kanjis = find_kanjis_in_dict(self, word)
        except KeyError:
            pass
        else:
            data_to_merge = []
            for kanji in kanjis:
                index = self.index(kanji)
                data_to_merge.append(self.pop(index))

            new_reading, new_meaning = "", ""
            for data in data_to_merge:
                _, data_reading, data_meaning = data
                new_reading += data_reading
                new_meaning += data_meaning
            self.add(word, new_reading, new_meaning)

    def update_kanji_meaning(self, kanji: str, meaning: str):
        row = self._find_kanji_index(kanji)
        if row != -1:
            self[row].meaning = meaning
            self.model.modify_row(row, self[row])
            self.first_combobox_model.modify_row(row, self[row])
            self.second_combobox_model.modify_row(row, self[row])
        else:
            raise IndexError

    def merge_kanjis(self, rows):
        kanji_merged_data = ["", "", ""]
        for i in range(len(rows)):
            kanji = self.remove_by_row(rows[i] - i)
            for j, kanji_data in enumerate(kanji):
                kanji_merged_data[j] += kanji_data

        row_to_insert = rows[0]
        self.insert(
            row_to_insert,
            kanji_merged_data[0],
            kanji_merged_data[1],
            kanji_merged_data[2])
        self.first_combobox_model.actualize_items_text()
        self.second_combobox_model.actualize_items_text()

    def _model_is_modified(self, item):
        """Modify its own list to fit with modifications."""

        row = self.model.indexFromItem(item).row()
        kanji = self.model.item(row, 0).text()
        reading = self.model.item(row, 1).text()
        meaning = self.model.item(row, 2).text()

        self[row].update_attributes(kanji, reading, meaning)
        self.sentence._update_position_kanji()

        kanji_data = KanjiData(kanji, reading, meaning)
        self.first_combobox_model.modify_row(row, kanji_data)
        self.second_combobox_model.modify_row(row, kanji_data)

    def set_models(
            self,
            kanji_data_model: KanjiDataModel,
            first_combobox_model: KanjiDataComboBoxModelMode,
            second_combobox_model: KanjiDataComboBoxModelMode):
        self.model = kanji_data_model
        self.first_combobox_model = first_combobox_model
        self.second_combobox_model = second_combobox_model

    def clone(self):
        new_kanji_data_list = KanjiDataList()
        for data in (self):
            kanji, reading, meaning = data
            new_kanji_data_list.add(kanji, reading, meaning)
        new_kanji_data_list.set_models(
            self.model.clone(),
            self.first_combobox_model.clone(),
            self.second_combobox_model.clone())
        return new_kanji_data_list
