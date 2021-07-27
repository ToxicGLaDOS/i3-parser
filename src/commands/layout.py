from enum import Enum, auto
from typing import Iterable, List
from utils.all_spaces import all_spaces
from utils.enums import LowercaseEnum
from commands.command import Command

class LayoutMode(LowercaseEnum):
    DEFAULT = auto()
    TABBED = auto()
    STACKING = auto()
    SPLITV = auto()
    SPLITH = auto()

class LayoutToggleOption(LowercaseEnum):
    SPLIT = auto()
    ALL = auto()

class LayoutToggleBetweenOption(LowercaseEnum):
    SPLIT = auto()
    TABBED = auto()
    STACKING = auto()
    SPLITV = auto()
    SPLITH = auto()

class LayoutCommand(Command):
    def __init__(self):
        super().__init__()


class LayoutSet(LayoutCommand):
    def __init__(self, mode: LayoutMode, spacing: Iterable[str] = all_spaces):
        super().__init__()
        self.mode = mode
        self.spacing = spacing

    def __str__(self):
        return f"layout{self.spacing[0]}{str(self.mode)}"

class LayoutToggle(LayoutCommand):
    def __init__(self, toggle: LayoutToggleOption, spacing: Iterable[str] = all_spaces):
        super().__init__()
        self.toggle = toggle
        self.spacing = spacing
    
    def __str__(self):
        return f"layout{self.spacing[0]}toggle{self.spacing[1]}{str(self.toggle)}"

class LayoutToggleBetween(LayoutCommand):
    def __init__(self, toggle_between: List[LayoutToggleBetweenOption], spacing: Iterable[str] = all_spaces):
        super().__init__()
        if len(toggle_between) == 0:
            raise ValueError("toggle_between must have at least one element in it.")
        self.toggles = toggle_between
        self.spacing = spacing
    
    def __str__(self):
        spacing_index = 0
        s = "layout"
        s += self.spacing[spacing_index]
        spacing_index += 1
        s += "toggle"
        for toggle in self.toggles:
            s += self.spacing[spacing_index]
            spacing_index += 1
            s += str(toggle)
        
        return s
