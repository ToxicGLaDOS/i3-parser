from utils.enums import LowercaseEnum
from utils.all_spaces import all_spaces
from typing import Iterable
from enum import auto

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

