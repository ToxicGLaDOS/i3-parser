from enum import Enum, auto
from typing import Iterable
from utils.all_spaces import all_spaces
from utils.enums import Direction
from commands.command import Command


class FocusModeOption(Enum):
    MODE_TOGGLE = auto()
    TILING = auto()
    FLOATING = auto()

    @staticmethod
    def from_string(s: str):
        return FocusModeOption[s.upper()]
    
    def __str__(self):
        return self.name.lower()

class FocusTargetOption(Enum):
    CHILD = auto()
    PARENT = auto()
    
    @staticmethod
    def from_string(s: str):
        return FocusTargetOption[s.upper()]
    
    def __str__(self):
        return self.name.lower()

class FocusRelativeOption(Enum):
    PREV = auto()
    NEXT = auto()

    @staticmethod
    def from_string(s: str):
        return FocusRelativeOption[s.upper()]
    
    def __str__(self):
        return self.name.lower()

class FocusCommand(Command):
    pass

class FocusMode(FocusCommand):
    def __init__(self, mode: FocusModeOption, spacing: Iterable[str] = all_spaces):
        self.mode = mode
        self.spacing = spacing
    
    def __str__(self):
        return f"focus{self.spacing[0]}{str(self.mode)}"

class FocusDirection(FocusCommand):
    def __init__(self, direction: Direction, spacing: Iterable[str] = all_spaces):
        self.direction = direction
        self.spacing = spacing

    def __str__(self):
        return f"focus{self.spacing[0]}{str(self.direction)}"

class FocusTarget(FocusCommand):
    def __init__(self, target: FocusTargetOption, spacing: Iterable[str] = all_spaces):
        self.target = target
        self.spacing = spacing
    
    def __str__(self):
        return f"focus{self.spacing[0]}{str(self.target)}"

class FocusOutput(FocusCommand):
    def __init__(self, output: str, spacing: Iterable[str] = all_spaces):
        self.output = output
        self.spacing = spacing
    
    def __str__(self):
        return f"focus{self.spacing[0]}output{self.spacing[1]}{self.output}"

class FocusRelative(FocusCommand):
    def __init__(self, relative: FocusRelativeOption, sibling: bool = False, spacing: Iterable[str] = all_spaces):
        self.relative = relative
        self.sibling = sibling
        self.spacing = spacing
    
    def __str__(self):
        s = f"focus{self.spacing[0]}{str(self.relative)}"
        if self.sibling:
            s += self.spacing[1]
            s += "sibling"
        
        return s