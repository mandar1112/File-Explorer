
from pathlib import Path
import platform
import os


class FileLauncher:

    def __init__(self):
        self.system = platform.system()


    def open(self, path: Path):

        if not path.exists():
            raise FileNotFoundError(path)
        
        if self.system == "Windows":
            self._open_windows(path)
        
        elif self.system == "Linux":
            self._open_linux(path)

        elif self.system == "Darwin":
            self._open_macos(path)

        else:
            raise NotImplementedError(f"{self.system} is not supported.")
    

    def open_with(self, path: Path):
        pass


    def reveal(self, path: Path):
        pass


    def open_terminal(self, path: Path):
        pass







    def _open_windows(self, path: Path):
        os.startfile(path)
    
    def _open_linux(self, path: Path):
        pass

    def _open_macos(self, path: Path):
        pass