from aqt import mw

from PyQt6.QtCore import QCoreApplication, QSettings
from PyQt6.QtWidgets import QApplication

from .src.vocabulary.manager import VocabularyManager
from .src.gui.main_window import MainWindow


class App(QApplication):
    def __init__(self):
        super().__init__([])
        self.vocabulary_manager = VocabularyManager()

        self.main_window = MainWindow(self.vocabulary_manager)
        
    def start(self):
        self.main_window.show()
        # sys.exit(self.exec())

    def _init_settings(self):
        QCoreApplication.setApplicationName("KankiMate")
        QCoreApplication.setOrganizationName("Yanisju")

        config = mw.addonManager.getConfig(__name__)
        settings = QSettings()

        for setting_name, setting_value in config.items():
            settings.setValue(setting_name, setting_value)

if __name__ == '__main__':
    app = App()
    app.start()