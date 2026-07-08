
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtCore import Qt


class ApplicationActions:

    def __init__(self, parent):
        self.parent = parent

        self.create_navigation_actions()
        self.create_context_menu_actions()
        self.create_file_actions()
        self.create_edit_actions()
        self.create_view_actions()
        self.create_help_actions()

    
    def create_navigation_actions(self):
        self.back = QAction("←", self.parent)
        self.forward = QAction("→", self.parent)
        self.up = QAction("↑", self.parent)


    def create_context_menu_actions(self):
        self.open = QAction("Open", self.parent)
        self.properties = QAction("Properties", self.parent)


    def create_file_actions(self):
        self.rename = QAction("Rename", self.parent)
        self.rename.setShortcut(QKeySequence(Qt.Key_F2))
        
        self.delete = QAction("Delete", self.parent)
        self.delete.setShortcut(QKeySequence(Qt.Key_Delete))

        self.exit = QAction("Exit", self.parent)


    def create_edit_actions(self):
        self.copy = QAction("Copy", self.parent)
        self.cut = QAction("Cut", self.parent)
        self.paste = QAction("Paste", self.parent)
        self.select_all = QAction("Select All", self.parent)

        self.copy.setShortcut(QKeySequence.Copy)
        self.cut.setShortcut(QKeySequence.Cut)
        self.paste.setShortcut(QKeySequence.Paste)
        self.select_all.setShortcut(QKeySequence.SelectAll)
    

    def create_view_actions(self):
        self.refresh = QAction("Refresh", self.parent)
        self.refresh.setShortcut(Qt.Key_F5)

   
    def create_help_actions(self):
        self.about = QAction("About", self.parent)
        