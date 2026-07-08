
from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Signal


class AddressBar(QLineEdit):

    pathSubmitted = Signal(str)

    def __init__(self):
        super().__init__()

        self.setPlaceholderText("Enter Text")
        self.returnPressed.connect(self.on_return_pressed)

    
    def on_return_pressed(self):
        self.pathSubmitted.emit(self.text())