
from PySide6.QtWidgets import QToolBar
from PySide6.QtGui import QAction

class MainToolBar(QToolBar):

    def __init__(self, actions):
        super().__init__("Main Toolbar")

        self.actions = actions

        self.build_toolbar()
    

    def build_toolbar(self):
        self.addAction(self.actions.back)
        self.addAction(self.actions.forward)
        self.addAction(self.actions.up)