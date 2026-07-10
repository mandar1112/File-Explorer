
from PySide6.QtWidgets import (
    QStatusBar,
    QLabel
)


class MainStatusBar(QStatusBar):

    def __init__(self):
        super().__init__()

        self.create_widgets()
        self.create_layout()

        self.show_ready()
    
    
    def create_widgets(self) -> None:
        self.info_label = QLabel()
        self.disk_label = QLabel()
    

    def create_layout(self) -> None:
        self.addWidget(self.info_label)
        self.addPermanentWidget(self.disk_label)


    def show_ready(self) -> None:
        self.info_label.setText("Ready")
        self.clear_disk_space()

    
    def show_selection(self, total_items: int, selected_items: int = 0, selected_size: str | None = None) -> None:
        item_text = "item" if total_items == 1 else "items"
        message = f"{total_items} {item_text}"
        
        if selected_items > 0:
            message += f"  |  {selected_items} selected"
        
        if selected_size:
            message += f"  |  {selected_size}"
        
        self.info_label.setText(message)
    

    def show_disk_space(self, free_space: str):
        self.disk_label.setText(f"Free: {free_space}")
    
    
    def show_message(self, message: str):
        self.info_label.setText(message)

    
    def clear_disk_space(self):
        self.disk_label.setText("")
