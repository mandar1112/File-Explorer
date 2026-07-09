
from pathlib import Path
from send2trash import send2trash
import shutil as sh


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


    def move(self, source: Path, destination_dir: Path):
        destination = destination_dir / source.name
        sh.move(source , destination)
        


    def copy(self, source: Path, destination_dir: Path):
        destination = destination_dir / source.name
        
        if source.is_file():
            sh.copy2(source, destination)
        else:
            sh.copytree(source, destination)


    def create_folder(self, path: Path):
        path.mkdir()


    def create_file(self, path):
        path.touch()
