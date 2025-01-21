from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QLabel
from .vocabulary_combobox import VocabularyComboBox


class SentenceAttributesWidget(QWidget):
    def __init__(self, parent: QWidget, card_view) -> None:
        super().__init__(parent)
        self.card_view = card_view
        layout = QVBoxLayout(self)

        label = QLabel("Sentence Attributes")
        label.setProperty("class", "title")
        layout.addWidget(label)


        form_layout = QFormLayout()
        layout.addLayout(form_layout)

        
        attributes_name = [
            "Sentence:",
            "Meaning:",
            "Word 1: ",
            "Word 2: ",
        ]

        self.widget_list = self._init_layout(form_layout, attributes_name)
        self.attributes_value = []

    def _init_layout(self, form_layout: QFormLayout, attributes_name: list):
        widget_list = []

        label_list = []
        for text in attributes_name:
            label = QLabel(text)
            label.setProperty("class", "attributes")
            label_list.append(label)

        line_edit = QLineEdit()
        line_edit.setProperty("class", "sentence")
        widget_list.append(line_edit)
        form_layout.addRow(label_list[0], line_edit)
        line_edit.textEdited.connect(self._is_sentence_attribute_modified)

        line_edit = QLineEdit()
        line_edit.setProperty("class", "translation")
        widget_list.append(line_edit)
        form_layout.addRow(label_list[1], line_edit)
        line_edit.textEdited.connect(self._is_translation_attribute_modified)

        self.word1_combobox = VocabularyComboBox()
        widget_list.append(self.word1_combobox)
        form_layout.addRow(label_list[2], self.word1_combobox)
        self.word1_combobox.currentIndexChanged.connect(
            self._is_word1_attribute_modified)

        self.word2_combobox = VocabularyComboBox()
        widget_list.append(self.word2_combobox)
        form_layout.addRow(label_list[3], self.word2_combobox)
        self.word2_combobox.currentIndexChanged.connect(
            self._is_word2_attribute_modified)

        return tuple(widget_list)

    def _is_sentence_attribute_modified(self):
        text = self.widget_list[0].text()
        self.attributes_value[0] = text
        self.card_view.set_card_view_from_attributes_values(
            self.attributes_value)

    def _is_translation_attribute_modified(self):
        text = self.widget_list[1].text()
        self.attributes_value[1] = text
        self.card_view.set_card_view_from_attributes_values(
            self.attributes_value)

    def _is_word1_attribute_modified(self):
        try:
            word1_row = self.widget_list[2].currentIndex()
            kanji1_data = self.sentence.kanji_data_list[word1_row]
            self.attributes_value[2] = kanji1_data
        except BaseException:
            self.attributes_value[2] = None
        self.card_view.set_card_view_from_attributes_values(
            self.attributes_value)
        self.widget_list[3].hide_and_change_index(
            self.widget_list[2].currentIndex())

    def _is_word2_attribute_modified(self):
        try:
            kanji2_row = self.widget_list[3].currentIndex()
            if kanji2_row == len(
                    self.sentence.kanji_data_list):  # If word2 selection is set to None
                kanji2_data = None
            else:
                kanji2_data = self.sentence.kanji_data_list[kanji2_row]
            self.attributes_value[3] = kanji2_data
        except BaseException:
            self.attributes_value[3] = None
        self.card_view.set_card_view_from_attributes_values(
            self.attributes_value)

        self.widget_list[3].hide_and_change_index(
            self.widget_list[2].currentIndex())

    def _kanji_data_model_is_modified(self):
        self.card_view.set_card_view_from_attributes_values(
            self.attributes_value)

    def set_to_new_sentence(self, sentence):
        self.sentence = sentence
        self.sentence.kanji_data_list.model.itemChanged.connect(
            self._kanji_data_model_is_modified)
        self.attributes_value = [None, None, None, None]
        for i in range(2):
            self.attributes_value[i] = sentence.attributes[i]
            self.widget_list[i].setText(sentence.attributes[i])
            self.widget_list[i].setCursorPosition(0)

        self.word1_combobox.set_kanji_data_model(
            sentence.kanji_data_list.first_combobox_model)
        self.word2_combobox.set_kanji_data_model(
            sentence.kanji_data_list.second_combobox_model)

        if sentence.word1_data is None:
            self.widget_list[2].set_to_empty_value()
        else:
            word1_kanji = sentence.word1_data.word
            word1_index = sentence.kanji_data_list._find_kanji_index(word1_kanji)
            self.widget_list[2].setCurrentIndex(word1_index)
            self._is_word1_attribute_modified()

        if sentence.word2_data is None:
            self.widget_list[3].set_to_empty_value()
        else:
            word2_kanji = sentence.word2_data.word
            word2_index = sentence.kanji_data_list._find_kanji_index(word2_kanji)
            self.widget_list[3].setCurrentIndex(word2_index)

        self.sentence.kanji_data_list.model.row_deleted.connect(
            self._is_word1_attribute_modified)
        self.sentence.kanji_data_list.model.row_deleted.connect(
            self._is_word2_attribute_modified)
