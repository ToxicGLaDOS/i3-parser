from enum import Enum, auto
from typing import Iterable, List
from utils.all_spaces import all_spaces
from utils.enums import LowercaseEnum
from commands.command import Command

class WorkspaceDirectionOption(LowercaseEnum):
    NEXT = auto()
    PREV = auto()
    NEXT_ON_OUTPUT = auto()
    PREV_ON_OUTPUT = auto()

class WorkspaceCommand(Command):
    def __init__(self):
        super().__init__()

class WorkspaceBackAndForth(WorkspaceCommand):
    def __init__(self, spacing: Iterable[str] = all_spaces):
        super().__init__()
        self.spacing = spacing

    def __str__(self):
        return f"workspace{self.spacing[0]}back_and_forth"

class WorkspaceDirection(WorkspaceCommand):
    def __init__(self, workspace_direction: WorkspaceDirectionOption, spacing: Iterable[str] = all_spaces):
        super().__init__()
        self.workspace_direction = workspace_direction
        self.spacing = spacing
    
    def __str__(self):
        return f"workspace{self.spacing[0]}{str(self.workspace_direction)}"

class WorkspaceNumber(WorkspaceCommand):
    def __init__(self, number: int, spacing: Iterable[str] = all_spaces):
        super().__init__()
        self.number = number
        self.spacing = spacing
    
    def __str__(self):
        return f"workspace{self.spacing[0]}number{self.spacing[1]}{self.number}"

class WorkspaceLabeled(WorkspaceCommand):
    def __init__(self, workspace_label: str, spacing: Iterable[str] = all_spaces):
        super().__init__()
        self.workspace_label = workspace_label
    
    def __str__(self):
        return f"workspace{self.spacing[0]}{self.workspace_label}"
