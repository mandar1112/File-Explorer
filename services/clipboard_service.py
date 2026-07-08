
from pathlib import Path
from enum import Enum


class ClipboardOperation(Enum):
    COPY = "copy"
    CUT = "cut"



class ClipboardService:

    def __init__(self):
        self._paths = []
        self._operation = None
    

    def copy(self, paths: list[Path]):
        self._paths = paths.copy()
        self._operation = ClipboardOperation.COPY
    

    def cut(self, paths: list[Path]):
        self._paths = paths.copy()
        self._operation = ClipboardOperation.CUT


    def get_paths(self):
        return self._paths.copy()
    

    def get_operation(self):
        return self._operation
    

    def clear(self):
        self._paths.clear()
        self._operation = None
    