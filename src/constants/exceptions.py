class VocabularyAlreadyExists(Exception):
    def __init__(self, word: str) -> None:
        message = f"{word} has already been imported."
        super().__init__(message)

class VocabularyIsNotValid(Exception):
    def __init__(self, word: str) -> None:
        message = f"{word} is not valid. (should contains only romajis, kana or kanjis)"
        super().__init__(message)
    