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

def show_transcription(view, event, sentence_len, position_kanji, kanji_data):
    """Show a QToolTip containing furigana of the howered kanji. """

    cursor = view.cursorForPosition(event.pos()) # Get cursor for position
    char_position = cursor.position() # Get the position of the character under the cursor

    if char_position <= sentence_len:
        cursor.setPosition(char_position) # Place the cursor at this position and select the character
        cursor.movePosition(QTextCursor.MoveOperation.Right, QTextCursor.MoveMode.KeepAnchor, 1)
        char = cursor.selectedText()

        
        if cursor.position() - 1 in position_kanji.keys(): # TODO: Add "and is_kanji(char) ?"
            kanji = position_kanji[cursor.position() - 1]
            kana_transcription, _, _ = kanji_data.get_data_by_kanji(kanji)

            print_furigana(view, cursor, kana_transcription)
        else:
            QToolTip.hideText()
    else:
        cursor.select(QTextCursor.SelectionType.WordUnderCursor)
        word = cursor.selectedText()

        if is_kanji(word):
            try:
                kana_transcription, _, _ = kanji_data.get_data_by_kanji(kanji)
                print_furigana(view, cursor, kana_transcription)
            except:
                QToolTip.hideText()
        else:
            QToolTip.hideText()

def print_furigana(view, cursor, kana_transcription):
    cursor_rect = view.cursorRect(cursor)
    text_position = cursor_rect.center()
    global_position = view.mapToGlobal(text_position)
    QToolTip.showText(global_position, kana_transcription, view)