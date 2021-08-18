from statements.statement import Statement
from commands.command_set import CommandSet
from typing import Iterable
from utils.all_spaces import all_spaces
from enum import Enum, auto

class BindOption(Enum): 
    RELEASE = auto()
    BORDER = auto()
    WHOLE_WINDOW = auto()
    EXCLUDE_TITLEBAR = auto()

    @staticmethod
    def from_str(s: str):
        if s == "--release":
            return BindOption.RELEASE
        elif s == "--border":
            return BindOption.BORDER
        elif s == "--whole-window":
            return BindOption.WHOLE_WINDOW
        elif s == "--exclude-titlebar":
            return BindOption.EXCLUDE_TITLEBAR
        else:
            raise ValueError(f"Expected one of (--release, --border, --whole-window, --exclude-titlebar), got {s}")

    def __str__(self):
        return '--' + self.name.lower().replace('_', '-')



class BindingStatement(Statement):
    def __init__(self,
                 keyword: str,
                 bind_options0: list[BindOption],
                 key: str,
                 bind_options1: list[BindOption],
                 commands: CommandSet,
                 spacing: Iterable[str] = all_spaces):
        self.keyword = keyword
        self.bind_options0 = bind_options0
        self.key = key
        self.bind_options1 = bind_options1
        self.commands = commands
        self.spacing = spacing
    
    def __str__(self):
        spacing_iterator = iter(self.spacing)
        s = self.keyword
        for bind_option in self.bind_options0:
            s += next(spacing_iterator)
            s += str(bind_option)
        
        s += next(spacing_iterator)
        s += self.key
        for bind_option in self.bind_options1:
            s += next(spacing_iterator)
            s += str(bind_option)
        
        s += next(spacing_iterator)
        s += str(self.commands)
        
        return s
