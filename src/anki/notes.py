# import genanki

from .utils import get_fields_as_list


class Notes(list):
    """A class representing notes within an Anki deck, containing individual cards."""

    def __init__(self, model):
        self.model = model
        self._notes = []
        self._sort_number = 0

    # def add(self, sentence):
    #     """Add a single note to the deck. """
    #     note_field = get_fields_as_list(sentence)
    #     note_field.insert(0, str(self._sort_number))

    #     note = genanki.Note(
    #         model=self.model,
    #         fields=note_field)

    #     self._notes.append(note)
    #     self._sort_number += 1
    #     return note

    # def modify(self, sentence, row):
    #     note_field = get_fields_as_list(sentence)
    #     note = genanki.Note(
    #         model=self.model,
    #         fields=note_field)

    #     self._notes[row] = note

    # def del_card(self, row):
    #     self._notes.pop(row)

    # def clear(self):
    #     super().clear()
    #     self._sort_number = 0
