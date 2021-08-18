from statements.statement import Statement
from typing import Iterable
from utils.all_spaces import all_spaces
from utils.enums import NoneEnum
from criteria_set import CriteriaSet
from enum import auto

class AssignOption(NoneEnum):
    WORKSPACE = auto()
    OUTPUT = auto()
    NUMBER = auto()
    NONE = auto()


class AssignStatement(Statement):
    def __init__(self, criteria_set: CriteriaSet, assign_option: AssignOption, target: str, has_arrow: bool = False, spacing: Iterable[str] = all_spaces):
        super().__init__()
        if assign_option == AssignOption.NUMBER:
            try:
                int(target)
            except ValueError:
                assert False
        self.criteria_set = criteria_set
        self.assign_option = assign_option
        self.target = target
        self.has_arrow = has_arrow
        self.spacing = spacing
    
    def __str__(self):
        spacing_iterator = iter(self.spacing)
        s = "assign"
        s += next(spacing_iterator)
        s += str(self.criteria_set)
        s += next(spacing_iterator)
        if self.has_arrow:
            s += "→"
            s += next(spacing_iterator)
        if self.assign_option != AssignOption.NONE:
            s += str(self.assign_option)
            s += next(spacing_iterator)
        s += str(self.target)

        return s

