from statements.statement import Statement
from typing import Iterable
from utils.all_spaces import all_spaces
from utils.enums import LowercaseEnum
from enum import auto

def all_true():
    while True:
        yield True

class ModifierKey(LowercaseEnum):
    MOD1 = auto()
    MOD2 = auto()
    MOD3 = auto()
    MOD4 = auto()
    MOD5 = auto()
    SHIFT = auto()
    CONTROL = auto()
    CTRL = auto()

class FloatingModifierStatement(Statement):
    def __init__(self, modifiers: Iterable[ModifierKey], pluses: Iterable[bool] = all_true(), spacing: Iterable[str] = all_spaces):
        super().__init__()
        self.modifiers = modifiers
        self.pluses = pluses
        self.spacing = spacing

    def __str__(self):
        spacing_iterator = iter(self.spacing)
        pluses_iterator = iter(self.pluses)
        s = "floating_modifier"
        for modifier in self.modifiers:
            s += next(spacing_iterator)
            s += str(modifier)
            plus = next(pluses_iterator)
            if plus:
                s += next(spacing_iterator)
                s += "+"
        return s
