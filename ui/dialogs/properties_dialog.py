
from pathlib import Path

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QPushButton
)

from services.icon_service import IconService
from utils.formatters import (format_size, format_datetime)


class PropertiesDialog(QDialog):

    def __init__(self, path: Path):
        super().__init__()

        self.path = path

        self.icon_service = IconService()

        self.setWindowTitle(f"{self.path.name} Properties")
        self.setMinimumWidth(500)

        self.create_widgets()
        self.create_layout()
        self.load_properties()


    def create_widgets(self):
        self.icon_label = QLabel()
        icon = self.icon_service.get_icon(self.path)

        icon_pixmap = icon.pixmap(64,64)
        self.icon_label.setPixmap(icon_pixmap)

        self.name_label = QLabel(self.path.name)
        self.name_label.setStyleSheet("font-size: 16px, font-weight: bold")
        self.type_label = QLabel()
        self.location_label = QLabel()
        self.size_label = QLabel()
        self.created_label = QLabel()
        self.modified_label = QLabel()
        self.last_accessed_label = QLabel()
        self.contains_label = QLabel()

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.accept)


    def create_layout(self):
        main_layout = QVBoxLayout(self)

        form_layout = QFormLayout()
        form_layout.addRow("Type: ", self.type_label)
        form_layout.addRow("Location:", self.location_label)
        form_layout.addRow("Contains: ", self.contains_label)
        form_layout.addRow("Size: ", self.size_label)
        form_layout.addRow("Created: ", self.created_label)
        form_layout.addRow("Modified: ", self.modified_label)
        form_layout.addRow("Last Accessed: ", self.last_accessed_label)
        

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.icon_label)
        header_layout.addWidget(self.name_label)
        header_layout.addStretch()

        main_layout.addLayout(header_layout)
        main_layout.addLayout(form_layout)

        button_layout = QHBoxLayout()

        button_layout.addStretch()
        button_layout.addWidget(self.close_button)

        main_layout.addLayout(button_layout)
    

    def load_properties(self):
        stats = self.path.stat()

        self.name_label.setText(self.path.name)
        self.type_label.setText(self.get_file_type())
        self.location_label.setText(str(self.path.parent))
        self.created_label.setText(format_datetime(stats.st_birthtime))
        self.modified_label.setText(format_datetime(stats.st_mtime))
        self.last_accessed_label.setText(format_datetime(stats.st_atime))

        if self.path.is_file():
                self.size_label.setText(format_size(stats.st_size))
                self.contains_label.setText("N/A")
        else:
            files, folders = self.count_folder_contents()
            self.contains_label.setText(self.format_contains(files, folders))
            self.size_label.setText("-")
    

    def get_file_type(self):
        if self.path.is_dir():
            return "Folder"
        
        suffix = self.path.suffix.lower()

        file_types = {
            ".txt": "Text File",
            ".py": "Python File",
            ".json": "JSON File",
            ".csv": "CSV File",
            ".xlsx": "Excel Workbook",
            ".docx": "Word Document",
            ".pdf": "PDF Document",
            ".png": "PNG Image",
            ".jpg": "JPEG Image",
            ".jpeg": "JPEG Image",
            ".gif": "GIF Image",
            ".mp3": "MP3 Audio",
            ".mp4": "MP4 Video",
            ".zip": "ZIP Archive",
        }

        return file_types.get(suffix, f"{suffix.upper()} File" if suffix else "File")
        
    
    def count_folder_contents(self):
        files = 0
        folders = 0

        for item in self.path.iterdir():
            if item.is_file():
                files += 1
            elif item.is_dir():
                folders += 1

        return files, folders  
    

    def format_contains(self, files, folders): 
        file_text = "File" if files == 1 else "Files"
        folder_text = "Folder" if folders == 1 else "Folders"

        return f"{files} {file_text} | {folders} {folder_text}"
 