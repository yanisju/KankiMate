from PyQt6.QtWidgets import QPushButton
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl

class WordAudioPlayerButton(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)

        self.player = QMediaPlayer()
        audio_output = QAudioOutput()
        self.player.setAudioOutput(audio_output)
        audio_output.setVolume(50)

        self.clicked.connect(self._play)
    
    def _play(self):
        self.player.setSource(QUrl("C:/Users/ids/AppData/Roaming/Anki2/addons21/kanji_app/data/temp/audio/難しい_audio.mp4"))
        self.player.play()