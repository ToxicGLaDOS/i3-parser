from enum import Enum, auto
from abc import ABC, abstractmethod
from typing import Tuple, Iterable
from utils.all_spaces import all_spaces
from commands.command import Command


class FullscreenArgument(Enum):
    NONE = auto()
    ENABLE = auto()
    TOGGLE = auto()
    DISABLE = auto()

    @staticmethod
    def from_string(s: str):
        if s == '':
            return FullscreenArgument.NONE
        elif s == "enable":
            return FullscreenArgument.ENABLE
        elif s == "toggle":
            return FullscreenArgument.TOGGLE
        elif s == "disable":
            return FullscreenArgument.DISABLE
        else:
            raise ValueError(f"Expected one of ('', 'enable', 'toggle', 'disable'), got '{s}'")

    def __str__(self):
        if self.value != FullscreenArgument.NONE.value:
            return self.name.lower()
        # NONE means empty string
        else:
            return ''

class FullscreenCommand(Command):
    def __init__(self, arg: FullscreenArgument, is_global: bool = False, spacing: Iterable[str] = all_spaces):
        if arg.value == FullscreenArgument.DISABLE and is_global:
            raise ValueError("Can't have fullscreen argument 'disable' with is_global = True")
        self.arg = arg
        self.is_global = is_global
        self.spacing = spacing
    
    def __str__(self):
        spacing_index = 0
        s = "fullscreen"
        if self.arg != FullscreenArgument.NONE:
            s += self.spacing[spacing_index]
            spacing_index += 1
            s += str(self.arg)
        if self.is_global:
            s += self.spacing[spacing_index]
            spacing_index += 1
            s += "global"
        
        return s


