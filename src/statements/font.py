from typing import Iterable
from utils.all_spaces import all_spaces
from statements.statement import Statement


class FontStatement(Statement):
    def __init__(self, font_name: str, spacing: Iterable[str] = all_spaces):
        super().__init__()
        # TODO: Consider looking for font name and size (even though the parser takes it all in as one string)
        self.font_name = font_name
        self.spacing = spacing
    
    def __str__(self):
        spacing_iterator = iter(self.spacing)
        return f"font{next(spacing_iterator)}{self.font_name}"