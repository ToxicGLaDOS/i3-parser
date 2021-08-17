from statements.statement import Statement
from utils.enums import LowercaseEnum, NoneEnum
from enum import auto
from typing import Union, Iterable
from utils.all_spaces import all_spaces
from abc import ABC

class ParameterizedCriteriaOption(LowercaseEnum):
    CLASS = auto()
    INSTANCE = auto()
    WINDOW_ROLE = auto()
    CON_ID = auto()
    ID = auto()
    WINDOW_TYPE = auto()
    CON_MARK = auto()
    TITLE = auto()
    URGENT = auto()
    WORKSPACE = auto()
    MACHINE = auto()
    FLOATING_FROM = auto()
    TILING_FROM = auto()

class SingleCriteriaOption(LowercaseEnum):
    TILING = auto()
    FLOATING = auto()
    ALL = auto()

class AssignOption(NoneEnum):
    WORKSPACE = auto()
    OUTPUT = auto()
    NUMBER = auto()
    NONE = auto()

class SingleCriteria(object):
    def __init__(self, criteria_option: SingleCriteriaOption):
        self.criteria_option = criteria_option

    def __str__(self):
        return f"{str(self.criteria_option)}"

class ParameterizedCriteria(object):
    def __init__(self, criteria_option: ParameterizedCriteriaOption, parameter: str):
        self.criteria_option = criteria_option
        self.parameter = parameter
    
    def __str__(self):
        return f"{str(self.criteria_option)}={self.parameter}"

class CriteriaSet(object):
    def __init__(self, criteria: list[SingleCriteria, ParameterizedCriteria], spacing: Iterable[str] = all_spaces):
        self.criteria = criteria
        self.spacing = spacing

    def __str__(self):
        spacing_iterator = iter(self.spacing)
        s = "["
        s += str(self.criteria[0])
        for criteria in self.criteria[1:]:
            s += next(spacing_iterator)
            s += str(criteria)
        s += "]"
        return s


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

