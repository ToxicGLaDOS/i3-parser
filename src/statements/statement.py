from abc import ABC
from utils.all_spaces import all_spaces

class Statement(ABC):
    def __init__(self):
        self.spacing = all_spaces
    # Helper method used when building objects from the
    # the visitors. We just keep track of spaces in reverse
    # because we're parsing from the bottom of the ast up
    def _add_spacing_reversed(self, space: str):
        # If self.spacing is it's default value
        # then turn it into a list instead
        if self.spacing == all_spaces:
            self.spacing = []
        
        self.spacing.insert(0, space)