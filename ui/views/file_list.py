
from PySide6.QtWidgets import (
    QListWidget, 
    QListWidgetItem,
    QAbstractItemView
)
from PySide6.QtCore import (
    Qt, 
    Signal
)

from pathlib import Path
from services.icon_service import IconService



class FileListView(QListWidget):

    fileActivated = Signal(Path)
    fileContextMenuRequested = Signal(object)
    backgroundContextMenuRequested = Signal(object)
    selectionInfoChanged = Signal(list)

    def __init__(self):
        super().__init__()

        self.icon_service = IconService()
        self.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu_requested)
        self.itemSelectionChanged.connect(self.on_selection_changed)

    
    def show_files(self, files):
        self.clear()
        
        for file in files:
            item = QListWidgetItem(file.name)
            item.setIcon(self.icon_service.get_icon(file))
            item.setData(Qt.UserRole, file)
            self.addItem(item)
    

    def on_item_double_clicked(self, item):
        path = item.data(Qt.UserRole)
        self.fileActivated.emit(path)
    

    def selected_paths(self) -> list[Path]:
        # selected_items = self.selectedItems()
        # paths = []
        # for item in selected_items:
        #     paths.append(item.data(Qt.UserRole))

        # return paths

        return [item.data(Qt.UserRole) for item in self.selectedItems()]


    def current_path(self) -> Path | None:
        item = self.currentItem()

        if item is None:
            return None
        
        return item.data(Qt.UserRole)
    

    def on_context_menu_requested(self, position):
        global_position = self.viewport().mapToGlobal(position)

        item = self.itemAt(position)

        if item:
            self.setCurrentItem(item)
            self.fileContextMenuRequested.emit(global_position)
        else:
            self.backgroundContextMenuRequested.emit(global_position)
    

    def on_selection_changed(self):
        self.selectionInfoChanged.emit(self.selected_paths())
