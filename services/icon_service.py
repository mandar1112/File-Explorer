
from PySide6.QtWidgets import QFileIconProvider
from PySide6.QtCore import QFileInfo

from pathlib import Path


class IconService:

    def __init__(self):
        self.icon_provider = QFileIconProvider()
    

    def get_icon(self, path: Path):
        file_info = QFileInfo(str(path))
        return self.icon_provider.icon(file_info)
    