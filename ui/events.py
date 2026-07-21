
from dataclasses import dataclass
from pathlib import Path

from PySide6.QtCore import Qt



@dataclass(slots=True)
class DropRequested:
    sources: list[Path]
    destination: Path
    action: Qt.DropAction = Qt.MoveAction


@dataclass(slots=True)
class RenameRequested:
    source: Path
    new_name: str


@dataclass(slots=True)
class DeleteRequested:
    paths: list[Path]


@dataclass(slots=True)
class CopyRequested:
    sources: list[Path]
    destination: Path