from enum import auto
from typing import Iterable
from utils.all_spaces import all_spaces
from utils.enums import EnableDisableToggle
from commands.command import Command

class FloatingCommand(Command):
    def __init__(self, enableDisableToggle: EnableDisableToggle, spacing: Iterable[str] = all_spaces):
        super().__init__()
        self.enableDisableToggle = enableDisableToggle
        self.spacing = spacing
    
    def __str__(self):
        return f"floating{self.spacing[0]}{str(self.enableDisableToggle)}"