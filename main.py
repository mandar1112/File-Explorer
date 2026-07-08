
import sys # To Access Operating System

from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow # File Explorer Window

app = QApplication(sys.argv) # Start GUI

window = MainWindow() # Create the Explorer
window.show() # Make it visible

sys.exit(app.exec()) # Run the program until exit
