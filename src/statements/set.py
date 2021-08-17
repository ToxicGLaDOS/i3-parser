from typing import Iterable
from utils.all_spaces import all_spaces
from statements.statement import Statement
from variable import Variable

class SetStatement(Statement):
    def __init__(self, variable: Variable, value: str, spacing: Iterable[str] = all_spaces):
        super().__init__()
        self.variable = variable
        self.value = value
        self.spacing = spacing
    
    def __str__(self):
        spacing_iterator = iter(self.spacing)
        return f"set{next(spacing_iterator)}{str(self.variable)}{next(spacing_iterator)}{self.value}"