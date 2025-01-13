from PyQt6.QtGui import QStandardItem


class KanjiData():
    def __init__(self, word: str, reading: str, meaning: str) -> None:
        self.word = word
        self.reading = reading
        self.meaning = meaning

    def __get__(self):
        return (self.word, self.reading, self.meaning)

    def __iter__(self):
        return iter((self.word, self.reading, self.meaning))

    def get_item(self):
        return [
            QStandardItem(
                self.word), QStandardItem(
                self.reading), QStandardItem(
                self.meaning)]

    def update_attributes(self, word, reading, meaning):
        self.word = word
        self.reading = reading
        self.meaning = meaning
