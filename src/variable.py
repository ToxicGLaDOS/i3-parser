class Variable(object):
    def __init__(self, variable_name: str):
        super().__init__()
        self.variable_name = variable_name

    def __str__(self):
        return f"${self.variable_name}"