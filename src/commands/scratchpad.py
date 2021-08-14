from enum import auto
from typing import Iterable
from utils.all_spaces import all_spaces
from utils.enums import LowercaseEnum
from utils.measurement import Measurement
from commands.command import Command

class ScratchpadCommand(Command):
    def __init__(self, spacing: Iterable[str] = all_spaces):
        super().__init__()
        self.spacing = spacing
    
    def __str__(self):
        spacing_iterator = iter(self.spacing)
        return f"scratchpad{next(spacing_iterator)}show"
