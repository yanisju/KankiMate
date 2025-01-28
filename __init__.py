from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo, qconnect
from PyQt6.QtGui import QAction
from .app import App

def appStart() -> None:
    app.start()

app = App()
action = QAction("KankiMate", mw)
qconnect(action.triggered, appStart)
mw.form.menuTools.addAction(action)