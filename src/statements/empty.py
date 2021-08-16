from statements.statement import Statement


class EmptyStatement(Statement):
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        return ""