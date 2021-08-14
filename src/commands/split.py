from enum import auto
from typing import Iterable
from utils.all_spaces import all_spaces
from utils.enums import LowercaseEnum
from commands.command import Command

class SplitDirection(LowercaseEnum):
    HORIZONTAL = auto()
    VERTICAL = auto()
    TOGGLE = auto()
    H = auto()
    V = auto()
    T = auto()


class SplitCommand(Command):
    def __init__(self, direction: SplitDirection, spacing: Iterable[str] = all_spaces):
        super().__init__()
        self.direction = direction
        self.spacing = spacing
    
    def __str__(self):
        return f"split{self.spacing[0]}{self.direction}"