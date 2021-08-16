from typing import Iterable
from utils.all_spaces import all_spaces
from statements.statement import Statement


class SetStatement(Statement):
    def __init__(self, variable_name: str, value: str, spacing: Iterable[str] = all_spaces):
        super().__init__()
        self.variable_name = variable_name
        self.value = value
        self.spacing = spacing
    
    def __str__(self):
        spacing_iterator = iter(self.spacing)
        return f"set{next(spacing_iterator)}${self.variable_name}{next(spacing_iterator)}{self.value}"