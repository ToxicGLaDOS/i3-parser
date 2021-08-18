from statements.statement import Statement
from statements.comment import CommentStatement
from statements.binding import BindingStatement
from statements.empty import EmptyStatement
from statements.set import SetStatement
from typing import Iterable, Union
from utils.all_spaces import all_spaces
from enum import auto

class ModeBlockStatement(Statement):
    def __init__(self,
                 name: str,
                 statements: Union[CommentStatement, BindingStatement, EmptyStatement, SetStatement],
                 pango_markup_flag: bool,
                 spacing: Iterable[str] = all_spaces):
        super().__init__()
        # TODO: Ensure the statements are of proper type
        self.name = name
        self.statements = statements
        self.pango_markup_flag = pango_markup_flag
        self.spacing = spacing
    
    def __str__(self):
        spacing_iterator = iter(self.spacing)
        s = "mode"
        s += next(spacing_iterator)
        if self.pango_markup_flag:
            s += "--pango_markup"
            s += next(spacing_iterator)
        s += self.name
        # This space is tricky because we have no way of knowing
        # if it should be there or not, so self.spacing must include an ""
        # if it shouldn't be there
        s += next(spacing_iterator)
        s += "{\n"
        for statement in self.statements:
            s += next(spacing_iterator)
            s += str(statement)
            s += "\n"
        s += "}"
        return s

