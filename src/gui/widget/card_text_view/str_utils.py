from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QToolTip


def get_color(tag):
    colors = {"h": "blue",
              "n": "orange",
              "o": "green",
              "a": "red",
              "k": "purple"
              }
    return colors.get(tag[0], "black")  # Default black if tag not found


def colorize_transcription(match):
    kanji = match.group(1)
    tag = match.group(3)
    color = get_color(tag)
    return f'<span style="color:{color}">{kanji}</span>'


def is_kanji(text):
    return any("\u4e00" <= char <= "\u9faf" for char in text)


def show_transcription(view, event, sentence_len: int, position_kanji, kanji_data):
    """Show a QToolTip containing furigana of the howered kanji. """

    cursor = view.cursorForPosition(event.pos())  # Get cursor for position
    # Get the position of the character under the cursor
    char_position = cursor.position()

    if char_position <= sentence_len:
        # Place the cursor at this position and select the character
        cursor.setPosition(char_position)
        cursor.movePosition(
            QTextCursor.MoveOperation.Right,
            QTextCursor.MoveMode.KeepAnchor,
            1)
        char = cursor.selectedText()

        if cursor.position() - 1 in position_kanji.keys():  # TODO: Add "and is_kanji(char) ?"
            kanji = position_kanji[cursor.position() - 1]
            try:
                kana_transcription = kanji_data.get_kanji(kanji).reading
                print_furigana(view, cursor, kana_transcription)
            except:
                pass
            
        else:
            QToolTip.hideText()
    else:
        cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        word = cursor.selectedText()

        if is_kanji(word):
            try:
                kana_transcription = kanji_data.get_kanji(word).reading
                print_furigana(view, cursor, kana_transcription)
            except BaseException:
                QToolTip.hideText()
        else:
            QToolTip.hideText()


def print_furigana(view, cursor, kana_transcription):
    cursor_rect = view.cursorRect(cursor)
    text_position = cursor_rect.center()
    global_position = view.mapToGlobal(text_position)
    QToolTip.showText(global_position, kana_transcription, view)
