
from pathlib import Path

class NavigationController:

    def __init__(self):
        self.history = []
        self.history_index = -1
        self.current_path = Path(".")
    

    def navigate(self, path):
        path = Path(path)
        self.current_path = path

        if (self.history_index == -1 or self.history[self.history_index] != path):
            self.history = self.history[:self.history_index + 1]
            self.history.append(path)
            self.history_index += 1
        
        return self.current_path


    def go_back(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.current_path = self.history[self.history_index]
            return self.current_path
        return None
        
    
    def go_forward(self):
        if self.history_index < (len(self.history) - 1):
            self.history_index += 1
            self.current_path = self.history[self.history_index]
            return self.current_path
        return None
    

    def go_up(self):
        self.current_path = self.current_path.parent
        self.navigate(self.current_path)
        return self.current_path
