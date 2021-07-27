from enum import Enum, auto
from typing import Tuple, Iterable
from utils.all_spaces import all_spaces
from commands.command import Command


class ModeCommand(Command):
    def __init__(self, mode_name: str, spacing: Iterable[str] = all_spaces):
        super().__init__()
        self.mode_name = mode_name
        self.spacing = spacing
    
    def __str__(self):
        return f"mode{self.spacing[0]}{self.mode_name}"