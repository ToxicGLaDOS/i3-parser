from enum import auto
from statements.statement import Statement
from utils.enums import LowercaseEnum, NoneEnum
from utils.all_spaces import all_spaces
from typing import Union, Iterable
from commands.command_set import CommandSet
from criteria_set import CriteriaSet

class ForWindowStatement(Statement):
    def __init__(self, criteria_set: CriteriaSet, commands: CommandSet, spacing: Iterable[str] = all_spaces):
        super().__init__()
        self.criteria_set = criteria_set
        self.commands = commands
        self.spacing = spacing
    
    def __str__(self):
        spacing_iterator = iter(self.spacing)
        s = "for_window"
        s += next(spacing_iterator)
        s += str(self.criteria_set)
        s += next(spacing_iterator)
        s += str(self.commands)
        return s

