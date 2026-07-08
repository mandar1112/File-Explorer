
from PySide6.QtWidgets import QMenu


class FileContextMenu(QMenu):

    def __init__(self, actions):
        super().__init__()

        self.actions = actions

        self.build_menu()
    

    def build_menu(self):
        self.addAction(self.actions.open)
        
        self.addSeparator()
        
        self.addAction(self.actions.rename)
        self.addAction(self.actions.delete)
        
        self.addSeparator()

        self.addAction(self.actions.properties)