
from PySide6.QtWidgets import QStatusBar


class MainStatusBar(QStatusBar):

    def __init__(self):
        super().__init__()

        self.set_message("Ready")
    

    def set_message(self, message):
        self.showMessage(message)