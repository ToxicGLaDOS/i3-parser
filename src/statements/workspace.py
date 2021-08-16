from typing import Iterable
from utils.all_spaces import all_spaces
from statements.statement import Statement

class WorkspaceStatement(Statement):
    def __init__(self, workspace_name: str, output_name: str, spacing: Iterable[str] = all_spaces):
        super().__init__()
        # TODO: Check to make sure workspace_name and output_name are a single word or a quoted series of words
        self.workspace_name = workspace_name
        self.output_name = output_name
        self.spacing = spacing
    
    def __str__(self):
        spacing_iterator = iter(self.spacing)
        return f"workspace{next(spacing_iterator)}{self.workspace_name}{next(spacing_iterator)}output{next(spacing_iterator)}{self.output_name}"
