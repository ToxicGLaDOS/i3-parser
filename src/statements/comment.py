from typing import Iterable
from utils.all_spaces import all_spaces
from statements.statement import Statement


class CommentStatement(Statement):
    def __init__(self, comment_text: str):
        super().__init__()
        assert "\n" not in comment_text
        self.comment_text = comment_text
    
    def __str__(self):
        return f"#{self.comment_text}"