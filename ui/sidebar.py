
from pathlib import Path

from PySide6.QtWidgets import (QListWidget, QListWidgetItem)
from PySide6.QtCore import (Qt, Signal, QStandardPaths)


class SidebarWidget(QListWidget):

    locationSelected = Signal(Path)

    def __init__(self):
        super().__init__()
        self.setup_items()
        self.itemClicked.connect(self.on_item_double_clicked)

    
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


    def on_item_double_clicked(self, item):
        path = item.data(Qt.UserRole)
        self.locationSelected.emit(path)