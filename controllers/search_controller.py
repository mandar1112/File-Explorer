
from pathlib import Path


class SearchController:

    def filter_files(self, files: list[Path], query: str) -> list[Path]:
        
        query = query.lower().strip()

        if not query:
            return files
        
        return [file for file in files if query in file.name.lower()]