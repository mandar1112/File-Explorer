
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QKeyEvent, QAction
from PySide6.QtWidgets import QLineEdit, QStyle


class SearchBar(QLineEdit):

    searchTextChanged = Signal(str)
    escapePressed = Signal()

    def __init__(self):
        super().__init__()

        self.setPlaceholderText("Search Current Folder...")
        self.setClearButtonEnabled(True)

        self.textChanged.connect(self.searchTextChanged.emit)

    
    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.selectAll()
    

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Escape:
            self.escapePressed.emit()
            return
        
        super().keyPressEvent(event)
