
from datetime import datetime

def format_size(size: int) -> str:
    if size == 0:
        return "0 B"
    
    units = ["B", "KB", "MB", "GB", "TB"]

    value = float(size)

    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.1f} {unit}"

        value /= 1024


def format_datetime(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%d %b %Y %I:%M %p") 

