
from PySide6.QtWidgets import QMenuBar


class MainMenuBar(QMenuBar):

    def __init__(self, actions):
        super().__init__()

        self.actions = actions

        self.create_file_menu()
        self.create_edit_menu()
        self.create_view_menu()
        self.create_go_menu()
        self.create_help_menu()

    
    def create_file_menu(self):
        file_menu = self.addMenu("File")
        file_menu.addAction(self.actions.new_folder)
        file_menu.addAction(self.actions.new_file)
        file_menu.addSeparator()
        file_menu.addAction(self.actions.rename)
        file_menu.addAction(self.actions.delete)
        file_menu.addSeparator()
        file_menu.addAction(self.actions.exit)
  
    
    def create_edit_menu(self):
        edit_menu = self.addMenu("Edit")
        edit_menu.addAction(self.actions.copy)
        edit_menu.addAction(self.actions.cut)
        edit_menu.addAction(self.actions.paste)
        edit_menu.addSeparator()
        edit_menu.addAction(self.actions.select_all)


    def create_view_menu(self):
        view_menu = self.addMenu("View")
        view_menu.addAction(self.actions.refresh)


    def create_go_menu(self):
        go_menu = self.addMenu("Go")
        go_menu.addAction(self.actions.back)
        go_menu.addAction(self.actions.forward)
        go_menu.addSeparator()
        go_menu.addAction(self.actions.up)


    def create_help_menu(self):
        help_menu = self.addMenu("Help")
        help_menu.addAction(self.actions.about)