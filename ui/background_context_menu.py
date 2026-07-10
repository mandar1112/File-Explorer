
from PySide6.QtWidgets import QMenu


class BackgroundContextMenu(QMenu):

    def __init__(self, actions):
        super().__init__()

        self.actions = actions

        self.build_menu()
    

    def build_menu(self):
        new_menu = self.addMenu("New")
        new_menu.addAction(self.actions.new_folder)
        new_menu.addAction(self.actions.new_file)
        
        self.addSeparator()
        self.addAction(self.actions.paste)
        self.addSeparator()
        self.addAction(self.actions.refresh)
        self.addSeparator()
        self.addAction(self.actions.properties)