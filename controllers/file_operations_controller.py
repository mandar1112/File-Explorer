
from pathlib import Path
from core.file_manager import FileManager


class FileOperationsController:

    def __init__(self, file_manager : FileManager):
        self.file_manager = file_manager
    

    def delete(self, paths: list[Path]):
        failed = []

        for path in paths:
            try:
                self.file_manager.delete(path)
            except Exception as e:
                failed.append((path, e))
        return failed

    
    def rename(self, source: Path, new_name: str):
        destination = source.parent / new_name
        self.file_manager.rename(source, destination)


    def copy(self, source, destination):
        pass


    def move(self, source, destination):
        pass