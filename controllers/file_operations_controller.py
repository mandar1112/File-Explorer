
from pathlib import Path
from collections.abc import Callable
from core.file_manager import FileManager
from services.clipboard_service import ClipboardOperation


class FileOperationsController:

    def __init__(self, file_manager : FileManager):
        self.file_manager = file_manager
    

    def copy_items(self, sources: list[Path], destination: Path):
        return self._execute_operation(sources, destination ,self.file_manager.copy)


    def move_items(self, sources: list[Path], destination: Path):
        return self._execute_operation(sources, destination, self.file_manager.move)


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


    def paste(self, sources: list[Path], destination: Path, operation: ClipboardOperation):
        if operation == ClipboardOperation.COPY:
            return self.copy_items(sources, destination)

        elif operation == ClipboardOperation.CUT:
            return self.move_items(sources, destination)

        return []
    

    def create_folder(self, path: Path):
        self.file_manager.create_folder(path)


    def create_file(self, path: Path):
        self.file_manager.create_file(path)


    def _execute_operation(self, sources: list[Path], destination: Path, operation: Callable[[Path, Path], None]) -> list:
        failed = []

        for source in sources:
            if not self._validate_operation(source, destination):
                continue

            try:
                operation(source, destination)
            except Exception as e:
                failed.append((source, e))
        
        return failed


    def _validate_operation(self, source: Path, destination: Path) -> bool:
        
        if not source.exists():
            return False
        
        if not destination.exists():
            return False
        
        if not destination.is_dir():
            return False
        
        # Same Folder
        if source.parent == destination:
            return False
        
        # Dropping onto itself
        if source == destination:
            return False
        
        # Folder into its own descendant
        if source.is_dir():
            try:
                destination.relative_to(source)
                return False
            except ValueError:
                pass
        
        return True
    


