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

class CardDialogMode(Enum):
    UNKNOWN = 0
    IS_VOCABULARY = 1
    IS_ADDED = 2

class CardTextViewMode(Enum):
    IS_MAIN_WINDOW = 1
    IS_NOT_MAIN_WINDOW = 2

class ModelDialogOptionsMode(Enum):
    FRONT_MODEL = 1
    BACK_MODEL = 2
    STYLE_MODEL = 3

class VocabularyJLPTLevel(Enum):
    UNKNOWN = 0
    JLPT_N1 = 1
    JLPT_N2 = 2
    JLPT_N3 = 3
    JLPT_N4 = 4
    JLPT_N5 = 5

class VocabularyPitchAccent(Enum):
    ATAMADAKA = 0 # 頭高, starting high going low
    NAKADAKA = 1 # 中高, starting low, going high, finishing low
    ODAKA = 2 # 尾高, starting low, going high, particle must be low
    HEIBAN = 3 # 平板, starting low, going high, particle must be high
    UNKNOWN = 4