from typing import Iterable
from utils.all_spaces import all_spaces
from commands.command import Command
from enum import Enum, auto

def all_semicolons():
    while True:
        yield ';'

class Separator(Enum):
    SEMICOLON = auto()
    COMMA = auto()
    NONE = auto()

    @staticmethod
    def from_string(s: str):
        if s == ';':
            return Separator.SEMICOLON
        elif s == ',':
            return Separator.COMMA
        elif s == None or s == "":
            return Separator.NONE
        else:
            raise ValueError
    
    def __str__(self):
        if self.name == "SEMICOLON":
            return ';'
        elif self.name == "COMMA":
            return ','
        elif self.name == "NONE":
            return ""
        else:
            raise NotImplementedError


class CommandSet(object):
    def __init__(self, commands: list[Command], separators: Iterable[Separator] = all_semicolons, spacing: Iterable[str] = all_spaces):
        super().__init__()
        self.commands = commands
        self.separators = separators
        self.spacing = spacing

    def __str__(self):
        spacing_iterator = iter(self.spacing)
        separators_iterator = iter(self.separators)
        s = str(self.commands[0])

        for command in self.commands[1:]:
            s += next(spacing_iterator)
            s += str(next(separators_iterator))
            s += next(spacing_iterator)
            s += str(command)
        
        return s

    def __iter__(self):
        return iter(self.commands)
    
    def __len__(self):
        return len(self.commands)