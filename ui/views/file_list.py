
from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import Qt, Signal, QMimeData, QUrl
from PySide6.QtGui import (
    QDrag,
    QDragEnterEvent,
    QDragLeaveEvent,
    QDragMoveEvent,
    QDropEvent
)
from PySide6.QtWidgets import (
    QListWidget, 
    QListWidgetItem,
    QAbstractItemView
)

from services.icon_service import IconService
from ui.events import DropRequested



class FileListView(QListWidget):

    fileActivated = Signal(Path)
    fileContextMenuRequested = Signal(object)
    backgroundContextMenuRequested = Signal(object)
    selectionInfoChanged = Signal(list)

    # sources, destination
    dropRequested = Signal(DropRequested)

    def __init__(self):
        super().__init__()

        self.current_directory: Path | None = None

        self.icon_service = IconService()

        self.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.itemSelectionChanged.connect(self.on_selection_changed)
        
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu_requested)

        # Drag and Drop permissions
        self._hovered_drop_target: Path | None = None

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(Qt.MoveAction)

    
    def show_files(self, directory: Path, files: list[Path]):
        self.current_directory = directory
        self.clear()
        
        for file in files:
            item = QListWidgetItem(file.name)
            item.setIcon(self.icon_service.get_icon(file))
            item.setData(Qt.UserRole, file)
            self.addItem(item)
    

    def on_item_double_clicked(self, item):
        self.fileActivated.emit(item.data(Qt.UserRole))
    

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


    def get_drop_destination(self, position) -> Path | None:
        item = self.itemAt(position)

        if item is None:
            return self.current_directory
        
        destination = item.data(Qt.UserRole)

        if destination.is_dir():
            return destination
        
        return None

    
    # Drag and Drop
    def startDrag(self, supportedAction: Qt.DropAction) -> None:
        paths = self.selected_paths()

        if not paths:
            return
        
        mime_data = QMimeData()
        urls = [QUrl.fromLocalFile(str(path)) for path in paths]
        mime_data.setUrls(urls)

        drag = QDrag(self)
        drag.setMimeData(mime_data)

        drag.exec(Qt.CopyAction | Qt.MoveAction, Qt.MoveAction)


    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        destination = self.get_drop_destination(event.position().toPoint())
        
        if destination is None:
            event.ignore()
            return
        
        if destination != self._hovered_drop_target:
            self._hovered_drop_target = destination

        event.accept()

    
    def dragLeaveEvent(self, event: QDragLeaveEvent) -> None:
        self._hovered_drop_target = None
        event.accept()
    

    def dropEvent(self, event: QDropEvent) -> None:
        destination = self.get_drop_destination(event.position().toPoint())
        
        if destination is None:
            event.ignore()
            return
        
        sources = [
            Path(url.toLocalFile()) 
            for url in event.mimeData().urls()
        ]

        # Ignore if every source is already in destination
        if all(source.parent == destination for source in sources):
            event.ignore()
            return

        request = DropRequested(
            sources=sources, 
            destination=destination, 
            action=event.dropAction()
        )
        self.dropRequested.emit(request)
        
        self._hovered_drop_target = None
        event.accept()
    
