
from os import path
from PyQt6.QtWidgets import QMainWindow, QToolBar, QFormLayout, QLineEdit, QStatusBar

from .central_widget import CentralWidget
from .action.import_from_file import ImportFromFileAction


class MainWindow(QMainWindow):
    def __init__(self, vocabulary_manager):
        super().__init__(None)
        self.setWindowTitle("KankiMate")
        self._resize_and_center()

        self.vocabulary_manager = vocabulary_manager

        centralWidget = CentralWidget(self, vocabulary_manager)
        self.setCentralWidget(centralWidget)

        addon_base_dir = path.realpath(__file__)
        for i in range(3):
            addon_base_dir = path.dirname(addon_base_dir)

        css_file_path = path.join(addon_base_dir, "styles", "group_box.css")

        with open(css_file_path, "r") as css_file:
            self.setStyleSheet(css_file.read())

        self._createMenu()
        # self._createToolBar()
        # self._createStatusBar()

    def _createMenu(self):
        file = self.menuBar().addMenu("File")
        import_from_file_action = ImportFromFileAction(
            self, self.vocabulary_manager)
        file.addAction(import_from_file_action)
        file.addAction("&Exit", self.close)

    def _createToolBar(self):
        tools = QToolBar(parent=self)
        layout = QFormLayout()
        layout.addRow("Name:", QLineEdit())

        tools.addWidget(layout)
        self.addToolBar(tools)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("I'm the Status Bar")
        self.setStatusBar(status)

    def _resize_and_center(self):
        screen_rect = self.screen().availableGeometry()
        self.resize(screen_rect.width() - 200, screen_rect.height() - 100)

        x_center = int((screen_rect.width() - self.width()) / 2)
        y_center = int((screen_rect.height() - self.height()) / 2)
        self.move(x_center, y_center)
