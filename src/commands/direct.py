from enum import auto
from typing import Iterable
from utils.all_spaces import all_spaces
from utils.enums import LowercaseEnum
from commands.command import Command

class DirectCommandArgument(LowercaseEnum):
    EXIT = auto()
    RESTART = auto()
    RELOAD = auto()
    OPEN = auto()


class DirectCommand(Command):
    def __init__(self, argument: DirectCommandArgument):
        super().__init__()
        self.argument = argument
    
    def __str__(self):
        return f"{self.argument}"