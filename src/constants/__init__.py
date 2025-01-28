from enum import Enum

class RetrieverMode(Enum):
    HTTP = 1
    LOCAL = 2

class SentenceWidgetMode(Enum):
    VOCABULARY_SENTENCE = 1
    ADDED_SENTENCE = 2

class KanjiDataComboBoxModelMode(Enum):
    FIRST_COMBO_BOX = 1
    SECOND_COMBO_BOX = 2

class CardTextViewMode(Enum):
    IS_MAIN_WINDOW = 1
    IS_NOT_MAIN_WINDOW = 2

class ModelDialogOptionsMode(Enum):
    FRONT_MODEL = 1
    BACK_MODEL = 2
    STYLE_MODEL = 3