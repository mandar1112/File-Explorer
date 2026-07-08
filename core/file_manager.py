
from pathlib import Path
from send2trash import send2trash


class FileManager:

    def list_directory(self, path):
        folder = Path(path)
        if not folder.exists():
            return []
        return list(folder.iterdir())


    def delete(self, path: Path):
        send2trash(path)


    def rename(self, source: Path, destination: Path):
        source.rename(destination)


    def move(self, source, destination):
        pass


    def copy(self, source, destination):
        pass


    def create_folder(self, path):
        pass


    def create_file(self, path):
        pass
