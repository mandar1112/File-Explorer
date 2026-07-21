
from pathlib import Path

from PySide6.QtGui import QDragEnterEvent, QDragMoveEvent, QDropEvent
from ui.events import DropRequested

from PySide6.QtWidgets import (QListWidget, QListWidgetItem)
from PySide6.QtCore import (Qt, Signal, QStandardPaths)


class SidebarWidget(QListWidget):

    locationSelected = Signal(Path)
    dropRequested = Signal(DropRequested)

    def __init__(self):
        super().__init__()
        
        self.setup_items()
        self.itemClicked.connect(self.on_item_clicked)

        # Drag and Drop
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(Qt.MoveAction)

    
    def setup_items(self):
        locations = [
            ("Home", Path.home()),
            ("Desktop", Path(QStandardPaths.writableLocation(QStandardPaths.DesktopLocation))),
            ("Documents", Path(QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation))),
            ("Downloads", Path(QStandardPaths.writableLocation(QStandardPaths.DownloadLocation))),
            ("Pictures", Path(QStandardPaths.writableLocation(QStandardPaths.PicturesLocation))),
            ("Music", Path(QStandardPaths.writableLocation(QStandardPaths.MusicLocation))),
            ("Videos", Path(QStandardPaths.writableLocation(QStandardPaths.MoviesLocation))),
        ]

        for text, path in locations:
            if path.exists():
                self.add_location(text, path)

        self.setMaximumWidth(150)


    def add_location(self, text:str, path:Path):
        if not path.exists():
            return
        
        item = QListWidgetItem(text)
        item.setData(Qt.UserRole, path)
        self.addItem(item)


    def on_item_clicked(self, item):
        path = item.data(Qt.UserRole)
        self.locationSelected.emit(path)
    

    def get_drop_destination(self, position) -> Path | None:
        item = self.itemAt(position)

        if item is None:
            return None
        
        return item.data(Qt.UserRole)
    

    # Drag and Drop
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

        event.accept()