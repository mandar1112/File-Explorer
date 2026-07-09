
from pathlib import Path

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QInputDialog
)

from core.file_manager import FileManager
from controllers.file_operations_controller import FileOperationsController
from controllers.navigation_controller import NavigationController

from services.file_launcher import FileLauncher
from services.clipboard_service import ClipboardService, ClipboardOperation

from ui.toolbar import MainToolBar
from ui.sidebar import SidebarWidget
from ui.menu_bar import MainMenuBar
from ui.address_bar import AddressBar
from ui.status_bar import MainStatusBar
from ui.context_menu import FileContextMenu
from ui.actions import ApplicationActions
from ui.views.file_list import FileListView



class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.file_manager = FileManager()
        self.file_operations = FileOperationsController(self.file_manager)
        self.navigation = NavigationController()
        self.file_launcher = FileLauncher()
        self.clipboard = ClipboardService()
        
        # Window
        self.setWindowTitle("File Explorer")
        self.resize(1200, 700)

        # UI Components
        self.actions = ApplicationActions(self)
        self.create_components()

        # Build UI
        self.build_ui()

        # Connect Signals
        self.connect_signals()

        # Load Initial Directory
        self.display_directory(".")


    def create_components(self):
        self.file_list = FileListView()
        self.toolbar = MainToolBar(self.actions)
        self.sidebar = SidebarWidget()
        self.menu_bar = MainMenuBar(self.actions)
        self.address_bar = AddressBar()
        self.status_bar = MainStatusBar()
        self.context_menu = FileContextMenu(self.actions)


    def build_ui(self):
        self.addToolBar(self.toolbar)
        self.setMenuBar(self.menu_bar)
        self.setStatusBar(self.status_bar)
        self.create_main_layout()

    
    def connect_signals(self):
        # Toolbar
        self.actions.back.triggered.connect(self.on_back_clicked)
        self.actions.forward.triggered.connect(self.on_forward_clicked)
        self.actions.up.triggered.connect(self.on_up_clicked)

        # Address Bar
        self.address_bar.pathSubmitted.connect(self.display_directory)

        # Sidebar
        self.sidebar.locationSelected.connect(self.on_sidebar_location_selected)

        # File List
        self.file_list.fileActivated.connect(self.on_file_activated)
        self.file_list.contextMenuRequested.connect(self.show_context_menu)
        
        # Action
        self.actions.new_folder.triggered.connect(self.trigger_new_folder)
        self.actions.new_file.triggered.connect(self.trigger_new_file)
        self.actions.open.triggered.connect(self.trigger_open)
        self.actions.copy.triggered.connect(self.trigger_copy)
        self.actions.cut.triggered.connect(self.trigger_cut)
        self.actions.paste.triggered.connect(self.trigger_paste)
        self.actions.properties.triggered.connect(self.trigger_properties)
        self.actions.delete.triggered.connect(self.trigger_delete)
        self.actions.rename.triggered.connect(self.trigger_rename)
        self.actions.exit.triggered.connect(self.trigger_exit)
        self.actions.refresh.triggered.connect(self.trigger_refresh)
        self.actions.about.triggered.connect(self.trigger_about)


    def create_main_layout(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout()
        central.setLayout(main_layout)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.address_bar)
        right_layout.addWidget(self.file_list)

        main_layout.addWidget(self.sidebar)
        main_layout.addLayout(right_layout)
    

    def show_context_menu(self, position):
        paths = self.file_list.selected_paths()        
        self.actions.rename.setEnabled(len(paths) == 1)
        self.context_menu.exec(position)


    def update_navigation(self, path, add_to_history):
        if add_to_history:
            return self.navigation.navigate(path)
        path = Path(path)
        self.navigation.current_path = path
        return path


    # Directory Display
    def display_directory(self, path, add_to_history=True):
        path = self.update_navigation(path, add_to_history)
        self.address_bar.setText(str(path))
        files = self.file_manager.list_directory(path)
        self.file_list.show_files(files)
    
    
    # Trigger Event
    def trigger_new_folder(self):
        self.on_new_folder_requested()


    def trigger_new_file(self):
        self.on_new_file_requested()


    def trigger_open(self):
        path = self.file_list.current_path()
        if path is None:
            return
        
        self.on_file_activated(path)
    

    def trigger_copy(self):
        paths = self.file_list.selected_paths()
        if not paths:
            return
        
        self.clipboard.copy(paths)
    

    def trigger_paste(self):
        self.on_paste_requested()


    def trigger_cut(self):
        paths = self.file_list.selected_paths()
        if not paths:
            return
        
        self.clipboard.cut(paths)

        
    def trigger_properties(self):
        path = self.file_list.current_path()
        if path is None:
            return
        
        print(path)


    def trigger_delete(self):
        paths = self.file_list.selected_paths()
        if not paths:
            return
        
        self.on_delete_requested(paths)


    def trigger_rename(self):
        path = self.file_list.current_path()
        if path is None:
            return
        
        self.on_rename_requested(path)

    
    def trigger_exit(self):
        self.on_exit_requested()
    

    def trigger_refresh(self):
        self.on_refresh_requested()


    def trigger_about(self):
        self.on_about_requested()


    # Toolbar Events
    def on_back_clicked(self):
        path = self.navigation.go_back()
        if path:
            self.display_directory(path)


    def on_forward_clicked(self):
        path = self.navigation.go_forward()
        if path:
            self.display_directory(path)


    def on_up_clicked(self):
        path = self.navigation.go_up()
        if path:
            self.display_directory(path)
    

    # Sidebar Events
    def on_sidebar_location_selected(self, path: Path):
        self.display_directory(path)


    # File Events
    def refresh_current_directory(self):
        self.display_directory(self.navigation.current_path, add_to_history=False)


    def show_error(self, title, message):
        QMessageBox.critical(self, title, message)


    def on_file_activated(self, path: Path):
        if path.is_dir():
            self.display_directory(path)
            return
        
        self.file_launcher.open(path)
    

    def on_new_folder_requested(self):
        folder_name, ok = QInputDialog.getText(self, "New Folder", "Folder Name: ")

        if not ok:
            return
        
        folder_name = folder_name.strip()
        if not folder_name:
            return
        
        folder_path = self.navigation.current_path / folder_name

        if folder_path.exists():
            self.show_error("New Folder", "A folder with that name already exists.")
            return

        try:
            self.file_operations.create_folder(folder_path)
            self.refresh_current_directory()
        except Exception as e:
            self.show_error("New Folder Error", str(e))
    

    def on_new_file_requested(self):
        file_name, ok = QInputDialog.getText(self, "New File", "File Name:")
        if not ok:
            return
        
        file_name = file_name.strip()
        if not file_name:
            return
        
        file_path = self.navigation.current_path / file_name

        if file_path.exists():
            self.show_error("New File", "A file or folder with that name already exists.")
            return

        try:
            self.file_operations.create_file(file_path)
            self.refresh_current_directory()
        except Exception as e:
            self.show_error("New File Error", str(e))


    def on_delete_requested(self, paths):
        reply = QMessageBox.question(self, "Delete", f"Delete {len(paths)} item(s)?", QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        
        try:
            self.file_operations.delete(paths)
            self.refresh_current_directory()
        except Exception as e:
            self.show_error("Delete Error", str(e))
    

    def on_rename_requested(self, path):
        new_name, ok = QInputDialog.getText(self, "Rename", "New name: ", text=path.name)

        if not ok:
            return
        
        new_name = new_name.strip()
        
        if not new_name:
            return

        if new_name == path.name:
            return
        
        try:
            self.file_operations.rename(path, new_name)
            self.refresh_current_directory()
        except Exception as e:
            self.show_error("Rename Error", str(e))
    

    def on_paste_requested(self):
        paths = self.clipboard.get_paths()

        if not paths:
            return
        
        operation = self.clipboard.get_operation()

        try:
            self.file_operations.paste(paths, self.navigation.current_path, operation)
            
            if operation == ClipboardOperation.CUT:
                self.clipboard.clear()
            self.refresh_current_directory()
        except Exception as e:
            self.show_error("Paste Error", str(e))


    def on_exit_requested(self):
        self.close()
    

    def on_refresh_requested(self):
        self.refresh_current_directory()   

    def on_about_requested(self):
        QMessageBox.about(self, "About Explorer", "Explorer\n\n" "Version: 0.5\n" "Developed by Mandar Patil\n" "Built with Python and PySide6")


