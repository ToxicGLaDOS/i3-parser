from enum import Enum, auto
from typing import Iterable
from utils.all_spaces import all_spaces
from commands.command import Command


class ExecCommand(Command):
    def __init__(self, command: str, spacing: Iterable[str] = all_spaces):
        super().__init__()
        self.command = command
        self.spacing = spacing
    
    def __str__(self):
        return f"exec{self.spacing[0]}{self.command}"